# Import Discord Libraries
import discord
from discord.ext import commands

# Import the Bot Object
from bot_init import bot

# Import Necessary Local Files
from commands.random_commands import send_saw
from data import message_logs_channel

# Import Other Necessary Libraries
import os

@bot.event
async def on_message_delete(message):
    """
    Description:
        Event handler that logs deleted messages in an embed format.

    Parameters:
        message (discord.Message): The deleted message object.

    Returns:
        None
    """
    
    # Send "SAW" in response to the deleted message
    await send_saw(message.channel)
    
    # Checks if a log channel has been set
    if message_logs_channel:
    
        # Create an Embed to log the Deleted Message
        embed = discord.Embed(
            title       = "Message Deleted",
            description = f"Author: {message.author.mention}",
            color       = discord.Color.red()
        )
        
        # Display the Message in the Embed
        embed.add_field(name = "Content", value = message.content, inline = False)
        
        # Send the Embed to the Log Channel
        await message_logs_channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    """
    Description:
        Event handler that logs edited messages in an embed format.

    Parameters:
        before (discord.Message): The message before editing.
        after (discord.Message): The message after editing.

    Returns:
        None
    """
    
    # Checks if a log channel has been set
    if message_logs_channel:
    
        # Create an Embed to log the Edited Message
        embed = discord.Embed(
            title       = "Message Edited",
            description = f"Author: {before.author.mention}",
            color       = discord.Color.orange()
        )
        
        # Display the Message Edit
        embed.add_field(name = "Before", value = before.content, inline = False)
        embed.add_field(name = "After",  value = after.content,  inline = False)
        
        # Send the embed to the log channel
        await message_logs_channel.send(embed = embed)
        
async def log_purged_messages(purged_messages, purged_by):

    # Open a .txt file to save all the logged messages
    log_filename = "purged_messages.txt"
    with open(log_filename, "w", encoding="utf-8") as log_file:
        for message in purged_messages:
            log_file.write(f"{message.author.display_name}: {message.content}\n")

    # Create an embed message to log purge info
    embed = discord.Embed(
        title="Message Purge",
        description=f"{len(purged_messages)} messages purged by {purged_by.mention}",
        color=discord.Color.dark_red()
    )
    embed.add_field(name="Channel", value=ctx.channel.mention, inline=False)
    embed.add_field(name="Purged by", value=purged_by.mention, inline=False)
    embed.set_thumbnail(url=purged_by.avatar_url)

    # Attach the .txt file to the embed
    with open(log_filename, "rb") as file:
        file_data = discord.File(file, filename=log_filename)
        embed.set_file(file_data)

    # Send the embed message to the log channel
    await message_logs_channel.send(embed=embed)

    # Remove the file from the operating system once finished
    os.remove(log_filename)

@bot.command()
@commands.has_permissions(administrator = True)
async def set_message_logs_channel(ctx, channel: discord.TextChannel):
    """
    Command that allows administrators to set the log channel.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        channel (discord.TextChannel): The text channel where logs should be sent.

    Returns:
        None
    """
    
    # Set the log channel to the argument
    global message_logs_channel
    message_logs_channel = channel
    
    # Send confirmation message
    await ctx.send(f"Message Logs Channel set to {channel.mention}")
