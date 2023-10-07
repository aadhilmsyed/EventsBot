# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Necessary Local Files
from config import import_restricted_channels, export_restricted_channels

# Import Other Necessary Libraries
from random import randrange as randomnumber

async def send_saw(channel, author):
    """
    Description:
        Responds with a saw to a deleted message when called by logs.message_logs.on_message_delete()

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    
    # Import the Restricted Channels List
    restricted_channels = await import_restricted_channels()

    # Return if the channel of the message is in the restricted channel
    if channel.id in restricted_channels: return
    
    # Print SAW every 1 in 3 times
    if (randomnumber(1,4) == 2):
        await channel.send("SAW")
        logger.info(f"'SAW' was sent to {channel} after message delete by {author}.")
    
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
