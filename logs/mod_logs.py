# Import Discord Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot_init import bot
from bot_logger import logger

# Import Necessary Local Files
from data import ban_reasons, kick_reasons, timeout_reasons
from data import mod_logs_channel
from logs.member_logs import on_member_left

# Function to log mod actions as an embed
async def log_mod_action(embed_title, embed_description, embed_color, user, reason = None, mod = None):

    try:
        # Check if log channel has been set
        if mod_logs_channel:
    
            # Create an Embed
            embed = discord.Embed(
                title       = embed_title,
                description = embed_description,
                color       = embed_color
            )
            embed.set_thumbnail(url = user.avatar_url)
            if mod:    embed.add_field(name = "Responsible Moderator", value = mod,    inline = False)
            if reason: embed.add_field(name = "Reason:",               value = reason, inline = False)
            
            # Send the Embed to the Log Channel
            await mod_logs_channel.send(embed = embed)
       
    # Log any Errors
    except Exception as e: logger.error(f"An error occurred: {e}")

@bot.event
async def on_member_remove(member):

    try:
        # Check if the member was banned
        async for entry in member.guild.audit_logs(limit = 1, action = discord.AuditLogAction.ban):
            if entry.target == member:
                title       = "Member Banned"
                description = f"{member} was banned by {entry.user}"
                color       = discord.Color.red()
                reason      = ban_reasons.get(member.id, None)
                await log_mod_action(title, description, color, member, entry.user, reason)
                return

        # Check if the member was kicked
        async for entry in member.guild.audit_logs(limit = 1, action = discord.AuditLogAction.kick):
            if entry.target == member:
                title       = "Member Kicked"
                description = f"{member} was kicked by {entry.user}"
                color       = discord.Color.orange()
                reason      = kick_reasons.get(member.id, None)
                await log_mod_action(title, description, color, member, entry.user, reason)
                return

        # If neither banned nor kicked, pass to member_logs.on_member_left
        await on_member_left(member)
    
    # Log any Errors
    except Exception as e: logger.error(f"An error occurred: {e}")


@bot.event
async def on_member_unban(guild, user):

    try:
        title       = "Member Unbanned"
        description = f"{user} was unbanned; reason for ban below"
        color       = discord.Color.green()
        reason      = ban_reasons.get(member.id, None)
        await log_mod_action(title, description, color, user, reason)
       
    # Log any Errors
    except Exception as e: logger.error(f"An error occurred: {e}")

@bot.event
async def on_member_timeout(member):

    try:
        title       = "Member Timed Out"
        description = f"{member} was timed out"
        color       = discord.Color.green()
        await log_mod_action(title, description, color, user)
       
    # Log any Errors
    except Exception as e: logger.error(f"An error occurred: {e}")


@bot.command()
@commands.has_permissions(administrator=True)
async def set_mod_logs_channel(ctx, channel: discord.TextChannel):
    """
    Command that allows administrators to set the log channel for moderation actions.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        channel (discord.TextChannel): The text channel where moderation logs should be sent.

    Returns:
        None
    """
    
    # Set the log channel to the argument
    global mod_logs_channel
    mod_logs_channel = channel
    
    # Send confirmation message
    await ctx.send(f"Moderation Logs Channel set to {channel.mention}")
