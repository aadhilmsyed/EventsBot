# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot.init import bot
from bot.logger.init import logger

# Import Other Necessary Libraries
import aiohttp
import requests
import time
import math

# Import Necessary Local Files
from config import metar_embed_thumbnail_url
#from data.keys import unsplash_api_key

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
    
    logger.info(f"'METAR' command issued by {ctx.author}.")
    
    try:
        # Perform Input Validation on the ICAO Airport Code
        if not icao_code.isalnum() or not (len(icao_code) == 4):
            await ctx.send ("Invalid ICAO code format. It must 4 alphanumeric characters.")
            return
            
        # Get the METAR data from the API
        logger.info("Connecting to external weather report API...")
        metar_data = await get_metar_info(icao_code)
        
        # Send Error Message and Exit Function if No Information was Retrieved
        if metar_data == None:
            await ctx.send(f"Unable to retrieve METAR info for {icao_code}")
            return
        else: logger.info("Successfully Retrieved METAR Information for {icao_code}.")

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
        global metar_embed_thumbnail_url
        embed.set_thumbnail(url = metar_embed_thumbnail_url)

        # Set Embed Footer
        text = "Data Provided by Aviation Weather Center API.\nImage Provided by Unsplash API."
        embed.set_footer(text = text)

        await ctx.send(embed = embed)
    
    # Log any Errors
    except Exception as e: logger.error(e)
    
    
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
    api_url = f"https://aviationweather.gov/cgi-bin/data/metar.php?ids={icao_code}&format=json"
    
    try:
        # Send a GET request to the API
        response = requests.get(api_url)

        # Return the response if the request was successful
        if response.status_code == 200: return response.json()[0]
        
        # If the request was unsuccessful, return nothing
        else: return None

    # Log any Errors
    except Exception as e: logger.error(e)


## Function to fetch an image of an airport using its ICAO code
#async def get_airport_image(icao_code : str):
#
#    # Define the query for the airport using its ICAO code
#    search_query = f"{icao_code} airport"
#
#    # Construct the URL for the Unsplash API search
#    url = f"https://api.unsplash.com/search/photos/?query={search_query}&client_id={unsplash_api_key}"
#
#    try:
#        # Send a GET request to the Unsplash API
#        response = requests.get(url)
#
#        # Check if the request was successful (status code 200)
#        if response.status_code == 200:
#            data = response.json()
#
#            # Check if there are any results
#            if 'results' in data and len(data['results']) > 0:
#                # Get the URL of the first image in the results
#                image_url = data['results'][0]['urls']['regular']
#                return image_url
#
#    # Log any Errors
#    except Exception as e: logger.error(f"An error occurred: {e}")
#
#    # Return None if no image was found
#    return None
