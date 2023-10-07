# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Other Necessary Files
import json
import csv
import pandas as pd


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


async def import_flight_hours(file_path = 'data/flight_hours.csv'):
    """
    Descrptions:
        Imports flight hours data from the CSV File
    
    Arguments:
        file_path (str) : String containing the file path
    
    Returns:
        None
    """
    try:
    
        # Import Data from CSV file into a Dataframe
        df = pd.read_csv(file_path)
        
        # Convert the Dataframe into a Dictionary
        flight_hours = df.to_dict(orient='dict')
        
        # Return the dictionary
        return flight_hours

    # If File is Not Found, then Create it
    except FileNotFoundError:
        with open(file_path, 'w') as file: logger.info(f'{file_path} was created'); return {}
        
    # Log any Errors
    except Exception as e: logger.error(e); return {};


async def export_flight_hours(flight_hours, file_path = 'data/flight_hours.csv'):
    """
    Descrptions:
        Exports flight hours data to the CSV File
    
    Arguments:
        flight_hours (dict) : The dictionary to export to the CSV file
        file_path (str) : String containing the file path
    
    Returns:
        None
    """
    try:
        
        # Convert the Dictionary into a Pandas Dataframe
        df = pd.DataFrame(flight_hours)
        
        # Export the DataFrame to CSV File
        df.to_csv('data/flight_hours.csv')

    # Log any Errors
    except Exception as e: logger.error(e)


async def import_start_times(file_path = 'data/start_times.csv'):
    """
    Descrptions:
        Imports start times data from the CSV File
    
    Arguments:
        file_path (str) : String containing the file path
    
    Returns:
        None
    """
    try:
    
        # Import Data from CSV file into a Dataframe
        df = pd.read_csv(file_path)
        
        # Convert the Dataframe into a Dictionary
        start_times = df.to_dict(orient='dict')
        
        # Return the dictionary
        return start_times

    # If File is Not Found, then Create it
    except FileNotFoundError:
        with open(file_path, 'w') as file: logger.info(f'{file_path} was created'); return {}
        
    # Log any Errors
    except Exception as e: logger.error(e); return {};
    

async def export_start_times(start_times, file_path = 'data/start_times.csv'):
    """
    Descrptions:
        Exports start times data to the CSV File
    
    Arguments:
        flight_hours (dict) : The dictionary to export to the CSV file
        file_path (str) : String containing the file path
    
    Returns:
        None
    """
    try:
    
        # Convert the Dictionary into a Pandas Dataframe
        df = pd.DataFrame(start_times)
        
        # Export the DataFrame to CSV File
        df.to_csv(file_path)

    # Log any Errors
    except Exception as e: logger.error(e)


async def import_restricted_channels(file_path='data/restricted_channels.txt'):
    """
    Descrptions:
        Imports restricted channels data from the txt File
    
    Arguments:
        file_path (str) : String containing the file path
    
    Returns:
        None
    """
    try:
    
        # Import Data from Text File into a List
        with open(file_path, 'r') as file:
            restricted_channels = [line.strip() for line in file.readlines()]
        
        # Return the List of Channels
        return restricted_channels
    
    # If no File is Found, then Create One
    except FileNotFoundError:
        with open(file_path, 'w') as file: logger.info(f'{file_path} was created')
        return []
    
    # Log any Errors
    except Exception as e: logger.error(e); return []


async def export_restricted_channels(restricted_channels, file_path='data/restricted_channels.txt'):
    """
    Descrptions:
        Exports restricted channels data to a txt File
    
    Arguments:
        restricted_channels (list) : List of Restricted Channels
        file_path (str) : String containing the file path
    
    Returns:
        None
    """
    try:

        # Write the New Restricted Channels to the File
        with open(file_path, 'w') as file:
            for channel_id in restricted_channels:
                file.write(f"{channel_id}\n")
                
    # Log any Errors
    except Exception as e: logger.error(e); return {};


async def import_event_status(file_path = 'data/event_status.txt'):
    """
    Descrptions:
        Imports the event status and current voice channel from a txt file
    
    Arguments:
        file_path (str) : String containing the file path
    
    Returns:
        None
    """
    try:
        
        # Import the Event Status Data from txt File
        with open(file_path, 'r') as file:
            is_event_active_str, voice_channel_str = file.read().strip().split('\n')
            is_event_active = (is_event_active_str.lower() == 'true')
            voice_channel = voice_channel_str if voice_channel_str else None
            
        # Return the Variables
        return is_event_active, voice_channel
        
    # If no File is Found, then Create One
    except FileNotFoundError:
        with open(file_path, 'w') as file: logger.info(f'{file_path} was created')
        return False, None
    
    # Log any Errors
    except Exception as e: logger.error(e); return []


async def export_event_status(is_event_active, voice_channel, file_path = 'data/event_status.txt'):
    """
    Descrptions:
        Exports the event status and current voice channel to a txt file
    
    Arguments:
        is_event_active (bool) : True indicates event is currently ongoing
        voice_channel (discord.VoiceChannel) : Voice Channel of Event
        file_path (str) : String containing the file path
    
    Returns:
        None
    """
    try:

        # Write the Event Status to the File
        with open(file_path, 'w') as file:
            file.write(f"{str(is_event_active).lower()}\n")
            file.write(f"{voice_channel}\n")
                
    # Log any Errors
    except Exception as e: logger.error(e); return {};

