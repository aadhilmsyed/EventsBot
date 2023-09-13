# Import Discord Libraries
import discord
from discord.ext import commands

# Get the Bot Object from the bot_init module
from bot_init import bot

# Import Necessary Local Files
from data import member_logs_channel

@bot.event
async def on_member_join(member):
    """
    Description:
        Event handler that logs member joins in a specified channel.

    Arguments:
        member (discord.Member): The member who joined.

    Returns:
        None
    """
    
    # Check if log channel is set
    if member_logs_channel:
    
        # Create an embed for the member join log with the user's avatar
        embed = discord.Embed(
            title       = "Member Joined",
            description = f"Member: {member.mention}",
            color       = discord.Color.green()
        )
        
        embed.set_thumbnail(url = member.avatar)
        
        # Send the embed to the member logs channel
        await member_logs_channel.send(embed = embed)

async def on_member_left(member):
    """
    Description:
        Event handler that logs member leaves in a specified channel.
        Is called by logs.mod_logs.on_member_remove after checking for kick or ban

    Arguments:
        member (discord.Member): The member who left.

    Returns:
        None
    """
    
    # Check if log channel is set
    if member_logs_channel:
    
        # Create an embed for the member leave log with the user's avatar
        embed = discord.Embed(
            title       = "Member Left",
            description = f"Member: {member.mention}",
            color       = discord.Color.red()
        )
        
        embed.set_thumbnail(url = member.avatar)  # Include user's avatar in the embed
        
        # Send the embed to the member logs channel
        await member_logs_channel.send(embed = embed)
        
@bot.event
async def on_member_update(before, after):
    """
    Description:
        Event handler that logs role updates in a specified channel.

    Parameters:
        before (discord.Member): The member's state before the update.
        after (discord.Member): The member's state after the update.

    Returns:
        None
    """
    
    # Check if log channel is set
    if member_logs_channel:
    
        # Check for role updates
        if before.roles != after.roles:
        
            # Convert the Roles into a List
            added_roles   = [role for role in after.roles  if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]
            
            # List the Roll Changes in a String
            if added_roles:
                role_change_str = f"Added roles: {', '.join([role.mention for role in added_roles])}\n"
            else:
                role_change_str = ""
            if removed_roles:
                role_change_str += f"Removed roles: {', '.join([role.mention for role in removed_roles])}"
            
            # Get the Responsible Moderator through Audit Logs
            responsible_mod = await get_responsible_mod(after)
            
            # Create an embed for the role update log with the user's avatar
            embed = discord.Embed(
                title       = "Role Update",
                description = f"Member: {after.mention}",
                color       = discord.Color.blue()
            )
            
            # Add the Changed Roles, Moderator, and Avatar to the Embed
            embed.add_field(name = "Role Changes",          value = role_change_str, inline = False)
            embed.add_field(name = "Responsible Moderator", value = responsible_mod, inline = False)
            embed.set_thumbnail(url = after.avatar)  # Include user's avatar in the embed
            
            # Send the Embed Message to the Channel
            await member_logs_channel.send(embed = embed)

@bot.event
async def on_member_nickname_update(member, before, after):
    """
    Description:
        Event handler that logs nickname changes in a specified channel.

    Parameters:
        member (discord.Member): The member whose nickname changed.
        before (discord.Member): The member's state before the change.
        after (discord.Member): The member's state after the change.

    Returns:
        None
    """
    
    # Check if log channel is set
    if member_logs_channel:
    
        # Check for nickname changes
        if before.nick != after.nick:
        
            # Get the Responsible Moderator
            responsible_mod = await get_responsible_mod(member)
            
            # Create an embed for the nickname change log with the user's avatar
            embed = discord.Embed(
                title       = "Nickname Change",
                description = f"Member: {member.mention}",
                color       = discord.Color.orange()
            )
            
            # Add the Embed Attributes (Previous Name, New Name, Moderator, Avatar)
            embed.add_field(name = "Before",                value = before.nick,     inline = False)
            embed.add_field(name = "After",                 value = after.nick,      inline = False)
            embed.add_field(name = "Responsible Moderator", value = responsible_mod, inline = False)
            embed.set_thumbnail(url = member.avatar)  # Include user's avatar in the embed
            
            # Send the Embed Message to Log Channel
            await member_logs_channel.send(embed = embed)

async def get_responsible_mod(guild):
    """
    Description:
        Fetches the responsible moderator for a role update action in the server's audit logs.

    Parameters:
        guild (discord.Guild): The server (guild) where the action occurred.

    Returns:
        str: A mention of the responsible moderator.
    """
    
    # Fetch From Audit Logs
    async for entry in guild.audit_logs(limit = 1, action = discord.AuditLogAction.member_role_update):
        responsible_mod = entry.user.mention
        return responsible_mod

@bot.command()
@commands.has_permissions(administrator = True)
async def set_member_logs_channel(ctx, channel: discord.TextChannel):
    """
    Description:
        Command that allows administrators to set the member logs channel.

    Arguments:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        channel (discord.TextChannel): The text channel where member logs should be sent.

    Returns:
        None
    """
    
    # Set the Global Log Channel Variable to Argument
    global member_logs_channel
    member_logs_channel = channel
    
    # Send Confirmation Message
    await ctx.send(f"Member Logs Channel set to {channel.mention}")

# TODO: Combine Member Leave with Kick/Ban/Leave Logic in mod_logs.py
