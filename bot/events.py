# Import Discord Python Libaries
import discord
from discord.ext import commands

# Import the Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Necessary Local Files
from bot.logger.parser import export_logfile
from events.flight_logs import update_event_status

# Import datetime library to check latency
import datetime

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
    logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    
    # Start the Event Activity Status
    update_event_status.start()


@bot.event
async def on_disconnect():
    """
    Description:
        Event handler triggered when the bot disconnects from the Discord server.

        This function is responsible for exporting log data to a CSV file when the bot goes offline.
        It logs a message to indicate the export process has started and another message when the export is complete.

        Note:
        - Make sure to configure the `export_logfile` function appropriately to export log data as desired.
        - This event is useful for ensuring log data is saved before the bot goes offline.

    Arguments:
        None

    Returns:
        None
    """
    logger.info('Bot Disconnecting. Exporting log data...')
    export_logfile()
    logger.info('Log Data Exported.')

