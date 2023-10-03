# Import Discord Python Libraries
import discord
from discord.enums import EventStatus
from discord.ext import commands, tasks

# Import Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Necessary Local Files
from config import flight_hours, start_time
from config import voice_channel, is_event_active

# Import Other Necessary Libraries
from datetime import datetime as time
import pytz

# Declare Global Variables
global is_event_active
global voice_channel
global flight_hours
global start_time

@bot.event
async def on_voice_state_update(member, before, after):
    """
    Description:
        This bot event function monitors changes between the voice channel to track flight hours.
        If the is_event_active flag is enabled, this function will track the hours of each
        member in the voice channel until they leave.
    
    Arguments:
        member : The member that is switching voice channels
        before : The voice channel that the member was in before (if any)
        after  : The voice channel that the member was in after (if any)
        
    Returns:
        None
    """
    try:
    
        # Declare Global Variables
        global is_event_active
        global voice_channel
        global flight_hours
        global start_time

        # Exit the Function if there is no Ongoing Event
        if not is_event_active: return

        # If the User has joined the vc, start their timer
        if after.channel == voice_channel:
            start_time[member.name] = time.now(pytz.utc)
            logger.info(f"{member} Joined the Event. Starting Logging...")
            
        # If the User left the vc, then stop their timer and add it to flight logs
        if before.channel == voice_channel:
        
            # Check if the user was previously tracked
            if member.name not in start_time: return
            
            # Calculate the flight time and add it to the member's flight hours
            elapsed_time = time.now(pytz.utc) - start_time[member.name]
            if member.name not in flight_hours: flight_hours[member.name] = elapsed_time
            else: flight_hours[member.name] += elapsed_time
            logger.info(f"{member.name} Left the Event. Logging Complete ({elapsed_time}).")
            logger.info(f"{member.name} Total Flight Hours - {flight_hours[member.name]}.")
            logger.info(f"flight_hours now has a total of {len(flight_hours)} members.")
            
            # Remove the user from the tracking dictionary
            del start_time[member.name]
    
    except Exception as e: logger.error(e)
    
    
@bot.event
async def on_scheduled_event_update(before, after):
    """
    Description:
        This bot event function monitors changes made to scheduled events, specifically
        the status. If the status changes to active, then the event has started so the flag
        is enabled. Likewise the flag is disabled when the status changes to ended.
    
    Arguments:
        before : The state of the scheduled event before any changes
        after  : The state of the scheduled event after any changes
        
    Returns:
        None
    """
    try:
        
        # Declare Global Variables
        global is_event_active
        global voice_channel
        global flight_hours
        global start_time

        # Set Event Active Status to True if Event is Active
        if after.status == EventStatus.active:
            logger.info(f"Starting Flight Logging for Event '{after.name}'.")
            is_event_active = True
            voice_channel = after.channel
            
            # Log any Members who were already in vc
            log_vc_members(after.channel)
                
        # Set Event Active Status to False if Event has Ended & Update Flight Hours
        if after.status == EventStatus.ended:
            logger.info(f"Ending Flight Logging for Event '{after.name}'.")
            is_event_active = False
            voice_channel = None
            
            # Update Flight Hours
            update_flight_hours()
            
    except Exception as e: logger.error(e)
    

def log_vc_members(channel):
    """
    Description:
        This helper function logs any members who may have already been in the vc prior
        to the start of the event to avoid any edge cases.
    
    Arguments:
        channel : The voice channel that the members are in
        
    Returns:
        None
    """
    try:
        
        # Declare Global Variables
        global flight_hours
        global start_time

        # Start the Flight Logger For every member in the channel
        for member in channel.members:
            start_time[member.name] = time.now(pytz.utc)
            logger.info(f"{member} Joined the Event. Starting Logging...")
    
    except Exception as e: logger.error(e)
    
    
def update_flight_hours():
    """
    Description:
        This helper function calculates and updates the flight hours of the remaining
        members who joined the event in case the event ends before they leave.
    
    Arguments:
        None
        
    Returns:
        None
    """
    try:
    
        # Declare Global Variables
        global flight_hours
        global start_time
    
        # For every member who joined the event
        for member_name in list(start_time.keys()):
        
            # Increment their flight hours with the elapsed time
            elapsed_time = time.now(pytz.utc) - start_time[member_name]
            if member_name not in flight_hours: flight_hours[member_name] = elapsed_time
            else: flight_hours[member_name] += elapsed_time
            logger.info(f"{member_name} Left the Event. Logging Complete ({elapsed_time}).")
            logger.info(f"{member_name} Total Flight Hours - {flight_hours[member_name]}.")
            logger.info(f"flight_hours now has a total of {len(flight_hours)} members.")
            
            # Delete that member instance from start times
            del start_time[member_name]
        
    except Exception as e: logger.error(e)
