# Get the Token from the OS environment
import os
import random
import sys
import time

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
from discord.errors import HTTPException
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
from config import config

# Import Flight Logging
from flight_logs import on_scheduled_event_update, on_voice_state_update

# Import Member Commands
from help import admin_help, help, lh_help, mod_help
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

# Import Long Haul Commands
from longhauls import (
    checkin,
    clear_lh_attributes,
    clear_lh_checkin_role,
    clear_lh_security_role,
    set_lh_arrival,
    set_lh_available_business_seats,
    set_lh_available_economy_seats,
    set_lh_available_first_class_seats,
    set_lh_available_gates,
    set_lh_available_premium_economy_seats,
    set_lh_airline,
    set_lh_boarding_time,
    set_lh_date,
    set_lh_departure,
    set_lh_departure_time,
    set_lh_flight_number,
    start_lh_checkin,
    stop_lh_checkin,
    view_lh_attributes,
)

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

# Retry config for Cloudflare Error 1015 (IP rate limit / temporary ban)
MAX_RETRIES = 6
BASE_DELAY = 45
MAX_DELAY = 600  # 10 minutes cap

# Stagger first connection to avoid thundering herd on cold start
initial_delay = random.uniform(15, 45)
print(f"Waiting {initial_delay:.1f}s before first connection (reduces Cloudflare 1015 on cold start)...")
time.sleep(initial_delay)

# Start the Bot with retry logic for Cloudflare rate limiting
for attempt in range(MAX_RETRIES):
    try:
        bot.run(TOKEN)
        break
    except HTTPException as e:
        is_rate_limit = e.status == 429 or "1015" in str(getattr(e, "response", "")) or "1015" in str(e)
        if is_rate_limit and attempt < MAX_RETRIES - 1:
            delay = min(BASE_DELAY * (2**attempt), MAX_DELAY)
            print(f"Cloudflare rate limit (1015). Retrying in {delay:.0f}s (attempt {attempt + 1}/{MAX_RETRIES})...")
            time.sleep(delay)
        else:
            raise
