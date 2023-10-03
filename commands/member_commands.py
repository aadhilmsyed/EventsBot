# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Necessary Local Files
from config import flight_hours
    
    
def calculate_hours(flight_time):
    
    hours, remainder = divmod(flight_time, 3600)
    minutes, _ = divmod(remainder, 60)
    
    return hours, minutes
    
@bot.command()
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
    
    logger.info(f"'dotspam' command issued by {ctx.author} with limit {limit}.")
    
    # Convert the Argument to Integer, throw Error if not an integer
    try: limit = int(limit)
    except ValueError:
        await ctx.send("Please enter an integer value between 1 and 20.")
        return
    
    # Check if the user provided a valid limit
    if limit < 1 or limit > 20:
        await ctx.send("Please enter an integer value between 1 and 20.")
        return
        
    # Print as many times as the limit
    for _ in range(limit): await ctx.send(".")

    
def expected_role(minutes):
    """
    Description
        Returns the expected role given the person's flight time for the month

    Parameters:
        minutes (int) : Flight Time in minutes

    Returns:
        None
    """

    if   minutes > (15 * 60): return "First Class"
    elif minutes > (10 * 60): return "Business Class"
    elif minutes > (5  * 60): return "Premium Economy"
    elif minutes > (2  * 60): return "Economy Class"
    else: return "Member"


@bot.command()
async def flighttime(ctx):
    """
    Description
        Returns the flight time of the command message author

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    
    logger.info(f"'flighttime' command was issued by {ctx.message.author}...")
    
    try:
        # Declare Global Variable
        global flight_hours
        flight_time = flight_hours.copy()
        logger.info(f"Flight Hours has a total of {len(flight_time)} members.")
        
        # Retrieve the message author as the member name
        member = ctx.message.author
        member_name = member.name
        highest_role = max(member.roles, key=lambda role: role.position)
        embed_color = highest_role.color
        
        # Declare Local Variables
        hours, minutes = 0, 0
        
        # Check if the member has flight hours recorded
        if member_name in list(flight_time.keys()):
        
            # Calculate the flight time in hours & minutes
            hours, minutes = calculate_hours(flight_time[member_name].total_seconds())
            logger.info(f"Flight Time Information for {member_name} was found ({int(hours)} h {int(minutes)} m)")
            
        else: logger.info(f"Flight Time Information for {member_name} was not found")
        
        # Format flight hours as a string
        flight_time = f"{int(hours)} hours {int(minutes)} minutes"
            
        # Create an embed
        embed = discord.Embed(title = f"Flight Time for {member_name}", color = embed_color)
        embed.add_field(name = "Current Flight Hours", value = flight_time)
        embed.add_field(name = "Expected Role", value = expected_role((hours * 60 + minutes)))
        embed.set_thumbnail(url=ctx.message.author.avatar)
        
        await ctx.send(embed = embed)
    
    except Exception as e: logger.error(e)
    

@bot.command()
async def leaderboard(ctx):
    """
    Description
        Responds with leaderboard of members with the highest flight times

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    
    logger.info(f"'leaderboard' command was issued by {ctx.author}")
    
    try:
        # Declare Global Variable
        global flight_hours
        flight_time = flight_hours.copy()
    
        # Sort the Dictionary by Highest flight hours
        logger.info("Sorting Leaderboard...")
        sorted_flight_hours = dict(sorted(flight_time.items(), key=lambda item: item[1], reverse=True))

        # Convert the sorted dictionary items into a list of tuples
        sorted_items = list(sorted_flight_hours.items())
        logger.info(f"Leaderboard has a total of {len(sorted_items)} members.")
        
        # Display the top 10 values
        limit = (10 if len(sorted_items) > 10 else len(sorted_items))
        
        # Print No Members Found if Limit is 0
        if limit == 0: await ctx.send("There are currently no people on the leaderboard."); return;
        
        #Create the embed
        embed = discord.Embed(
            title = f"Flight Time Leaderboard",
            color = discord.Color.blue(),
            description = "Members with the Highest Flight Hours in GeoFS Events"
        )
               
        # Set the server logo as the embed thumbnail
        embed.set_thumbnail(url = ctx.guild.icon.url)
        
        # For every member
        for i, (member_name, flight_time) in enumerate(sorted_items[:limit], start=1):
            
            # Calculate the Flight Hours
            hours, minutes = calculate_hours(flight_time.total_seconds())
            flight_time = f"{int(hours)} hours {int(minutes)} minutes"
            
            # Add the Information to the Embed
            embed.add_field(name = f"#{i}: {member_name}", value = flight_time, inline = False)
        
        # Send the Embed
        await ctx.send(embed=embed)
    
    # Log any Errors
    except Exception as e: logger.error(e)
    

@bot.command()
async def ping(ctx):
    """
    Description
        Responds with the bot's current latency (ping) when issued the !ping command.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    
    logger.info(f"'ping' command was issued by {ctx.author}")
    
    # Calculate the latency (ping)
    try: latency = round(bot.latency * 1000)  # Convert to milliseconds
    
    # Log any Errors
    except Exception as e: logger.error(e)

    # Send the latency as a message
    await ctx.send(f'Pong! Latency is {latency} ms')
