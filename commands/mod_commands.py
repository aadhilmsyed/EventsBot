# Import Discord Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot_init import bot
from bot_logger import logger

# Import Necessary Local Files
from logs.message_logs import log_purged_messages
from data              import ban_reasons, kick_reasons, timeout_reasons
from data              import restricted_channels

@bot.command()
@commands.has_permissions(administrator = True)
async def add_restricted_channel(ctx, channel: discord.TextChannel):
    """
    Command to add a channel to the list of restricted announcement channels.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        channel (discord.TextChannel): The text channel to restrict.

    Returns:
        None
    """
    
    if channel.id not in restricted_channels:
        restricted_channels.append(channel.id)
        await ctx.send(f"{channel.mention} is now a restricted announcement channel.")
    else:
        await ctx.send(f"{channel.mention} is already a restricted announcement channel.")

@bot.command()
@commands.has_permissions(administrator = True)
async def remove_restricted_channel(ctx, channel: discord.TextChannel):
    """
    Command to remove a channel from the list of restricted announcement channels.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        channel (discord.TextChannel): The text channel to unrestrict.

    Returns:
        None
    """
    
    if channel.id in restricted_channels:
        restricted_channels.remove(channel.id)
        await ctx.send(f"{channel.mention} is no longer a restricted announcement channel.")
    else:
        await ctx.send(f"{channel.mention} is not a restricted announcement channel.")
        
# TODO: Implement Kick, Ban, Timeout Functions
# TODO: Implement kick_reasons, ban_reasons, timeout_reasons dictionaries
# TODO: Save all dictionaries to a database in case bot fails

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    """
    Description:
        Command to purge a specified number of messages in a channel.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        limit (int): The number of messages to purge.

    Returns:
        None
    """
    
    # Convert the Argument to Integer, throw Error if not an integer
    try: limit = int(limit)
    except ValueError:
        await ctx.send("Please specify an integer value between 1 and 500.")
        return
    
    # Check if the user provided a valid limit
    if limit <= 0 or limit > 500:
        await ctx.send("Please specify an integer value between 1 and 500.")
        return

    # Purge messages (limit + 1 to purge command message as well)
    try: purged_messages = await ctx.channel.purge(limit + 1)
    
    # Log any Errors
    except Exception as e: logger.error(f"An error occurred: {e}")
    
    # Log the Purged Messages
    try:
        await log_purged_messages(purged_messages, ctx.author.mention)
        
    # Log any Errors
    except Exception as e: logger.error(f"An error occurred: {e}")
