# Store the Discord Bot Token
TOKEN = 'MTE0OTUwNjI2MTExMzY0MzA4Mw.GyxGyO.xyVPFsGrMOz_izZ-0aRKNYBb0obznJsjdn1qIE'

# Import Discord Libraries
import discord
from discord.ext import commands

# Import Bot Utilities Files
from bot_logger import logger
from bot_init   import bot
from bot_utils  import *
from data import *

# Import Bot Logger Files
from logs.member_logs  import *
from logs.message_logs import *
from logs.mod_logs     import *
from logs.server_logs  import *
from logs.voice_logs   import *
from logs.event_logs   import *

# Import Bot Command Files
from commands.metar           import *
from commands.member_commands import *
from commands.mod_commands    import *
from commands.random_commands import *

# Start the Bot
logger.info('Starting the bot...')
bot.run(TOKEN)

# TODO: Implement Welcome Function to Welcome New Members
# TODO: Implement Server Info Function
# TODO: Implmement Help Function
