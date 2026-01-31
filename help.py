# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
from config import config
from logger import logger


@bot.command()
async def help(ctx):
    """
    Description:
        Responds with a comprehensive embed describing all member-available commands.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """

    # Create main embed
    embed = discord.Embed(
        title="GeoFS Events CoPilot",
        color=discord.Color.blue(),
        description="Your Gateway to an Enhanced Flight Simulation Experience (**Version:** v2.4.2)",
    )

    # Add thumbnail
    try: embed.set_thumbnail(url=ctx.guild.icon.url)
    except: pass

    # Check user permissions for role-based features
    user_roles = [role.id for role in ctx.author.roles]
    is_economy_class = config.economy_class_role_id in user_roles
    is_premium_economy = config.premium_economy_role_id in user_roles
    is_business_class = config.business_class_role_id in user_roles
    is_first_class = config.first_class_role_id in user_roles
    is_first_officer = config.first_officer_role_id in user_roles
    is_captain = config.captain_role_id in user_roles
    is_moderator = config.moderator_role_id in user_roles
    is_booster = config.server_booster_role_id in user_roles

    # Basic commands
    embed.add_field(
        name="🔧 **Basic Commands**",
        value="`!ping`: Check bot latency\n`!quack`: Bot quacks back\n`!help`: Show this help menu",
        inline=False,
    )

    # Weather commands
    embed.add_field(
        name="🌤️ **Weather Commands**",
        value="`!metar <ICAO>`: Get METAR weather data for airport\n`!atis <ICAO>`: Get ATIS information for airport\n\nExample: `!metar KSFO`",
        inline=False,
    )

    # Flight tracking commands
    embed.add_field(
        name="✈️ **Flight Tracking**",
        value="`!flighttime [member]`: View flight hours (yours or specified member)\n`!leaderboard`: Monthly flight hours leaderboard\n`!view_member_history`: Events you've attended this month\n`!view_event_history`: List events and view attendance",
        inline=False,
    )

    # Long Haul Event commands
    embed.add_field(
        name="🛫 **Long Haul Events**",
        value="`!checkin`: Check in for long haul events",
        inline=False,
    )

    # Command Perks by Role (visible to all members)
    perks_text = "**Economy Class:** Basic commands only\n"
    perks_text += "**Premium Economy+:** `!dotspam [1-15]` - Spam dots (default: 10)\n"
    perks_text += "**Business Class+:** `!echo <message>` - Bot repeats your message\n"
    perks_text += "**First Class+:** `!spam <message>` - Bot spams message 5 times\n"

    embed.add_field(
        name="🎯 **Command Perks by Role**",
        value=perks_text,
        inline=False,
    )

    # Event participation info
    embed.add_field(
        name="✈️ **Event Participation**",
        value="Join voice channels during events to automatically log flight hours! Your time is tracked and roles are updated monthly based on your activity.",
        inline=False,
    )

    # Footer
    embed.set_footer(
        text="Developed by GeoFS Flights Channel | Use !mod_help for First Officer commands"
    )

    await ctx.send(embed=embed)


@bot.command()
async def mod_help(ctx):
    """
    Description:
        Responds with a comprehensive embed describing all First Officer+ commands.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """

    # Check if user has First Officer+ role
    user_roles = [role.id for role in ctx.author.roles]
    is_first_officer = config.first_officer_role_id in user_roles
    is_captain = config.captain_role_id in user_roles

    if not (is_first_officer or is_captain):
        await ctx.send("Your role is not high enough to use this command.")
        return

    # Create main embed
    embed = discord.Embed(
        title="🛡️ First Officer Commands",
        color=discord.Color.green(),
        description="Commands available to First Officers and Captains",
    )

    # Add thumbnail
    try:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    except:
        pass

    # Channel Management
    embed.add_field(
        name="📺 **Channel Management**",
        value="`!restrict <channels>`: Add channels to restricted list\n`!unrestrict <channels>`: Remove channels from restricted list\n`!view_restricted_channels`: List all restricted channels\n`!add_event_vc <channels>`: Add voice channels for event logging\n`!remove_event_vc <channels>`: Remove voice channels from event logging\n`!view_event_vc`: List all event voice channels\n",
        inline=False,
    )

    # Member Management
    embed.add_field(
        name="👥 **Member Management**",
        value="`!blacklist <member>`: Add member to command blacklist\n`!whitelist <member>`: Remove member from blacklist\n`!view_blacklist`: List all blacklisted members\n",
        inline=False,
    )

    # Flight Time Management
    embed.add_field(
        name="⏱️ **Flight Time Management**",
        value="`!add_flight_time <member> <minutes>`: Add flight time to member\n`!remove_flight_time <member> <minutes>`: Remove flight time from member\n`!view_flight_time <member>`: View member's flight time\n",
        inline=False,
    )

    # Event Attendance Management
    embed.add_field(
        name="📋 **Event Attendance Management**",
        value="`!add_event_attendance <member> <event>`: Add member to event attendance\n`!remove_event_attendance <member> <event>`: Remove member from event attendance\n`!view_event_attendance <event>`: View event attendance\n",
        inline=False,
    )

    # Long Haul Event Management Help
    embed.add_field(
        name="🛫 **Long Haul Event Management**",
        value="`!lh_help`: Long haul configuration help\n",
        inline=False,
    )

    # Footer
    embed.set_footer(
        text="First Officer Commands | Use !admin_help for Captain-only commands"
    )

    await ctx.send(embed=embed)


@bot.command()
async def admin_help(ctx):
    """
    Description:
        Responds with a comprehensive embed describing all Captain-only commands.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """

    # Check if user has Captain role
    user_roles = [role.id for role in ctx.author.roles]
    is_captain = config.captain_role_id in user_roles

    if not is_captain:
        await ctx.send("Your role is not high enough to use this command.")
        return

    # Create main embed
    embed = discord.Embed(
        title="👑 Captain Commands",
        color=discord.Color.red(),
        description="Commands available only to Captains",
    )

    # Add thumbnail
    try:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    except:
        pass

    # Event Control
    embed.add_field(
        name="🎯 **Event Control**",
        value="`!start_event <name>`: Start an unofficial event\n`!end_event`: End the current event\n`!add_event <name>`: Add event to history\n`!remove_event <name>`: Remove event from history\n",
        inline=False,
    )

    # System Management
    embed.add_field(
        name="⚙️ **System Management**",
        value="`!update_roles`: Update member roles based on flight hours\n`!clear_flight_logs`: Clear all flight logs (monthly reset)\n",
        inline=False,
    )

    # Long Haul Event Management Help
    embed.add_field(
        name="🛫 **Long Haul Event Management**",
        value="`!lh_help`: Long haul configuration help\n",
        inline=False,
    )

    # Footer
    embed.set_footer(text="Captain Commands | Use !mod_help for First Officer commands")

    await ctx.send(embed=embed)


@bot.command()
async def lh_help(ctx):
    """
    Description:
        Responds with a comprehensive embed describing all Long Haul configuration commands.
        Only accessible by First Officers and Captains.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """

    # Check if user has First Officer+ role
    user_roles = [role.id for role in ctx.author.roles]
    is_first_officer = config.first_officer_role_id in user_roles
    is_captain = config.captain_role_id in user_roles

    if not (is_first_officer or is_captain):
        await ctx.send("Your role is not high enough to use this command.")
        return

    # Create main embed
    embed = discord.Embed(
        title="🛫 Long Haul Event Configuration",
        color=discord.Color.purple(),
        description="Commands for configuring and managing long haul events",
    )

    # Add thumbnail
    try:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    except:
        pass

    # Flight Information Setup
    embed.add_field(
        name="✈️ **Flight Information Setup**",
        value="`!set_lh_departure <airport>`: Set departure airport\n`!set_lh_arrival <airport>`: Set arrival airport\n`!set_lh_airline <airline>`: Set airline name\n`!set_lh_flight_number <number>`: Set flight number\n`!set_lh_date <date>`: Set flight date\n`!set_lh_boarding_time <time>`: Set boarding time\n`!set_lh_departure_time <time>`: Set departure time\n",
        inline=False,
    )

    # Seat Configuration
    embed.add_field(
        name="🪑 **Seat Configuration**",
        value="`!set_lh_available_economy_seats <seats>`: Set economy seats (space-separated)\n`!set_lh_available_premium_economy_seats <seats>`: Set premium economy seats\n`!set_lh_available_business_seats <seats>`: Set business class seats\n`!set_lh_available_first_class_seats <seats>`: Set first class seats\n`!set_lh_available_gates <gates>`: Set available gates\n",
        inline=False,
    )

    # Event Management
    embed.add_field(
        name="🎯 **Event Management**",
        value="`!view_lh_attributes`: View current event configuration\n`!clear_lh_attributes`: Clear all event attributes\n`!start_lh_checkin`: Start the check-in process\n`!stop_lh_checkin`: Stop check-in and clear attributes\n",
        inline=False,
    )

    # Role Management
    embed.add_field(
        name="👥 **Role Management**",
        value="`!clear_lh_checkin_role`: Remove check-in role from all members\n`!clear_lh_security_role`: Remove security role from all members\n",
        inline=False,
    )

    # Setup Workflow
    embed.add_field(
        name="📋 **Recommended Setup Workflow**",
        value="1. `!set_lh_departure <airport>`\n2. `!set_lh_arrival <airport>`\n3. `!set_lh_airline <airline>`\n4. `!set_lh_flight_number <number>`\n5. `!set_lh_date <date>`\n6. `!set_lh_boarding_time <time>`\n7. `!set_lh_departure_time <time>`\n8. `!set_lh_available_economy_seats <seats>`\n9. `!set_lh_available_premium_economy_seats <seats>`\n10. `!set_lh_available_business_seats <seats>`\n11. `!set_lh_available_first_class_seats <seats>`\n12. `!set_lh_available_gates <gates>`\n13. `!start_lh_checkin`\n",
        inline=False,
    )

    # User Commands
    embed.add_field(
        name="🎫 **User Commands**",
        value="`!checkin`: Check in for the event (available to all members)\n",
        inline=False,
    )

    # Footer
    embed.set_footer(
        text="Long Haul Configuration | Use !help for general commands | Use !mod_help for other First Officer commands"
    )

    await ctx.send(embed=embed)
