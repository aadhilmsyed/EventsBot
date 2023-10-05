# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Define a custom help command by subclassing DefaultHelpCommand
class MyHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()

    # Override the send_help method to customize the help message
    async def send_help(ctx):
        """
        Description
            Responds with an embed describing commands that a user can issue.

        Parameters:
            ctx (discord.ext.commands.Context): The context object representing the command's context.

        Returns:
            None
        """
        try:
        
            # Update Logger Info
            logger.info(f"'ping' command was issued by {ctx.author}")
            
            # Create an embed
            embed = discord.Embed(
                title = f"GeoFS Events CoPilot",
                color = discord.Color.blue(),
                description = "Your Gateway to an Enhanced Flight Simulation Experience"
            )
            
            # Add the Member Commands
            embed.add_field(
                name = "!metar",
                value = "Retrieve the weather information for any airport with its ICAO code. Example Usage: !metar KSFO",
                inline = False
            )
            embed.add_field(
                name = "!ping",
                value = "Returns the latency. Example Usage: !ping",
                inline = False
            )
            embed.add_field(
                name = "!metar",
                value = "Spams a specified number of dots (1-20). If no number is specified, then it will dotspam 10 times. Example Usage: !dotspam 15",
                inline = False
            )
            embed.add_field(
                name = "!flighttime",
                value = "Retrieve the amount of flight hours you have logged. Example Usage: !flighttime",
                inline = False
            )
            embed.add_field(
                name = "!leaderboard",
                value = "Checkout who has the most flight hours logged for the current month. Example Usage: !leaderboard",
                inline = False
            )
            embed.add_field(
                name = "Event Participation.",
                value = "By participating in our events, you can increase your flight hours. At the end of each month, roles will be udpated to reflect flight activity, so make sure to join us whenever you can. We are thrilled to have you here at GeoFS Events, and we hope you enjoy your time here. :)",
                inline = False
            )
            
            # Set the server logo as the embed thumbnail
            embed.set_thumbnail(url = ctx.guild.icon.url)
            
            # Set footnote
            embed.set_footer(text = "Developed Proudly by GeoFS Flights Channel (the._.pickle)")
            
            # Send the latency as a message
            await ctx.send(embed = embed)
            
        # Log any Errors
        except Exception as e: logger.error(e)

# Set the bot help command to my class
bot.help_command = MyHelpCommand()