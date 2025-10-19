# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
from logger import logger

# Import from Local Files
from config import flight_hours_manager, config

# Import Other Necessary Libraries
import datetime
import json
import csv
import asyncio

def calculate_earned_role(minutes):
    """
    Calculate the earned role based on flight time in minutes.
    
    Args:
        minutes (int): Flight time in minutes
        
    Returns:
        int: Role ID for the earned role, or None if no role earned
    """
    if minutes == 0:
        return None
    
    # Calculate hours with grace (+1 hour)
    hours = (minutes // 60) + 1
    
    # Sort roles by threshold (highest first) to find the best role
    sorted_roles = sorted(config.roles.items(), key=lambda x: x[1], reverse=True)
    
    # Find the highest role threshold met
    for role_id, threshold in sorted_roles:
        if hours >= threshold: return role_id
    
    return None

@bot.command()
async def update_roles(ctx):
    """
    Description:
        Efficiently updates roles for all members using a role-based approach.
        This algorithm is much more efficient than the previous member-based approach.
        
    Arguments:
        ctx : The context of the command
        
    Returns:
        None
    """
    
    # Check if the message author is a captain
    executive_role = config.guild.get_role(config.captain_role_id)
    if executive_role not in ctx.message.author.roles: 
        await ctx.send("Your role is not high enough to use this command.")
        return
    
    # Check if role updates are already running
    if hasattr(update_roles, '_running') and update_roles._running:
        await ctx.send("Role updates are already in progress. Please wait for them to complete.")
        return
    
    # Mark as running
    update_roles._running = True
    
    try:
        await ctx.send(f"Starting Role Updates... Please check {config.log_channel.mention} for updates.")
        await logger.info(f" Role Updates Requested by {ctx.message.author.mention}.")
        
        # Step 1: Get all rank role objects
        rank_roles = {}
        for role_id in config.roles.keys():
            role = config.guild.get_role(role_id)
            if role:
                rank_roles[role_id] = role
                await logger.info(f"Found rank role: {role.name}")
            else:
                await logger.error(f"Role with ID {role_id} not found in guild")
        
        if not rank_roles:
            await ctx.send("No rank roles found! Please check your configuration.")
            return
        
        # Step 2: Remove all rank roles from members who have them
        await logger.info("Phase 1: Removing existing rank roles from all members...")
        total_removals = 0
        
        for role_id, role in rank_roles.items():
            members_with_role = role.members
            await logger.info(f"Removing {role.name} from {len(members_with_role)} members...")
            
            for member in members_with_role:
                if member.bot:
                    continue  # Skip bots
                    
                try:
                    await member.remove_roles(role)
                    total_removals += 1
                except discord.HTTPException as e:
                    if e.status == 429:  # Rate limited
                        await logger.error(f"Rate limited while removing {role.name}. Waiting...")
                        await asyncio.sleep(e.retry_after)
                        try:
                            await member.remove_roles(role)
                            total_removals += 1
                        except Exception as retry_error:
                            await logger.error(f"Failed to remove {role.name} from {member.mention} after retry: {retry_error}")
                    else:
                        await logger.error(f"Failed to remove {role.name} from {member.mention}: {e}")
                except Exception as e:
                    await logger.error(f"Failed to remove {role.name} from {member.mention}: {e}")
                
                # Small delay to prevent rate limiting
                await asyncio.sleep(0.05)
        
        await logger.info(f"Phase 1 Complete: Removed {total_removals} rank roles from members.")
        
        # Step 3: Add earned roles to members with flight time
        await logger.info("Phase 2: Adding earned roles to members with flight time...")
        total_additions = 0
        members_with_flight_time = 0
        
        for member_id_str, minutes in flight_hours_manager.flight_hours.items():
            if minutes == 0:
                continue
                
            members_with_flight_time += 1
            
            # Calculate earned role
            earned_role_id = calculate_earned_role(minutes)
            if not earned_role_id or earned_role_id not in rank_roles:
                continue
            
            earned_role = rank_roles[earned_role_id]
            
            # Get member object
            try:
                member = await config.guild.fetch_member(int(member_id_str))
                if not member or member.bot:
                    continue
                    
                # Add the earned role
                await member.add_roles(earned_role)
                total_additions += 1
                
                # Log the assignment
                hours = (minutes // 60) + 1
                await logger.info(f"Assigned {earned_role.name} to {member.mention} ({hours} hours earned)")
                
            except discord.HTTPException as e:
                if e.status == 429:  # Rate limited
                    await logger.error(f"Rate limited while adding roles. Waiting...")
                    await asyncio.sleep(e.retry_after)
                    try:
                        member = await config.guild.fetch_member(int(member_id_str))
                        if member and not member.bot:
                            await member.add_roles(earned_role)
                            total_additions += 1
                    except Exception as retry_error:
                        await logger.error(f"Failed to add {earned_role.name} to member {member_id_str} after retry: {retry_error}")
                else:
                    await logger.error(f"Failed to add {earned_role.name} to member {member_id_str}: {e}")
            except Exception as e:
                await logger.error(f"Failed to process member {member_id_str}: {e}")
            
            # Small delay to prevent rate limiting
            await asyncio.sleep(0.05)
        
        await logger.info(f"Phase 2 Complete: Added {total_additions} earned roles to {members_with_flight_time} members with flight time.")
        
        # Step 4: Export and summarize
        await ctx.send("Role Updates Complete!")
        await logger.info("Role Updates Complete. Now Exporting Flight Hours...")
        
        # Send the exported file to the log channel
        file_path = "data/logs/role_updates.txt"
        await flight_hours_manager.export(file_path)
        with open(file_path, "rb") as file: 
            await config.log_channel.send(file=discord.File(file, file_path))
        
        # Send summary statistics
        num_events = len(flight_hours_manager.event_history)
        num_members = len(flight_hours_manager.flight_hours)
        await logger.info(f"Summary: {num_events} events, {num_members} members logged time, {total_removals} roles removed, {total_additions} roles added.")
        
        # Step 5: Clear flight hours
        await ctx.send("Clearing Flight Hours...")
        
        try:
            flight_hours_manager.start_time.clear()
            flight_hours_manager.flight_hours.clear()
            flight_hours_manager.event_history.clear()
            flight_hours_manager.member_history.clear()
            flight_hours_manager.save()
            
            await ctx.send("Flight Hours Cleared.")
            await logger.info(f"Flight Hours Were Cleared by {ctx.message.author.mention}")
            
        except Exception as e: 
            await logger.error(f"Error clearing flight hours: {e}")
    
    finally:
        # Always clear the running flag
        update_roles._running = False
            
        
@bot.command()
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
    
    # Check if the message author is a captain
    executive_role = config.guild.get_role(config.captain_role_id)
    if executive_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Update logger information
    await ctx.send("Clearing Flight Hours");
    
    # Clear the Flight Hours Dictionary
    try:
        flight_hours_manager.start_time.clear()
        flight_hours_manager.flight_hours.clear()
        flight_hours_manager.event_history.clear()
        flight_hours_manager.member_history.clear()
        
    except Exception as e: await logger.error(e)
    
    # Export the updated data back to the file
    flight_hours_manager.save();
    
    # Update logger Information
    await ctx.send("Flight Hours Cleared."); await logger.info(f"Flight Hours Were Cleared by {ctx.message.author.mention}")
            
