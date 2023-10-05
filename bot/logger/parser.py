# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import the Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Other Necessary Libraries
import json
import pandas as pd
from collections import deque


async def export_logfile():

    # Retrieve the data from the log file
    logger.info("Retrieving Bot Logs from log_file.json")
    
    try:
    
        # Create a list to keep track of the log data
        log_data = []
    
        with open('data/log_file.json', 'r') as log_file:
        
            # Use deque to keep track of the last 500 lines
            log_queue = deque(maxlen = 500)
            
            for line in log_file:
                if line.strip():  # Check if the line is not empty
                    log_entry = json.loads(line)
                    log_queue.append(log_entry)
    
            # Convert the deque to a list
            log_data = list(log_queue)
            
        # Export a CSV file containing the last 100 log entries if there is data
        return pd.DataFrame(log_data) if log_data else None
    
    except Exception as e: logger.error(e)





