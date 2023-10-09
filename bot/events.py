# Import Discord Python Libaries
import discord
from discord.enums import EventStatus
from discord.ext import commands

# Import the Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Necessary Local Files
from bot.logger.parser import export_logfile
#from config import export_config_to_json, import_config_from_json
from config import export_bot_data, import_bot_data
from config import is_event_active
from events.flight_logs import log_vc_members

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
    
    # Declare global variable
    global is_event_active, guild
    
    # Update Logger with Login Information
    logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    
    # Import Bot Data from Files if it exists
    logger.info("Attempting to Retrieve Data from Data Files...")
    await import_bot_data()
    
    # If there is an active event, then start logging
    if is_event_active:
        for event in guild.scheduled_events:
            if event.status == EventStatus.active:
                log_vc_members(event.channel)
    


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
    logger.info("Bot Disconnecting. Attempting to Export Data...")
    await export_bot_data()


def log_left_member(member_name):
    """
    Descrption:
        This helper function logs any members who have left the voice channel or if an event
        has eneded. This function will calculate the amount of time the member has been in
        the voice channel and it will update their flight hours accordingly.
        
    Arguments:
        member_name (str) : Name of member - key to access flight hours and start times
        
    Returns:
        None
    """
    try:
    
        # Calculate the Elapsed Time of the Member in VC
        elapsed_time = time.now(pytz.utc) - start_time[member_name]
        
        # Add the Elapsed Time to the Member's Flight Hours
        if member_name not in flight_hours: flight_hours[member_name] = elapsed_time
        else: flight_hours[member_name] += elapsed_time
        
        # Update Logger Information
        logger.info(f"{member_name} Left the Event. Logging Complete ({elapsed_time}).")
        logger.info(f"{member_name} Total Flight Hours - {flight_hours[member_name]}.")
        logger.info(f"flight_hours now has a total of {len(flight_hours)} members.")
        
        # Delete that member instance from start times
        del start_time[member_name]
    
    # Log any Errors
    except Exception as e: logger.error(e)
