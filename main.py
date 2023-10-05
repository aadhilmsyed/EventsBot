# Get the Token from the OS environment
import os
TOKEN = os.environ['DISCORD_TOKEN']

# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import the Bot Module Files
from bot.init import bot
from bot.events import *
from bot.logger.init import logger

# Import the Data Module File
from config import *

# Import the Command Module Files
from commands.metar import *
from commands.member_commands import *
from commands.mod_commands import *
from commands.help import *

# Import the Events Module Files
from events.flight_logs import *
from events.send_saw import *
from events.monthly_roles import *

# Start the Bot
logger.info('Starting the bot...')
bot.run(TOKEN)
