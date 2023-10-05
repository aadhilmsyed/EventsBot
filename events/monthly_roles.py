# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import from Local Files
from config import flight_hours, roles

# Import Other Necessary Libraries
import datetime
import json
import csv

# Function to assign roles based on flight hours
async def assign_roles(ctx, member : discord.Member):
    """
    Description:
        This function acts as a helper function for the role updates. Given a member, it identifies the
        number of flight hours this member has flown and assigns their roles accordingly.
        
    Arguments:
        ctx : The command context object
        member (discord.Member) : The member that is pending role updates
        
    Returns:
        None
    """
    try:
        # Declare Global Variables
        global flight_hours
        global roles
        
        # If the Member is not a bot, assign the 'Member' role; else assign 'Bot'
        if not member.bot: await member.add_roles(discord.utils.get(member.guild.roles, id = 844635858501500988)) # TODO: Change to GE Member Role
        else:              await member.add_roles(discord.utils.get(member.guild.roles, id = 553935416496226305)) # TODO: Change to GE Member Role
        
        # Remove roles from previous role update
        for role_id in list(roles.keys()):
            await member.remove_roles(discord.utils.get(member.guild.roles, id = role_id))
        
        # Return if the member has not logged any flight hours
        if member.name not in list(flight_hours.keys()): return
        
        # Get the number of Minutes from the Flight Time
        hours = flight_hours[member.name].total_seconds() // 3600
        
        # Assign them Roles Based on their Threshold
        for role_id, threshold in roles.items():
        
            # If the Hours Meets the Threshold, Assign the Role
            if hours >= threshold:
                role = discord.utils.get(member.guild.roles, id = role_id)
                await member.add_roles(discord.utils.get(member.guild.roles, id = role_id))
                logger.info(f"{member.name} was assigned {role} during role updates.")
#                await ctx.send(f"{member.name} was assigned {role}.")
                break      # Prevents Multiple Role Assignments
                
    except Exception as e: logger.error(e)


# Command to update roles based on flight hours
@bot.command()
@commands.has_permissions(manage_roles = True)
async def update_roles(ctx):
    """
    Description:
        When called by an administrator, this function will iterate through every member in the server
        and update their roles by calling the assing_roles helper function
        
    Arguments:
        ctx : The context of the command
        
    Returns:
        None
    """
    
    # Update Logger Information
    logger.info(f"Server Role Updates requested by {ctx.message.author}.")
    logger.info("Starting Role Updates...")
    
    try:
        # For all members in the server, assign their new role
        for member in ctx.guild.members: await assign_roles(ctx, member)
        
        # Update Information to Channel and Logger
        await ctx.send("All Roles have been updated based on flight hours.")
        logger.info("Role Updates Complete.")
        
        # Clear the Flight Logs for the Next Month
        await clear_flight_logs(ctx)
        
    except Exception as e: logger.error(e)

@bot.command()
@commands.has_permissions(manage_roles = True)
async def clear_flight_logs(ctx):
    """
    Description:
        When called by an administrator, this function will reset all of the flight logs by removing
        every entry in the flight_hours dictionary.
        
    Arguments:
        ctx : The context of the command
        
    Returns:
        None
    """
    
    try:
        # Declare Global Variables
        global flight_hours
        
        # Export the Flight Logs to a JSON File in case we need to reload
#        filename = 'data/flight_logs.json'
#        logger.info(f"Saving flight logs to {filename}...")
#        save_flight_logs_to_file(filename)
#        logger.info(f"Flight Logs saved to {filename}.")
        
        # Clear each entry in the flight logs
        logger.info("Clearing Flight Logs...")
        for member in list(flight_hours.keys()): del flight_hours[member]
        logger.info("Flight Logs Reset.")
        await ctx.send("Flight Logs Have Been Reset.")
        
        # Check the Length of the Flight Logs to ensure full reset
        logger.info(f"flight_hours has a total of {len(flight_hours)} entries.")
    
    # Log any Errors
    except Exception as e: logger.error(e)


#@bot.command()
#@commands.has_permissions(manage_roles = True)
#async def export_flight_logs(ctx, filename):
#    """
#    Descrptions:
#        Exports data to a JSON file when bot disconnects or role udpates occur.
#
#    Arguments:
#        filename (str) : Name of the Export File
#
#    Returns:
#        None
#    """
#    try:
#
#        # Print Logger Message
#        logger.info(f"Exporting Flight Logs to {filename}...")
#
#        # Call the Helper Function to Save the Logs to a File
#        save_flight_logs_to_file(filename)
#
#        # Print Logger Message
#        logger.info("Exported Flight Logs Successfully.")
#
#    except Exception as e: logger.error(e)
#
#
#def save_flight_logs_to_file(filename):
#    """
#    Descrptions:
#        Helper function to create a flight_logs.json file and save the data there
#
#    Arguments:
#        filename (str) : Name of the Export File
#
#    Returns:
#        None
#    """
#
#    # Declare Global Variables
#    global flight_hours
#
#    # Return File in case we need to return
#    return_file = None
#
#    data = {"flight_hours": flight_hours}
#
#    # Open the JSON file and write the data to it
#    with open(filename, 'w') as json_file:
#        json.dump(data, json_file)
#        return_file = json_file
#
#    # Return the file if needed:
#    return return_file
#
#
#@bot.command()
#@commands.has_permissions(manage_roles = True)
#async def import_flight_logs(ctx, filename = 'data/flight_logs.json'):
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
#        global flight_hours
#
#        # Print Logger Message
#        logger.info(f"Importing Flight Logs from {filename}...")
#
#        # Open the JSON File and Read the Data from it
#        with open(filename, 'r') as json_file:
#            data = json.load(filename)
#            flight_hours = data.get("flight_hours", {})
#
#        # Print Logger Message
#        logger.info("Imported Flight Logs Successfully.")
#
#    except Exception as e: logger.error(e)
#
#
#@bot.command()
#@commands.has_permissions(manage_roles=True)
#async def get_flight_logs(ctx, filename='data/flight_logs.json'):
#    """
#    Description:
#        Returns a CSV file containing the flight hours to the channel.
#
#    Arguments:
#        filename (str) : Name of the JSON Flight Logs File
#
#    Returns:
#        None
#    """
#    try:
#
#        # Get the JSON Flight Logs File
#        logger.info(f"Retrieving Flight Logs from {filename}...")
#        json_file = save_flight_logs_to_file(filename)
#        data = json.load(json_file)
#        flight_hours = data.get("flight_hours", {})
#        logger.info(f"Retrieving Flight Logs from {filename}.")
#
#        # 2. Convert JSON Data to a List of Dictionaries
#        data_list = [{'member_name': key, 'flight_hours': value} for key, value in flight_hours.items()]
#
#        # 3. Write Data to a CSV File
#        csv_file_path = 'data/flight_logs.csv'
#        with open(csv_file_path, 'w', newline='') as csv_file:
#
#            # Specify the Column Names
#            fieldnames = ['member_name', 'flight_hours']
#
#            # Create a CSV writer object
#            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#
#            # Write the header row
#            csv_writer.writeheader()
#
#            # Write the data rows
#            csv_writer.writerows(data_list)
#
#        logger.info(f'Conversion from JSON to CSV completed. CSV file saved as {csv_file_path}')
#
#        # Send the CSV file as an attachment to the channel
#        with open(csv_file_path, 'rb') as file:
#            await ctx.send(file = discord.File(file))
#
#    # Log any Errors
#    except Exception as e: logger.error(e)
