# Import Discord Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot_init import bot
from bot_logger import logger

# Import Other Necessary Libraries
import aiohttp
import requests
import time
import math

# Import Necessary Local Files
from data import MAX_REQUESTS, TIME_WINDOW, request_timestamps

@bot.command()
async def metar(ctx, icao_code : str):
    """
    Command to fetch and display METAR information for a specified airport ICAO code.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        icao_code (str): The ICAO code of the airport for which METAR information is requested.

    Returns:
        None
    """
    
    try:
        # Check the Rate Limit (Terminate with Error Msg if Usage is Too High)
        limit_exceeded, minutes, seconds = await check_rate_limit()
        if limit_exceeded:
            ctx.send(f"Rate Limit Exceeded. Please try again in {minutes} minutes and {seconds} seconds.")
            return
    
        # Perform Input Validation on the ICAO Airport Code
        if not icao_code.isalnum() or not (len(icao_code) == 4):
            await ctx.send ("Invalid ICAO code format. It must 4 alphanumeric characters.")
            return
            
        # Get the METAR data from the API
        metar_data = await get_metar_info(icao_code)
        
        # Send Error Message and Exit Function if No Information was Retrieved
        if metar_data == None:
            await ctx.send(f"Unable to retrieve METAR info for {icao_code}")
            return

        # Create an embed
        embed = discord.Embed(
            title       = f"METAR for {metar_data['icaoId']}",
            description = f"{metar_data['name']}",
            color       = discord.Color.blue()
        )

        # Add Other Fields
        embed.add_field(name = "Latitude",                  value = f"{metar_data['lat']}"          )
        embed.add_field(name = "Longitude",                 value = f"{metar_data['lon']}"          )
        embed.add_field(name = "Altitude",                  value = f"{metar_data['elev']}"         )
        embed.add_field(name = "Temperature (°C)",          value = f"{metar_data['temp']}°C"       )
        embed.add_field(name = "Dew Point (°C)",            value = f"{metar_data['dewp']}°C"       )
        embed.add_field(name = "Wind Direction",            value = f"{metar_data['wdir']}°"        )
        embed.add_field(name = "Wind Speed (KT)",           value = f"{metar_data['wspd']} KT"      )
        embed.add_field(name = "Visibility",                value = f"{metar_data['visib']}"        )
        embed.add_field(name = "Altimeter (mb)",            value = f"{metar_data['altim']} mb"     )
        embed.add_field(name = "Sea Level Pressure (mb)",   value = f"{metar_data['slp']} mb"       )
        embed.add_field(name = "Report Time",               value = f"{metar_data['reportTime']}"   )

        # Check if there are cloud cover data
        if 'clouds' in metar_data:
            clouds = metar_data['clouds']
            cloud_info = "\n".join([f"{cloud['cover']} Clouds at {cloud['base']} feet" for cloud in clouds])
            embed.add_field(name = "Cloud Cover", value = cloud_info)
            
        # Add raw METAR Info to Embed
        embed.add_field(name = "Raw METAR", value = f"{metar_data['rawOb']}")

        # Add airport picture as the thumbnail
        airport_name = metar_data['name'].split(",")[0]
        search_query = f"{airport_name} Airport"
        image_url = await get_airport_image(search_query)
        if image_url: embed.set_thumbnail(url = image_url)

        # Set Embed Footer
        text = "Data Provided by Aviation Weather Center API.\nImage Provided by Unsplash API."
        embed.set_footer(text = text)

        await ctx.send(embed = embed)
    
    # Log any Errors
    except Exception as e: logger.error(f"An error occurred: {e}")
    
    
async def get_metar_info(icao_code : str):
    """
    Description:
        Fetches METAR information for a specified airport ICAO code.

    Parameters:
        icao_code (str): The ICAO code of the airport for which METAR information is requested.

    Returns:
        dict: A dictionary containing METAR information, or None if the data couldn't be retrieved.

    Raises:
        ValueError: If the provided ICAO code is not valid (incorrect format).
        requests.RequestException: If there is an issue with the HTTP request.
    """
    
    # API URL for METAR info
    api_url = f"https://beta.aviationweather.gov/cgi-bin/data/metar.php?ids={icao_code}&format=json"
    
    try:
        # Send a GET request to the API
        response = requests.get(api_url)

        # Return the response if the request was successful
        if response.status_code == 200: return response.json()[0]
        
        # If the request was unsuccessful, return nothing
        else: return None

    # Log any Errors
    except Exception as e: logger.error(f"An error occurred: {e}")


# Function to fetch an image of an airport using its ICAO code
async def get_airport_image(icao_code : str):

    # Set up your Unsplash API credentials (replace with your own API key)
    api_key = 'S4v0a9mxDRksIXG1GsuVkh28PwXfE7kptHEqQGHqKhE'

    # Define the query for the airport using its ICAO code
    search_query = f"{icao_code} airport"

    # Construct the URL for the Unsplash API search
    url = f"https://api.unsplash.com/search/photos/?query={search_query}&client_id={api_key}"

    try:
        # Send a GET request to the Unsplash API
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            # Check if there are any results
            if 'results' in data and len(data['results']) > 0:
                # Get the URL of the first image in the results
                image_url = data['results'][0]['urls']['regular']
                return image_url

    # Log any Errors
    except Exception as e: logger.error(f"An error occurred: {e}")

    # Return None if no image was found
    return None

import time

# Function to check rate limit and record request timestamps
async def check_rate_limit():
    
    # Store the Current Time
    current_time = time.time()

    # Remove timestamps that are older than the time window
    request_timestamps[:] = [timestamp for timestamp in request_timestamps if current_time - timestamp <= TIME_WINDOW]
    
    # Define minutes and seconds variables
    minutes, seconds = 0, 0

  # Check if the rate limit is exceeded
    if len(request_timestamps) >= MAX_REQUESTS:
    
        # Calculate remaining time
        remaining_time = int((request_timestamps[user_id][0] + TIME_WINDOW) - current_time)

        # Calculate minutes and seconds
        minutes, seconds = divmod(remaining_time, 60)
    
        # Return Rate Limit Exceeded
        return True, minutes, seconds

    # Record the current request timestamp
    request_timestamps.append(current_time)
    
    # Return Rate Limit Not Exceeded
    return False, minutes, seconds
