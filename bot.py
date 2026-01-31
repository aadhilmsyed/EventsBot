# Import Discord Python Library
import discord
from discord.enums import EventStatus
from discord.ext import commands
import os

from config import config, flight_hours_manager
from logger import logger

# Configure User-Agent header to comply with Discord API requirements
# Format: DiscordBot ($url, $versionNumber)
# This prevents Cloudflare access denied errors
bot_url = os.getenv("BOT_URL", "https://github.com/discord/discord-api-docs")
bot_version = os.getenv("BOT_VERSION", "2.4.2")
user_agent = f"DiscordBot ({bot_url}, {bot_version})"


class CustomBot(commands.Bot):
    """Custom Bot class that ensures User-Agent header is properly set"""
    
    async def setup_hook(self):
        """Called when the bot is being set up, before login"""
        await super().setup_hook()
        # Configure User-Agent header after HTTP client is initialized
        await self._configure_user_agent()
    
    async def _configure_user_agent(self):
        """
        Configure the HTTP client with proper User-Agent header.
        
        Discord API requires: User-Agent: DiscordBot ($url, $versionNumber)
        This prevents Cloudflare access denied errors.
        
        Note: Content-Type headers are automatically handled by discord.py
        (application/json, application/x-www-form-urlencoded, or multipart/form-data)
        """
        try:
            if hasattr(self, 'http') and self.http:
                http_client = self.http
                configured = False
                
                # Method 1: Set the user_agent attribute directly if it exists
                if hasattr(http_client, 'user_agent'):
                    http_client.user_agent = user_agent
                    configured = True
                
                # Method 2: Patch the aiohttp session's default headers
                # discord.py uses aiohttp.ClientSession internally
                session = None
                
                # Try different ways to access the session
                if hasattr(http_client, '_HTTPClient__session'):
                    session = http_client._HTTPClient__session
                elif hasattr(http_client, 'session'):
                    session = http_client.session
                elif hasattr(http_client, '_session'):
                    session = http_client._session
                
                if session:
                    # Update the session's default headers
                    # aiohttp.ClientSession uses _default_headers dict
                    if not hasattr(session, '_default_headers'):
                        session._default_headers = {}
                    session._default_headers['User-Agent'] = user_agent
                    configured = True
                    
                    # Also ensure it's in the headers dict if it exists
                    if hasattr(session, 'headers'):
                        if session.headers is None:
                            session.headers = {}
                        session.headers['User-Agent'] = user_agent
                        configured = True
                
                # Method 3: Monkey-patch the request method to always include User-Agent
                # This is a fallback to ensure the header is always sent
                if hasattr(http_client, 'request'):
                    original_request = http_client.request
                    
                    async def patched_request(*args, **kwargs):
                        """Patched request method that ensures User-Agent is always set"""
                        # Get or create headers dict
                        headers = kwargs.get('headers', {})
                        if headers is None:
                            headers = {}
                        
                        # Ensure User-Agent is set
                        if 'User-Agent' not in headers:
                            headers['User-Agent'] = user_agent
                        
                        kwargs['headers'] = headers
                        return await original_request(*args, **kwargs)
                    
                    http_client.request = patched_request
                    configured = True
                
                if configured:
                    print(f"User-Agent header configured: {user_agent}")
                else:
                    print(f"Warning: Could not configure User-Agent header (discord.py should handle this automatically)")
                    
        except Exception as e:
            # Log but don't fail - discord.py should handle this
            print(f"Warning: Could not configure User-Agent header: {e}")


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
    # Ensure User-Agent is configured (fallback in case setup_hook didn't work)
    await bot._configure_user_agent()
    
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
