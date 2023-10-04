# Import Discord Python Libaries
import discord
from discord.ext import commands

# Import the Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Necessary Local Files
from bot.logger.parser import export_logfile
from config import export_config_to_json, import_config_from_json

# Import datetime library to check latency
import datetime
import os

# Global Variable to Store config file name
config_file = 'data/config.json'

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
    
    # Import Configuration File if it exists
    if os.path.exists(config_file):
        logger.info(f"Importing Data from {config_file}...")
        import_config_from_json(config_file)
        logger.info("Successfully Imported Data.")


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
    logger.info('Bot Disconnecting. Exporting Data...')
    df = await export_logfile()
    df.to_csv("data/log_file.csv")
    await export_config_to_json(config_file)
    logger.info('All Data Successfully Exported.')

