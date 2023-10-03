# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import the Bot Module Files
from bot.init import bot
from bot.events import *
from bot.logger.init import logger

# Import the Data Module File
from data.token import TOKEN
from data.data import *

# Import the Command Module Files
from commands.metar import *
from commands.member_commands import *
from commands.mod_commands import *
from commands.random_commands import *

# Start the Bot
logger.info('Starting the bot...')
bot.run(TOKEN)
