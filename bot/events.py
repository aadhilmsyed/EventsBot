# Import Discord Python Libaries
import discord
from discord.ext import commands

# Import the Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Necessary Local Files
from config import import_start_times, export_start_times
from config import import_event_status, export_event_status
from events.flight_logs import log_vc_members, update_flight_hours

# Import datetime library to check latency
import datetime
import os

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
    try:
    
        # Update Logger with Login Information
        logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
        
        # Import Configuration File if it exists
        is_event_active, voice_channel = await import_event_status()
        
        # If there is an event ongoing, start logging it
        if is_event_active:
            logger.info("Ongoing Event Detected. Starting Logging...")
            log_vc_members(voice_channel)
            
    except Exception as e: logger.error(e)


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
    try:

        # If there is an event ongoing, save the current logged flight time
        logger.info("Bot Disconnecting. Saving Flight Hours...")
        update_flight_hours()
    
    except Exception as e: logger.error(e)
