# Import Discord Python Library
import discord
from discord.ext import commands

# Token to Connect to Discord API
TOKEN = 'MTE0OTUwNjI2MTExMzY0MzA4Mw.GyxGyO.xyVPFsGrMOz_izZ-0aRKNYBb0obznJsjdn1qIE'

# Define Intents & Create Bot Object
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '!', intents = intents)
