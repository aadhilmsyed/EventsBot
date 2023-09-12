# Import Discord Libaries
import discord
from discord.ext import commands

# Import the Bot Object
from bot_init import bot

# Import datetime library to check latency
import datetime

# Function to Determine Successful Connection
@bot.event
async def on_ready():
    """
    Description:
        An event handler triggered when the bot successfully connects to Discord.
        This function is automatically called when the bot logs in and is ready to operate.
        It prints the bot's username and user ID to the console as a confirmation of successful login.

    Arguments:
        None

    Returns:
        None
    """
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.command()
async def ping(ctx):
    """
    Description
        Responds with the bot's current latency (ping) when issued the !ping command.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    # Calculate the latency (ping)
    latency = round(bot.latency * 1000)  # Convert to milliseconds

    # Send the latency as a message
    await ctx.send(f'Pong! Latency is {latency} ms')
