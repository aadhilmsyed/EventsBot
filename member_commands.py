# Import Discord Python Libraries
import time
# Import Other External Libraries
from random import randrange

import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
# Import Necessary Local Files
from config import config, flight_hours_manager
from logger import logger


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)  # 5 second cooldown per user
async def dotspam(ctx, limit: int = 10):
    """
    Description:
        Responds with a spam of dots when the !dotspam command is issued

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        limit (int) : Number of times a dot should be spammed

    Returns:
        None
    """

    # Check if the message author is on the blacklist
    if str(ctx.message.author.id) in config.blacklist:
        await ctx.send("You have been blacklisted from using this command.")
        return

    # Check if user is moderator (can use freely)
    moderator_role = config.guild.get_role(config.moderator_role_id)
    is_moderator = moderator_role in ctx.message.author.roles

    # Check if user is server booster
    server_booster_role = config.guild.get_role(config.server_booster_role_id)
    is_booster = server_booster_role in ctx.message.author.roles

    # Check if user has required role (Premium Economy or above)
    premium_economy = config.guild.get_role(config.premium_economy_role_id)
    business_class = config.guild.get_role(config.business_class_role_id)
    first_class = config.guild.get_role(config.first_class_role_id)
    has_required_role = (
        premium_economy in ctx.message.author.roles
        or business_class in ctx.message.author.roles
        or first_class in ctx.message.author.roles
    )

    # Allow if moderator, booster, or has required role
    if not (is_moderator or is_booster or has_required_role):
        await ctx.send(
            "This command is accessible only to Premium Economy+, server boosters, or moderators."
        )
        return

    try:
        # Convert the Argument to Integer, throw Error if not an integer
        limit = int(limit)

        # Check if the user provided a valid limit
        if limit < 1 or limit > 15:
            await ctx.send("Please enter an integer value between 1 and 15.")
            return

        await ctx.message.delete()

        # Print as many times as the limit
        for _ in range(limit):
            await ctx.send(".")

    except ValueError:
        await ctx.send("Please enter an integer value between 1 and 15.")
    except commands.CommandOnCooldown as e:
        await ctx.send(
            f"This command is on cooldown. Try again in {e.retry_after:.1f} seconds."
        )
    except Exception as e:
        await logger.error(f"An error occurred in dotspam: {e}")


def expected_role(minutes):
    """
    Description
        Returns the expected role given the person's flight time for the month

    Parameters:
        minutes (int) : Flight Time in minutes

    Returns:
        str: The expected role based on flight time
    """

    if minutes > (config.roles[989232534313369630] * 60):
        return "First Class"
    elif minutes > (config.roles[1110680241569017966] * 60):
        return "Business Class"
    elif minutes > (config.roles[1110680332879011882] * 60):
        return "Premium Economy"
    elif minutes > (config.roles[1112981412191146004] * 60):
        return "Economy Class"
    else:
        return "Member"


@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)  # 3 second cooldown per user
async def flighttime(ctx, member: discord.Member = None):
    """
    Description
        Returns the flight time of the command message author

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    try:
        flight_time = flight_hours_manager.flight_hours.copy()

        # Retrieve the message author as the member name
        if member is None:
            member = ctx.message.author

        # Check if the member is a bot
        if member.bot:
            await ctx.send("Bots don't have flight time.")
            return

        # Check if member has roles to avoid errors
        if not member.roles:
            embed_color = discord.Color.default()
        else:
            highest_role = max(member.roles, key=lambda role: role.position)
            embed_color = highest_role.color

        # Check if the member has flight hours recorded
        hours, minutes = 0, 0
        if str(member.id) in flight_time.keys():
            hours, minutes = divmod(flight_time[str(member.id)], 60)

        # Format flight hours as a string
        flight_time_str = f"{int(hours)} hours {int(minutes)} minutes"

        # Create an embed
        embed = discord.Embed(
            title=f"Flight Time for {member.display_name}", color=embed_color
        )
        embed.add_field(name="Current Flight Hours", value=flight_time_str)
        embed.add_field(
            name="Expected Role", value=expected_role((hours * 60 + minutes))
        )

        # Safely get avatar URL
        try:
            avatar_url = (
                member.avatar.url
                if member.avatar
                else "https://sm.mashable.com/mashable_me/seo/default/discord_4r4y.jpg"
            )
        except:
            avatar_url = (
                "https://sm.mashable.com/mashable_me/seo/default/discord_4r4y.jpg"
            )

        embed.set_thumbnail(url=avatar_url)

        await ctx.send(embed=embed)

    except Exception as e:
        await logger.error(f"An error occurred in flighttime: {e}")
        await ctx.send(
            "An error occurred while retrieving flight time. Please try again later."
        )


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)  # 10 second cooldown per user
async def leaderboard(ctx):
    """
    Description
        Responds with leaderboard of members with the highest flight times

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    try:
        flight_time = flight_hours_manager.flight_hours.copy()

        # Sort the Dictionary by Highest flight hours
        sorted_flight_hours = dict(
            sorted(flight_time.items(), key=lambda item: item[1], reverse=True)
        )

        # Convert the sorted dictionary items into a list of tuples
        sorted_items = list(sorted_flight_hours.items())

        # Display the top 10 values
        limit = min(10, len(sorted_items))

        # Print No Members Found if Limit is 0
        if limit == 0:
            await ctx.send("There are currently no people on the leaderboard.")
            return

        # Create the embed
        embed = discord.Embed(
            title="Flight Time Leaderboard",
            color=discord.Color.blue(),
            description="Members with the Highest Flight Hours in GeoFS Events",
        )

        # Set the server logo as the embed thumbnail
        embed.set_thumbnail(url=ctx.guild.icon.url)

        # For every member
        for i, (member_id, flight_time) in enumerate(sorted_items[:limit], start=1):

            # Calculate the Flight Hours
            hours, minutes = divmod(flight_time, 60)
            flight_time_str = f"{int(hours)} hours {int(minutes)} minutes"

            # Add the Information to the Embed
            try:
                member = await bot.fetch_user(member_id)
                member_name = member.name if member else f"Unknown User ({member_id})"
            except:
                member_name = f"Unknown User ({member_id})"

            embed.add_field(
                name=f"#{i}: {member_name}", value=flight_time_str, inline=False
            )

        # Send the Embed
        await ctx.send(embed=embed)

    except Exception as e:
        await logger.error(f"An error occurred in leaderboard: {e}")


@bot.event
async def on_message_delete(message):
    """
    Description:
        Sends "SAW" to the channel when a message is deleted if the channel is not a restricted channel

    Parameters:
        message (discord.Message): The deleted message object.

    Returns:
        None
    """

    # Don't send "SAW" if the channel is a restricted channel
    if message.channel.id in config.restricted_channels:
        return

    # if the message is a bot command, then ignore
    if message.content.split(" ")[0] == "!echo":
        return

    # Otherwise send "SAW" for every one in three messages
    try:
        if randrange(1, 4) == 1:
            await message.channel.send("SAW")
    except Exception as e:
        await logger.error(f"An error occurred in on_message_delete: {e}")


@bot.event
async def on_reaction_remove(reaction, user):
    """
    Description:
        Sends "SAW" to the channel when a reaction is removed if the channel is not a restricted channel

    Parameters:
        reaction (discord.Reaction): The deleted reaction
        user (discord.User): The user who sent the reaction

    Returns:
        None
    """

    # Don't send "SAW" if the channel is a restricted channel
    if reaction.message.channel.id in config.restricted_channels:
        return

    # Otherwise send "SAW" for every one in three messages
    try:
        if randrange(1, 4) == 1:
            await reaction.message.channel.send("SAW")
    except Exception as e:
        await logger.error(f"An error occurred in on_reaction_add: {e}")


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)  # 2 second cooldown per user
async def ping(ctx):
    """
    Description
        Responds with the bot's current latency (ping) when issued the !ping command.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    try:
        latency = round(bot.latency * 1000)  # Convert to milliseconds
        await ctx.send(f"Pong! Latency is {latency} ms")

    except Exception as e:
        await logger.error(f"An error occurred in ping command: {e}")


@bot.command()
async def quack(ctx):
    """
    Description
        Responds with a duck whenever the quack command is called

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    try:
        await ctx.send(":duck:")
    except Exception as e:
        await logger.error(f"An error occurred in quack command: {e}")


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)  # 5 second cooldown per user
async def echo(ctx, *, message: str):
    """
    Command to repeat the input message and delete the command message.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        message (str): The message to repeat.

    Returns:
        None
    """

    # Check if the message author is on the blacklist
    if str(ctx.message.author.id) in config.blacklist:
        await ctx.send("You have been blacklisted from using this command.")
        return

    # Check if user is moderator (can use freely)
    moderator_role = config.guild.get_role(config.moderator_role_id)
    is_moderator = moderator_role in ctx.message.author.roles

    # Check if user is server booster
    server_booster_role = config.guild.get_role(config.server_booster_role_id)
    is_booster = server_booster_role in ctx.message.author.roles

    # Check if user has required role (Business Class or above)
    business_class = config.guild.get_role(config.business_class_role_id)
    first_class = config.guild.get_role(config.first_class_role_id)
    has_required_role = (
        business_class in ctx.message.author.roles
        or first_class in ctx.message.author.roles
    )

    # Allow if moderator, booster, or has required role
    if not (is_moderator or is_booster or has_required_role):
        await ctx.send(
            "This command is accessible only to Business Class+, server boosters, or moderators."
        )
        return

    # Check if the message contains a ping (only moderators can ping)
    if not is_moderator and (
        ctx.message.mentions
        or ctx.message.role_mentions
        or "@everyone" in message
        or "@here" in message
    ):
        await ctx.send("You cannot ping a role or member with the bot.")
        return

    # Delete the command message
    await ctx.message.delete()

    # Send the input message to the channel
    await ctx.send(message)


@bot.command()
async def spam(ctx, *, message: str):
    """
    Command to resend the input message 5 times and delete the command message.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        message (str): The message to repeat.

    Returns:
        None
    """

    # Check if the message author is on the blacklist
    if str(ctx.message.author.id) in config.blacklist:
        await ctx.send("You have been blacklisted from using this command.")
        return

    # Check if user is moderator (can use freely)
    moderator_role = config.guild.get_role(config.moderator_role_id)
    is_moderator = moderator_role in ctx.message.author.roles

    # Check if user is server booster
    server_booster_role = config.guild.get_role(config.server_booster_role_id)
    is_booster = server_booster_role in ctx.message.author.roles

    # Check if user has required role (First Class or above)
    first_class = config.guild.get_role(config.first_class_role_id)
    has_required_role = first_class in ctx.message.author.roles

    # Allow if moderator, booster, or has required role
    if not (is_moderator or is_booster or has_required_role):
        await ctx.send(
            "This command is accessible only to First Class+, server boosters, or moderators."
        )
        return

    # Check if the message contains a ping (only moderators can ping)
    if not is_moderator and (
        ctx.message.mentions
        or ctx.message.role_mentions
        or "@everyone" in message
        or "@here" in message
    ):
        await ctx.send("You cannot ping a role or member with the bot.")
        return

    # Delete the command message
    await ctx.message.delete()

    # Send the sanitized message to the channel
    for _ in range(5):
        await ctx.send(message)


@bot.command()
async def view_member_history(ctx, member: discord.Member = None):
    """
    Description:
        Shows all of the events that a member has attended

    Arguments:
        ctx : The command object
        member : The member to remove flight time from

    Return:
        None
    """

    # Check if the specified member is None
    if member is None:
        member = ctx.message.author

    # Check if the member is a bot
    if member.bot:
        await ctx.send("Bots don't have event history, silly!")
        return

    # Check if the member has attended at least one event
    if not flight_hours_manager.member_history:
        await ctx.send(
            f"{member.name} has not attended any events for the current month."
        )
        return
    if str(member.id) not in flight_hours_manager.member_history:
        await ctx.send(
            f"{member.name} has not attended any events for the current month."
        )
        return
    if not flight_hours_manager.member_history[str(member.id)]:
        await ctx.send(
            f"{member.name} has not attended any events for the current month."
        )
        return

    # Otherwise print all the channels
    num_events = len(flight_hours_manager.member_history[str(member.id)])
    events_str = f"## Events Attended for {member.name}\n"
    events_str += f"-# This member has attended a total of {num_events} event(s)."
    for event_name in flight_hours_manager.member_history[str(member.id)]:
        events_str += f"\n- {event_name}"
    await ctx.send(events_str)


@bot.command()
async def view_event_history(ctx, event_index: int = 0):
    """
    Description:
        Shows all of the events that a member has attended

    Arguments:
        ctx : The command object
        event_index : The index of the event to view (must be an integer)

    Return:
        None
    """

    try:
        # Validate that event_index is an integer
        event_index = int(event_index)
    except (ValueError, TypeError):
        await ctx.send("ERROR: Event index must be a valid integer.")
        return

    # Check if there have been any events in the current month
    if not flight_hours_manager.event_history:
        await ctx.send("There have not been any events in the current month.")
        return

    # Check if the event index is valid
    num_events = len(flight_hours_manager.event_history)
    if event_index < 0 or event_index > num_events:
        await ctx.send(f"ERROR: Event Index Must be Between 0 and {num_events}.")
        return

    # Get the list of all events that took place (now ordered consistently)
    events = list(flight_hours_manager.event_history.keys())

    # If the event index is 0, simply print out all of the events that happened during the current month
    if not event_index:

        # Send a message containing all of the events for the current month
        events_str = f"## List of Events in {ctx.guild.name} for the Current Month \n"
        events_str += "-# Check the attendance by passing the index of the event. (Example: !view_event_history 3)"
        for i, event_name in enumerate(events):
            events_str += f"\n{(i + 1)}. {event_name}"
        await ctx.send(events_str)
        return

    # Get the Event Name as the Index for the Event History Dictionary (now consistently ordered)
    event_name = events[(event_index - 1)]

    # Create a list of member names
    member_names = []
    for member_id in flight_hours_manager.event_history[event_name]:
        try:
            member = await bot.fetch_user(member_id)
            member_names.append(f"- {member.name}")
        except Exception as e:
            await logger.error(f"Failed to fetch member {member_id}: {e}")
            member_names.append(f"- Unknown User ({member_id})")

    # Send a message containing the people who attended the event
    attend_str = f"## Attendance for Event '{event_name}'\n"
    attend_str += f"-# This event had a total of {len(flight_hours_manager.event_history[event_name])} participant(s).\n"
    attend_str += "\n".join(member_names)
    await ctx.send(attend_str)
