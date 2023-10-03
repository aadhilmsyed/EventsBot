# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Restricted Channels List from admin_commands
from data.data import restricted_channels

# Import Other Libraries
import asyncio

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
    
async def send_saw(channel, author):
    """
    Description:
        Responds with a saw to a deleted message when called by logs.message_logs.on_message_delete()

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """

    # Return if the channel of the message is in the restricted channel
    if channel.id in restricted_channels: return
    
    # Print SAW and self-delete after 5 seconds
    sent_message = await channel.send("SAW")
    await asyncio.sleep(5)
    await sent_message.delete()
    logger.info(f"'SAW' was sent to {channel.mention} after message delete by {author}.")
    
@bot.event
async def on_message_delete(message):
    """
    Description:
        Event Handler Function that calls the send_saw function when a message is deleted.

    Parameters:
        message (discord.Message): The deleted message object.

    Returns:
        None
    """
    
    try:
        # Send "SAW" in response to the deleted message
        await send_saw(message.channel, message.author)
        
    except Exception as e:
        logger.error(e)
