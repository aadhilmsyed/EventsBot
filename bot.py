# Import Discord Python Library
import discord
from discord.enums import EventStatus
from discord.ext import commands
import os

from config import config, flight_hours_manager
from logger import logger

# Configure User-Agent header to comply with Discord API requirements and RFC 9110
# Discord requires: DiscordBot ($url, $versionNumber)
# RFC 9110 format: product (comment) where comment can contain version info
# Format is RFC-compliant: product token followed by comment in parentheses
bot_url = os.getenv("BOT_URL", "https://github.com/discord/discord-api-docs")
bot_version = os.getenv("BOT_VERSION", "2.4.2")
# Using Discord's exact format: DiscordBot ($url, $versionNumber)
# This is RFC 9110 compliant (product token + comment)
user_agent = f"DiscordBot ({bot_url}, {bot_version})"

# Monkey-patch discord.http.HTTPClient to always include User-Agent
# This must be done BEFORE any HTTPClient instances are created
_original_http_init = discord.http.HTTPClient.__init__
_original_http_request = discord.http.HTTPClient.request


def _patched_http_init(self, *args, **kwargs):
    """Patched HTTPClient.__init__ to set User-Agent immediately"""
    _original_http_init(self, *args, **kwargs)
    # Set User-Agent as soon as HTTPClient is created
    if hasattr(self, 'user_agent'):
        self.user_agent = user_agent
        print(f"HTTPClient initialized - Set user_agent attribute: {user_agent}")
    
    # Also patch the aiohttp session if it exists
    # discord.py uses aiohttp.ClientSession internally
    try:
        # Wait for session to be created (it might be created lazily)
        # We'll patch it in setup_hook or when it's first accessed
        pass
    except Exception as e:
        print(f"Note: Could not patch session in __init__: {e}")


async def _patched_http_request(self, route, *, files=None, form=None, **kwargs):
    """Patched HTTPClient.request to ensure User-Agent is always included"""
    # Ensure headers dict exists
    headers = kwargs.get('headers', {})
    if headers is None:
        headers = {}
    
    # Always set User-Agent if not already set
    if 'User-Agent' not in headers:
        headers['User-Agent'] = user_agent
        print(f"✓ Added User-Agent to request headers: {user_agent}")
    else:
        print(f"✓ User-Agent already in headers: {headers.get('User-Agent')}")
    
    kwargs['headers'] = headers
    
    # Also ensure the user_agent attribute is set on the HTTPClient
    if hasattr(self, 'user_agent'):
        self.user_agent = user_agent
    
    try:
        return await _original_http_request(self, route, files=files, form=form, **kwargs)
    except discord.errors.HTTPException as e:
        # Handle Cloudflare rate limiting (Error 1015)
        if e.status == 429 or (e.status == 403 and '1015' in str(e.response)):
            error_msg = str(e.response) if hasattr(e, 'response') else str(e)
            if '1015' in error_msg or 'rate limit' in error_msg.lower():
                print(f"⚠ Cloudflare Error 1015: IP temporarily banned. This usually clears in 15-60 minutes.")
                print(f"   The User-Agent header is correctly configured: {user_agent}")
                print(f"   Please wait for the IP ban to expire before retrying.")
        raise


# Apply the monkey-patch
discord.http.HTTPClient.__init__ = _patched_http_init
discord.http.HTTPClient.request = _patched_http_request
print(f"✓ Patched discord.http.HTTPClient to include User-Agent: {user_agent}")


class CustomBot(commands.Bot):
    """Custom Bot class (User-Agent is configured via module-level patch)"""
    
    async def setup_hook(self):
        """Called when the bot is being set up, before login"""
        await super().setup_hook()
        # Verify User-Agent is configured and patch aiohttp session
        if hasattr(self, 'http') and self.http:
            if hasattr(self.http, 'user_agent'):
                print(f"✓ Verified User-Agent in HTTPClient: {self.http.user_agent}")
            
            # Also patch the aiohttp session's default headers
            try:
                # Try to access the session
                session = None
                if hasattr(self.http, '_HTTPClient__session'):
                    session = self.http._HTTPClient__session
                elif hasattr(self.http, 'session'):
                    session = self.http.session
                elif hasattr(self.http, '_session'):
                    session = self.http._session
                
                if session:
                    # Update the session's default headers
                    if not hasattr(session, '_default_headers'):
                        session._default_headers = {}
                    session._default_headers['User-Agent'] = user_agent
                    print(f"✓ Set aiohttp session _default_headers['User-Agent']: {user_agent}")
                    
                    # Also ensure it's in the headers dict if it exists
                    if hasattr(session, 'headers'):
                        if session.headers is None:
                            session.headers = {}
                        session.headers['User-Agent'] = user_agent
                        print(f"✓ Set aiohttp session headers['User-Agent']: {user_agent}")
            except Exception as e:
                print(f"Note: Could not patch aiohttp session: {e}")


# Define Intents & Create Bot Object
intents = discord.Intents.all()
bot = CustomBot(command_prefix="!", intents=intents, help_command=None)

# Remove the help command
bot.remove_command("help")


# Function to Determine Successful Connection
@bot.event
async def on_ready():
    """
    Description:
        An event handler triggered when the bot successfully connects to Discord.
        This function is automatically called when the bot logs in and is ready to operate.
        It prints the bot's username and user ID to the console as a confirmation of successful login.

    Arguments:
        None

    Returns:
        None
    """
    # Update Logger with Login Information
    config.guild = bot.get_guild(config.guild_id)
    config.log_channel = config.guild.get_channel(config.log_channel_id)
    await logger.setChannel(config.log_channel)
    await logger.info(f"Logged in as {bot.user.name} ({bot.user.id})")

    # Load in Configuration Data from File
    config.load()
    flight_hours_manager.load()

    # If there is an ongoing event retrieve the event VC
    if flight_hours_manager.active_event:
        await logger.info(f"Resuming Event Logging...")
        return

    # If an event has already started, then start logging for that event
    for event in config.guild.scheduled_events:
        if event.status == EventStatus.active:

            # Update Logger Information
            await logger.info(f"Starting Flight Logging for Event '{event.name}'.")

            # Update the Event Voice Channel & Event Status Flag
            flight_hours_manager.active_event = event.name
            flight_hours_manager.event_history[event.name] = set()
            if event.channel:
                flight_hours_manager.voice_channels.append(event.channel)

            # If Members Are Already in the Voice Channel, Log Them
            if event.channel:
                for member in event.channel.members:
                    flight_hours_manager.log_start_time(member.id)
                    await logger.info(
                        f"{member.mention} Joined {event.channel.mention}. Starting Logging..."
                    )

            break


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)
    await logger.error(f"{error} {ctx.message.jump_url}")


@bot.event
async def on_disconnect():
    """Handle bot disconnection"""
    # await logger.error("Bot disconnected from Discord. Attempting to reconnect...")
    pass


@bot.event
async def on_resume():
    """Handle bot reconnection"""
    # await logger.info("Bot reconnected to Discord successfully.")
    pass


@bot.event
async def on_error(event, *args, **kwargs):
    """Handle general bot errors"""
    await logger.error(f"An error occurred in event {event}: {args} {kwargs}")
