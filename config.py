# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

## Import Necessary Local Files
#from events.flight_logs import log_left_member

# Import Other Necessary Files
import json
import os
import datetime

##############################################
# GLOBAL VARIABLES
##############################################

# List of restricted announcement channels
restricted_channels = []

# Dictionary of Flight Hours
flight_hours = {}

# Dictionary to Store Amount of Time in Voice Channel
start_time = {}

# Flag to Indicate whether an Event is active or not
is_event_active = False

# Voice Channel of the Event
voice_channel = None

# Define role IDs for different tiers
roles = { # Role ID, Hours
    989232534313369630: 8,
    1110680241569017966: 5,
    1110680332879011882: 3,
    1112981412191146004: 1
}

guild = bot.get_guild(553718744233541656)

# Embed Thumbnail for METAR commands
metar_embed_thumbnail_url = "https://media.istockphoto.com/id/537337166/photo/air-trafic-control-tower-and-airplance-at-paris-airport.jpg?b=1&s=612x612&w=0&k=20&c=kp14V8AXFNUh5jOy3xPQ_sxhOZLWXycdBL-eUGviMOQ="


##############################################
# CONFIGURATION FUNCTIONS
##############################################

## Function to export configuration to a JSON file
#async def export_config_to_json(filename):
#    """
#    Descrptions:
#        Exports data to a JSON file when bot disconnects
#
#    Arguments:
#        filename (str) : Name of the Export File
#
#    Returns:
#        None
#    """
#    try:
#
#        # Declare Global Variables
#        global restricted_channels, flight_hours, start_time
#
#        # Data to be Exported
#        data = {
#            "restricted_channels": restricted_channels,
#            "flight_hours": flight_hours,
#            "start_time": start_time
#        }
#
#        # Print Logger Message
#        logger.info(f"Exporting Data to {filename}...")
#
#        # Open the JSON file and write the data to it
#        with open(filename, 'w') as json_file:
#            json.dump(data, json_file)
#
#        # Print Logger Message
#        logger.info("Exported Data Successfully.")
#
#    except Exception as e: logger.error(e)
#
#
## Function to import configuration from a JSON file
#async def import_config_from_json(filename):
#    """
#    Descrptions:
#        Imports data from JSON file when bot reconnecst
#
#    Arguments:
#        filename (str) : Name of the Import File
#
#    Returns:
#        None
#    """
#    try:
#
#        # Declare Global Variables
#        global restricted_channels, flight_hours, start_time
#
#        # Print Logger Message
#        logger.info(f"Importing Data from {filename}...")
#
#        # Open the JSON File and Read the Data from it
#        with open(filename, 'r') as json_file:
#            data = json.load(json_file)
#            restricted_channels = data.get("restricted_channels", [])
#            flight_hours = data.get("flight_hours", {})
#            start_time = data.get("start_time", {})
#
#        # Print Logger Message
#        logger.info("Imported Data Successfully.")
#
#    except Exception as e: logger.error(e)

async def export_bot_data():
    """
    Descrptions:
        In case the bot disconnects, this helper function when called will export all of the data to a .txt file. This includes
        the flight hours, restricted channels, start times, and event status.
    
    Arguments:
        None
    
    Returns:
        None
    """
    try:
    
        # Declare global variables
        global flight_hours, start_time, restricted_channels, is_event_active, voice_channel
        
        # Log the Flight Hours of any Members who might be in the Voice Channel
        for member_name in list(start_time.keys()): log_left_member(member_name)
        
        # Export Data for the Flight Hours
        logger.info("Exporting Flight Hours to data/flight_hours.txt...")
        with open('data/flight_hours.txt', 'w') as file:
        
            # Write the flight hour data of every member to the file
            for member_name in list(flight_hours.keys()):
                minutes = (flight_hours[member_name].total_seconds() / seconds)
                file.write(f"{member_name} || {minutes}\n")
            
        # Update Logger Information
        logger.info("Successfully Exported Flight Hours.")
                
        # Export Data for the Start Times
        logger.info("Exporting Start Times to data/start_times.txt...")
        with open('data/start_times.txt', 'w') as file:
        
            # Write the start_time data of every member to the file
            for member_name in list(start_time.keys()):
                time_str = start_time[member_name].isoformat()
                file.write(f"{member_name} || {time_str}\n")
                
        # Update Logger Information
        logger.info("Successfully Exported Start Times.")
                
        # Export Data for the Restricted Channels
        logger.info("Exporting Restricted Channels to data/restricted_channels.txt...")
        with open('data/restricted_channels.txt', 'w') as file:
        
            # Write all the retricted channels to the file
            for channel_id in restricted_channels:
                file.write(f"{channel_id}\n")
                
        # Update Logger Information
        logger.info("Successfully Exported Restricted Channels.")
                
        # Export Data for the Event Status
        logger.info("Exporting Event Status to data/event_status.txt...")
        with open('data/event_status.txt', 'w') as file:
        
            # Write the is_event_active and voice channel data to the file
            file.write(f"{str(is_event_active).lower()}\n")

        # Update Logger Information
        logger.info("Successfully Exported Event Status.")
        
    # Log any Errors
    except Exception as e: logger.error(e)
    

async def import_bot_data():
    """
    Descrptions:
        Imports data from .txt files to restore bot data when the bot reconnects.
    
    Arguments:
        None
    
    Returns:
        None
    """
    try:
    
        # Declare global variables
        global flight_hours, start_time, restricted_channels, is_event_active, voice_channel

        # Import Data for the Flight Hours
        flight_hours = {}
        if os.path.exists('data/flight_hours.txt'):
            with open('data/flight_hours.txt', 'r') as file:
                logger.info("Importing Flight Hours from data/flight_hours.txt...")
                for line in file:
                    parts = line.strip().split(" || ")
                    if len(parts) == 2:
                        member_name = parts[0]
                        minutes = float(parts[1])
                        flight_hours[member_name] = datetime.timedelta(minutes=minutes)
                logger.info("Successfully Imported Flight Hours.")
        else: logger.info("data/flight_hours.txt could not be found.")

        # Import Data for the Start Times
        start_time = {}
        if os.path.exists('data/start_times.txt'):
            with open('data/start_times.txt', 'r') as file:
                logger.info("Importing Start Times from data/start_times.txt...")
                for line in file:
                    parts = line.strip().split(" || ")
                    if len(parts) == 2:
                        member_name = parts[0]
                        time_str = parts[1]
                        start_time[member_name] = datetime.datetime.fromisoformat(time_str)
                logger.info("Successfully Imported Start Times.")
        else: logger.info("data/start_times.txt could not be found.")

        # Import Data for the Restricted Channels
        restricted_channels = []
        if os.path.exists('data/restricted_channels.txt'):
            with open('data/restricted_channels.txt', 'r') as file:
                logger.info("Importing Restricted Channels from data/restricted_channels.txt...")
                for line in file:
                    channel_id = line.strip()
                    restricted_channels.append(channel_id)
                logger.info("Successfully Imported Restricted Channels.")
        else: logger.info("data/restricted_channels.txt could not be found.")

        # Import Data for the Event Status
        if os.path.exists('data/event_status.txt'):
            with open('data/event_status.txt', 'r') as file:
                logger.info("Importing Event Status from data/event_status.txt...")
                is_event_active_str = file.readline().strip().lower()
                is_event_active = is_event_active_str == 'true'
                logger.info("Successfully Imported Event Status.")
        else: logger.info("data/event_status.txt could not be found.")
            
    # Log any Errors
    except Exception as e: logger.error(e)

