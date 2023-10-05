# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Other Necessary Files
import json

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

# Embed Thumbnail for METAR commands
metar_embed_thumbnail_url = "https://media.istockphoto.com/id/537337166/photo/air-trafic-control-tower-and-airplance-at-paris-airport.jpg?b=1&s=612x612&w=0&k=20&c=kp14V8AXFNUh5jOy3xPQ_sxhOZLWXycdBL-eUGviMOQ="


##############################################
# CONFIGURATION FUNCTIONS
##############################################

# Function to export configuration to a JSON file
async def export_config_to_json(filename):
    """
    Descrptions:
        Exports data to a JSON file when bot disconnects
    
    Arguments:
        filename (str) : Name of the Export File
    
    Returns:
        None
    """
    try:
    
        # Declare Global Variables
        global restricted_channels, flight_hours, start_time
        
        # Data to be Exported
        data = {
            "restricted_channels": restricted_channels,
            "flight_hours": flight_hours,
            "start_time": start_time
        }
        
        # Print Logger Message
        logger.info(f"Exporting Data to {filename}...")
        
        # Open the JSON file and write the data to it
        with open(filename, 'w') as json_file:
            json.dump(data, json_file)
            
        # Print Logger Message
        logger.info("Exported Data Successfully.")
    
    except Exception as e: logger.error(e)


# Function to import configuration from a JSON file
async def import_config_from_json(filename):
    """
    Descrptions:
        Imports data from JSON file when bot reconnecst
    
    Arguments:
        filename (str) : Name of the Import File
    
    Returns:
        None
    """
    try:
    
        # Declare Global Variables
        global restricted_channels, flight_hours, start_time
        
        # Print Logger Message
        logger.info(f"Importing Data from {filename}...")
        
        # Open the JSON File and Read the Data from it
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            restricted_channels = data.get("restricted_channels", [])
            flight_hours = data.get("flight_hours", {})
            start_time = data.get("start_time", {})
            
        # Print Logger Message
        logger.info("Imported Data Successfully.")
    
    except Exception as e: logger.error(e)
