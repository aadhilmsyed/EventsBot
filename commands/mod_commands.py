# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Necessary Local Files
from data.data import restricted_channels

@bot.command()
@commands.has_permissions(manage_channels=True)
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
        logger.info(f"{channel.mention} was added as a restricted announcement channel by {ctx.author}")
    else:
        await ctx.send(f"{channel.mention} is already a restricted announcement channel.")
        

@bot.command()
@commands.has_permissions(manage_channels=True)
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
        logger.info(f"{channel.mention} was removed as a restricted announcement channel by {ctx.author}")
    else:
        await ctx.send(f"{channel.mention} is not a restricted announcement channel.")
