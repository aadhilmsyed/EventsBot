# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import the Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Other Necessary Libraries
import json
import pandas as pd

async def export_logfile():
    # Create an object to store the log data
    log_data = []

    # Retrieve the data from the log file
    logger.info("Retrieving Bot Logs from log_file.json...")
    with open('data/log_file.json', 'r') as log_file:
        for line in log_file:
            log_entry = json.loads(line)
            log_data.append(log_entry)

    # Export a CSV file containing the log data if there is data
    if log_data: return pd.DataFrame(log_data)
    else: return None

