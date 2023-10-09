# Import Discord Python Libaries
import discord
from discord.ext import commands

# Import the Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Necessary Local Files
from bot.logger.parser import export_logfile
from config import export_config_to_json, import_config_from_json
from config import export_bot_data, import_bot_data

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
        It also attempts to retrieve information from the data files if they exist.

    Arguments:
        None

    Returns:
        None
    """
    
    # Update Logger with Login Information
    logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    
    # Import Bot Data from Files if it exists
    logger.info("Attempting to Retrieve Data from Data Files...")
    import_bot_data()
    


@bot.event
async def on_disconnect():
    """
    Description:
        Event handler triggered when the bot disconnects from the Discord server.
        This function is responsible for exporting bot data to the data files if the bot goes offline.

    Arguments:
        None

    Returns:
        None
    """
    
    # Export Data to the Data Files
    export_bot_data()

