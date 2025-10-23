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
        description="Your Gateway to an Enhanced Flight Simulation Experience (**Version:** v2.4)",
    )

    # Add thumbnail
    try:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    except:
        pass

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
        value="```\n!ping                    - Check bot latency\n!quack                  - Bot quacks back\n!help                   - Show this help menu\n```",
        inline=False,
    )

    # Weather commands
    embed.add_field(
        name="🌤️ **Weather Commands**",
        value="```\n!metar <ICAO>           - Get METAR weather data for airport\n!atis <ICAO>            - Get ATIS information for airport\n\nExample: !metar KSFO\n```",
        inline=False,
    )

    # Flight tracking commands
    embed.add_field(
        name="✈️ **Flight Tracking**",
        value="```\n!flighttime [member]    - View flight hours (yours or specified member)\n!leaderboard           - Monthly flight hours leaderboard\n!view_member_history   - Events you've attended this month\n!view_event_history    - List events and view attendance\n```",
        inline=False,
    )

    # Premium Economy+ commands (if user has permission)
    if (
        is_premium_economy
        or is_business_class
        or is_first_class
        or is_first_officer
        or is_captain
        or is_moderator
        or is_booster
    ):
        embed.add_field(
            name="🎮 **Premium Economy+ Commands**",
            value="```\n!dotspam [1-15]        - Spam dots (default: 10)\n```",
            inline=False,
        )

    # Business Class+ commands (if user has permission)
    if (
        is_business_class
        or is_first_class
        or is_first_officer
        or is_captain
        or is_moderator
        or is_booster
    ):
        embed.add_field(
            name="💼 **Business Class+ Commands**",
            value="```\n!echo <message>        - Bot repeats your message\n```",
            inline=False,
        )

    # First Class+ commands (if user has permission)
    if is_first_class or is_first_officer or is_captain or is_moderator or is_booster:
        embed.add_field(
            name="🥇 **First Class+ Commands**",
            value="```\n!spam <message>        - Bot spams message 5 times\n```",
            inline=False,
        )

    # Event participation info
    embed.add_field(
        name="✈️ **Event Participation**",
        value="Join voice channels during events to automatically log flight hours! Your time is tracked and roles are updated monthly based on your activity.",
        inline=False,
    )

    # Role requirements
    role_info = "**Available to all members**"
    if (
        is_premium_economy
        or is_business_class
        or is_first_class
        or is_first_officer
        or is_captain
        or is_moderator
        or is_booster
    ):
        role_info += "\n**Premium Economy+:** Dotspam command available"
    if (
        is_business_class
        or is_first_class
        or is_first_officer
        or is_captain
        or is_moderator
        or is_booster
    ):
        role_info += "\n**Business Class+:** Echo command available"
    if is_first_class or is_first_officer or is_captain or is_moderator or is_booster:
        role_info += "\n**First Class+:** Spam command available"
    if is_moderator:
        role_info += "\n**Moderator:** All commands with pinging allowed"
    if is_booster:
        role_info += "\n**Server Booster:** Access to all role-based commands"

    embed.add_field(name="🔐 **Permission Levels**", value=role_info, inline=False)

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
        value="```\n!restrict <channels>     - Add channels to restricted list\n!unrestrict <channels>   - Remove channels from restricted list\n!view_restricted_channels - List all restricted channels\n!add_event_vc <channels> - Add voice channels for event logging\n!remove_event_vc <channels> - Remove voice channels from event logging\n!view_event_vc           - List all event voice channels\n```",
        inline=False,
    )

    # Member Management
    embed.add_field(
        name="👥 **Member Management**",
        value="```\n!blacklist <member>      - Add member to command blacklist\n!whitelist <member>      - Remove member from blacklist\n!view_blacklist          - List all blacklisted members\n```",
        inline=False,
    )

    # Flight Time Management
    embed.add_field(
        name="⏱️ **Flight Time Management**",
        value="```\n!add_flight_time <member> <minutes> - Add flight time to member\n!remove_flight_time <member> <minutes> - Remove flight time from member\n!view_flight_time <member> - View member's flight time\n```",
        inline=False,
    )

    # Event Attendance Management
    embed.add_field(
        name="📋 **Event Attendance Management**",
        value="```\n!add_event_attendance <member> <event> - Add member to event attendance\n!remove_event_attendance <member> <event> - Remove member from event attendance\n!view_event_attendance <event> - View event attendance\n```",
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
        value="```\n!start_event <name>      - Start an unofficial event\n!end_event              - End the current event\n!add_event <name>       - Add event to history\n!remove_event <name>    - Remove event from history\n```",
        inline=False,
    )

    # System Management
    embed.add_field(
        name="⚙️ **System Management**",
        value="```\n!update_roles            - Update member roles based on flight hours\n!clear_flight_logs       - Clear all flight logs (monthly reset)\n```",
        inline=False,
    )

    # Footer
    embed.set_footer(text="Captain Commands | Use !mod_help for First Officer commands")

    await ctx.send(embed=embed)
