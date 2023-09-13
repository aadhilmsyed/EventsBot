# Import Discord Python Library
import discord
from discord.ext import commands

# Define Intents & Create Bot Object
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '!', intents = intents)
