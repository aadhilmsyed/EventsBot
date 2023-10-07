# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Necessary Local Files
from config import import_restricted_channels, export_restricted_channels
from config import import_flight_hours, export_flight_hours
from config import import_start_times, export_start_times
from config import import_event_status, export_event_status
from bot.logger.parser import export_logfile
from events.flight_logs import log_vc_members

# Import Other Necessary Libraries
import pandas as pd
import io
import datetime
from datetime import timedelta

@bot.command()
@commands.has_permissions(manage_channels=True)
async def add_restricted_channel(ctx, *channels: discord.TextChannel):
    """
    Command to add a channel to the list of restricted channels.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        *channels (discord.TextChannel): The text channels to restrict.

    Returns:
        None
    """
    try:
    
        # Import the Restricted Channels List
        restricted_channels = await import_restricted_channels()
    
        # For every channel in the argument
        for channel in channels:
        
            # Add the channel to the list if its not already there
            if channel.id not in restricted_channels:
                restricted_channels.append(channel.id)
                await ctx.send(f"{channel.mention} is now a restricted channel.")
                logger.info(f"{channel.mention} was added as a restricted channel by {ctx.author}")
            
            # Otherwise inform the user that channel is already restricted
            else: await ctx.send(f"{channel.mention} is already a restricted channel.")
                
        # Export the updated restricted channels
        await export_restricted_channels(restricted_channels)
        
    # Log any Errors:
    except Exception as e: logger.error(e)
        
        
@bot.command()
@commands.has_permissions(manage_channels=True)
async def remove_restricted_channel(ctx, *channels: discord.TextChannel):
    """
    Command to remove a channel from the list of restricted channels.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        *channels (discord.TextChannel): The text channels to unrestrict.

    Returns:
        None
    """
    try:
    
        # Import the Restricted Channels List
        restricted_channels = await import_restricted_channels()
    
        # For every channel in the argument
        for channel in channels:
        
            # Add the Channel to the list if its not already there
            if channel.id in restricted_channels:
                restricted_channels.remove(channel.id)
                await ctx.send(f"{channel.mention} is no longer a restricted channel.")
                logger.info(f"{channel.mention} was removed as a restricted channel by {ctx.author}")
                
            # Otherwise inform the caller that channel is already unrestricted
            else: await ctx.send(f"{channel.mention} is not a restricted channel.")
                
        # Export the updated restricted channels
        await export_restricted_channels(restricted_channels)
                
    # Log any Errors:
    except Exception as e: logger.error(e)


@bot.command()
@commands.has_permissions(manage_channels=True)
async def view_restricted_channels(ctx):
    """
    Command to view the list of restricted channels.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    try:
    
        # Import the Restricted Channels List
        restricted_channels = await import_restricted_channels()
        
        # Print Header Message
        await ctx.send(f"Restricted Channels in {ctx.guild.name}:")
        
        channel_list = ""
        
        # Print every channel that is restricted
        for channel_id in restricted_channels: channel_list += f"<#{channel_id}>, "
        
        # Send the list to the channel of the command context
        if channel_list: await ctx.send(channel_list)
                
        # Export the updated restricted channels
        await export_restricted_channels(restricted_channels)
                
    # Log any Errors:
    except Exception as e: logger.error(e)


@bot.command()
@commands.has_permissions(manage_channels=True)
async def check_logfile(ctx):
    """
    Command to export and send bot logs in CSV format to the current channel.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    
    try:
        # Export the log data as a DataFrame
        log_data = await export_logfile()
        
        if log_data is not None:
            # Convert the DataFrame to CSV format
            csv_data = log_data.to_csv(index=False)
            
            # Send the CSV data as a file
            await ctx.send(content="Bot Logs:", file=discord.File(
                filename="bot_logs.csv",
                fp=io.StringIO(csv_data)  # Use io.StringIO here
            ))
            logger.info("Bot Logs File was sent to {ctx.channel}")
        else:
            await ctx.send("No log data available.")
            logger.info("Bot Logs File could not be created.")
    
    except Exception as e: logger.error(e)
    

@bot.command()
@commands.has_permissions(manage_channels=True)
async def toggle_voice_channel(ctx, channel: discord.VoiceChannel = None):
    """
    Description:
        Changes/Adds/Removes the Voice Channel to Track during an Event. If no argument is specified,
        then the voice_channel is set to None. Otherwise if a channel is passed as an argument, then
        that voice channel is assigned to the variable
        
    Arguments:
        ctx : The command object
        channels (discord.TextChannel) : Channel to be Assigned as the Event Voice Channel
        
    Returns:
        None
    """
    try:
        
        # Import the Voice Channel variable
        is_event_active, voice_channel = await import_event_status()
        
        # Set the Voice Channel to the argument
        voice_channel = channel
        logger.info(f"Event Voice Channel was set to {channel} by {ctx.message.author}.")
        await ctx.send(f"Event Voice Channel was set to {channel} by {ctx.message.author}.")
    
        # Export the new Voice Channel
        await export_event_status(is_event_active, voice_channel)
    
    except Exception as e: logger.error(e)
    
    
@bot.command()
@commands.has_permissions(manage_channels=True)
async def add_flight_time(ctx, member: discord.Member, minutes: int):
    """
    Description:
        Adds a Specified amount of Flight Time in minutes for a Specified Member.
        
    Arguments:
        ctx : The command object
        member : The member to add flight time to
        minutes : The amount of flight time to be added
        
    Return:
        None
    """
    try:
        
        # Import the Flight Hours from Memory
        flight_hours = await import_flight_hours()

        # If the member is not in the flight hours dictionary, add them
        if member.name not in list(flight_hours.keys()):
            flight_hours[member.name] = timedelta(minutes = minutes)
        
        # Otherwise add the flight hours to the member directly
        else: flight_hours[member.name] += timedelta(minutes = minutes)
        
        # Send a Message to the Channel and the Logger
        await ctx.send(f"{minutes} minutes were added to {member} by {ctx.message.author}.")
        logger.info(f"{minutes} minutes were added to {member} by {ctx.message.author}.")
        
        # Export the updated Flight Hours
        await export_flight_hours(flight_hours)
    
    except Exception as e: logger.error(e)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def remove_flight_time(ctx, member: discord.Member, minutes: int):
    """
    Description:
        Removes a Specified amount of Flight Time in minutes for a Specified Member.
        
    Arguments:
        ctx : The command object
        member : The member to remove flight time from
        minutes : The amount of flight time to be removed
        
    Return:
        None
    """
    try:
    
        # Import the Flight Hours from Memory
        flight_hours = await import_flight_hours()

        # If the member is not in the flight hours dictionary, add them
        if member.name not in list(flight_hours.keys()):
            ctx.send(f"{member.name} does not have any Flight Time.")
            logger.info(f"Could Not Remove Flight Time for {member.name}.")
            return
        
        # Otherwise add the flight hours to the member directly
        flight_hours[member.name] -= timedelta(minutes = minutes)
        
        # Send a Message to the Channel and the Logger
        await ctx.send(f"{minutes} minutes were removed from {member} by {ctx.message.author}.")
        logger.info(f"{minutes} minutes were removed from {member} by {ctx.message.author}.")
    
        # Export the updated Flight Hours
        await export_flight_hours(flight_hours)
    
    except Exception as e: logger.error(e)
