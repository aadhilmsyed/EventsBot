# Import Discord Python Libraries
import discord
from discord.ext import commands, tasks

# Import Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Necessary Local Files
from data.data import flight_hours, start_time
from data.data import voice_channels, scheduled_events

# Import Other Necessary Libraries
from datetime import datetime as time
import pytz

@bot.event
async def on_voice_state_update(member, before, after):

    # Exit the Function if there is no Ongoing Event
    if not is_event_active(): return

    # If the User has joined the vc, start their timer
    if after.channel and after.channel.id in voice_channels:
        start_time[member] = time.now(pytz.utc)
        logger.info(f"{member} Joined the Event. Starting Logging...")
        
    # If the User left the vc, then stop their timer and add it to flight logs
    if before.channel and before.channel.id in voice_channels:
    
        # Check if the user was previously tracked
        if member not in start_time: return
        
        # Calculate the flight time and add it to the member's flight hours
        elapsed_time =time.now(pytz.utc) - start_time[member]
        flight_hours[member] += elapsed_time
        logger.info(f"{member} Left the Event. Logging Complete ({elapsed_time}).")
        
        # Remove the user from the tracking dictionary
        del start_time[member]


# Function to check if there's an ongoing event
def is_event_active():

    # Return True if any Event is Active
    for event in scheduled_events:
        if scheduled_events[event]:
            logger.info(f"Starting Logging for Event '{event.name}'")
            return True
        
    # Return False if no Events are Active
    return False
    
    
@bot.event
async def on_scheduled_event_create(event):

    # Add the Event to the Scheduled Events List
    scheduled_events[event] = False if (time.now(pytz.utc) < event.start_time) else True
    logger.info(f"Added Event '{event.name}' to Scheduled Events.")
    
    # Log Current Members if the Event has Started
    if scheduled_events[event]: log_vc_members(event.guild)
    

@bot.event
async def on_scheduled_event_delete(event):
    
    # If the event was active, update flight logs
    if scheduled_events[event]: update_flight_hours()
    
    # Delete the Event from the Scheduled Events List
    del scheduled_events[event]
    logger.info(f"Added Event '{event.name}' to Scheduled Events.")
    

@bot.event
async def on_scheduled_event_update(before, after):
    
    # Remove the previous event from the scheduled events list
    del scheduled_events[before]
    logger.info(f"Removed Event '{before.name}' to Scheduled Events.")
    
    # Add the updated Event to the Scheduled Events List
    scheduled_events[after] = False if (time.now(pytz.utc) < after.start_time) else True
    logger.info(f"Added Event '{after.name}' to Scheduled Events.")
    
    # Log Current Members if the updated Event has Started
    if scheduled_events[after]: log_vc_members(after.guild)


@tasks.loop(minutes=5)
async def update_event_status():

    # Check every event in the scheduled_events list
    for event in scheduled_events:
    
        # If the start time for any event has passed
        if time.now(pytz.utc) > event.start_time:
        
            # Set Event Status to Active
            scheduled_events[event] = True
            logger.info(f"Starting Logging for Event '{event.name}'")
            
            # Log any Members who might Already Be in Voice Channel (Edge Case)
            log_vc_members(event.guild)
            
        # Otherwise Set Event Status to Inactive
        else: scheduled_events[event] = False

def log_vc_members(guild):

    # Check all Flight Communication Voice Channels
    for channel_id in voice_channels:
        
        # Get the Voice Channel Object
        voice_channel = guild.get_channel(channel_id)
        
        # For Every Member in the Voice CHannel
        for member in voice_channel.members:
            
            # Start their Flight Timer
            start_time[member] = time.now(pytz.utc)
            logger.info(f"{member} Joined the Event. Starting Logging...")
            

def update_flight_hours():
    
    # For every member who joined the event
    for member, start in start_time.items():
    
        # Increment their flight hours with the elapsed time
        elapsed_time = time.now(pytz.utc) - start
        flight_hours[member] += elapsed_time
        logger.info(f"{member} Left the Event. Logging Complete ({elapsed_time}).")
        
        # Delete that member instance from start times
        del start_time[member]
