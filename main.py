# Get the Token from the OS environment
import os
import sys

import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Validate required environment variables
if not TOKEN:
    print("ERROR: DISCORD_TOKEN environment variable is required!")
    print("Please create a .env file with your Discord bot token.")
    sys.exit(1)

# Environment variables are now validated in config.py during initialization
# No need to validate here since config.py will raise ValueError if any are missing

# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
from config import config

# Import Flight Logging
from flight_logs import on_scheduled_event_update, on_voice_state_update

# Import Member Commands
from help import admin_help, help, mod_help
from logger import logger
from member_commands import (
    dotspam,
    echo,
    flighttime,
    leaderboard,
    on_message_delete,
    on_reaction_remove,
    ping,
    quack,
    spam,
    view_event_history,
    view_member_history,
)
from metar import atis, metar

# Import Moderator Commands
from mod_commands import (
    add_event_attendance,
    add_event_vc,
    add_flight_time,
    blacklist,
    remove_event_attendance,
    remove_event_vc,
    remove_flight_time,
    restrict,
    unrestrict,
    view_blacklist,
    view_event_attendance,
    view_event_vc,
    view_flight_time,
    view_restricted_channels,
    whitelist,
)
from monthly_roles import clear_flight_logs, update_roles

# Start the Bot
bot.run(TOKEN)
