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
        if hours >= threshold:
            return role_id

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
    if hasattr(update_roles, "_running") and update_roles._running:
        await ctx.send(
            "Role updates are already in progress. Please wait for them to complete."
        )
        return

    # Mark as running
    update_roles._running = True

    try:
        await ctx.send(
            f"Starting Role Updates... Please check {config.log_channel.mention} for updates."
        )
        await logger.info(f" Role Updates Requested by {ctx.message.author.mention}.")

        # Step 1: Get all rank role objects
        rank_roles = {}
        for role_id in config.roles.keys():
            role = config.guild.get_role(role_id)
            if role:
                rank_roles[role_id] = role
            else:
                await logger.error(f"Role with ID {role_id} not found in guild")

        if not rank_roles:
            await logger.error("No rank roles found! Please check your configuration.")
            return

        # Step 2: Remove all rank roles from members who have them
        logger.info("Removing roles earned during the previous month...")
        for role_id, role in rank_roles.items():

            # Get all members with the role
            members_with_role = role.members

            # Remove the role from each member
            for member in members_with_role:
                if member.bot:
                    continue  # Skip bots
                while True:
                    try:
                        await member.remove_roles(role)
                        await logger.info(
                            f"- Removed {role.name} from {member.mention}"
                        )
                        break
                    except Exception as e:
                        await asyncio.sleep(0.05)

            # Small delay to prevent rate limiting
            await asyncio.sleep(0.05)

        # Initialize role count dictionary
        role_count = {role_id: 0 for role_id in rank_roles.keys()}

        # Step 3: Add earned roles to members with flight time
        logger.info("Adding roles earned during the current month...")
        for member_id_str, minutes in flight_hours_manager.flight_hours.items():

            # Calculate earned role
            earned_role_id = calculate_earned_role(minutes)
            if not earned_role_id or earned_role_id not in rank_roles:
                continue
            earned_role = rank_roles[earned_role_id]

            try:

                # Get member object
                member = await config.guild.fetch_member(int(member_id_str))
                if not member or member.bot:
                    continue

                # Add the earned role
                await member.add_roles(earned_role)
                role_count[earned_role_id] += 1

                # Log the assignment
                h, m = divmod(minutes, 60)
                await logger.info(
                    f"- Assigned {earned_role.name} to {member.mention} ({h}h {m}m flown)"
                )

            except Exception as e:
                await logger.error(f"Failed to process member {member_id_str}: {e}")

            # Small delay to prevent rate limiting
            await asyncio.sleep(0.05)

        # Step 4: Send member summary statistics
        num_members = len(flight_hours_manager.flight_hours)
        summary = f"Role Updates Complete! A total of {num_members} logged flight time during the current month."
        for role_id, count in role_count.items():
            summary += f"\n- {rank_roles[role_id].name}: {count} members"
        await ctx.send(summary)
        await logger.info(summary)

        # Step 5: Send event summary statistics
        num_events = len(flight_hours_manager.event_history)
        summary = f"A total of {num_events} events took place during the current month."
        for event_name, members in flight_hours_manager.event_history.items():
            summary += f"\n- {event_name}: {len(members)} members"
        await ctx.send(summary)
        await logger.info(summary)

        # Step 6: Clear flight hours
        await ctx.send("Clearing Flight Hours...")
        try:
            flight_hours_manager.start_time.clear()
            flight_hours_manager.flight_hours.clear()
            flight_hours_manager.event_history.clear()
            flight_hours_manager.member_history.clear()
            flight_hours_manager.save()
            await ctx.send("Flight Hours Cleared.")
            await logger.info(
                f"Flight Hours Were Cleared by {ctx.message.author.mention}"
            )
        except Exception as e:
            await ctx.send(
                "Error clearing flight hours. Please check the logs for more information."
            )
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
    if executive_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return

    # Update logger information
    await ctx.send("Clearing Flight Hours")

    # Clear the Flight Hours Dictionary
    try:
        flight_hours_manager.start_time.clear()
        flight_hours_manager.flight_hours.clear()
        flight_hours_manager.event_history.clear()
        flight_hours_manager.member_history.clear()
    except Exception as e:
        await logger.error(e)

    # Export the updated data back to the file
    flight_hours_manager.save()

    # Update logger Information
    await ctx.send("Flight Hours Cleared.")
    await logger.info(f"Flight Hours Were Cleared by {ctx.message.author.mention}")
