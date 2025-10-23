# Get the Token from the OS environment
import os
import dotenv
import sys

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
from logger import logger

# Import Member Commands
from help import help, mod_help, admin_help
from metar import metar, atis
from member_commands import flighttime, leaderboard
from member_commands import view_event_history, view_member_history
from member_commands import on_message_delete, on_reaction_remove
from member_commands import dotspam, ping, quack, echo, spam

# Import Moderator Commands
from mod_commands import restrict, unrestrict, view_restricted_channels
from mod_commands import add_event_vc, remove_event_vc, view_event_vc
from mod_commands import add_flight_time, remove_flight_time, view_flight_time
from mod_commands import blacklist, whitelist, view_blacklist
from mod_commands import (
    add_event_attendance,
    remove_event_attendance,
    view_event_attendance,
)

# Import Flight Logging
from flight_logs import on_scheduled_event_update, on_voice_state_update
from monthly_roles import update_roles, clear_flight_logs

# Start the Bot
bot.run(TOKEN)
