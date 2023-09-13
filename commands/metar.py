# Import Discord Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot_init import bot
from bot_logger import logger

# Import Other Necessary Libraries
import aiohttp
import requests

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

        # Set Embed Footer
        embed.set_footer(text="Data provided by Aviation Weather Center API")

        await ctx.send(embed = embed)
    
    # Log any Errors
    except Exception as e: logger.error(f"An error occurred: {e}")
    
"""
# Sample METAR data
metar_data = {
    'metar_id': 416157371,
    * 'icaoId': 'KSFO',
    'receiptTime': '2023-09-13 21:00:18',
    'obsTime': 1694638560,
    * 'reportTime': '2023-09-13 21:00:00',
    * 'temp': 22.2,
    * 'dewp': 14.4,
    * 'wdir': 310,
    * 'wspd': 8,
    'wgst': None,
    * 'visib': '10+',
    * 'altim': 1013,
    'slp': 1012.9,
    'qcField': 12,
    'wxString': None,
    'presTend': -1.5,
    'maxT': None,
    'minT': None,
    'maxT24': None,
    'minT24': None,
    'precip': None,
    'pcp3hr': None,
    'pcp6hr': None,
    'pcp24hr': None,
    'snow': None,
    'vertVis': None,
    'metarType': 'METAR',
    * 'rawOb': 'KSFO 132056Z 31008KT 10SM FEW006 22/14 A2991 RMK AO2 SLP129 T02220144 58015 $',
    'mostRecent': 1,
    'lat': 37.62,
    'lon': -122.366,
    'elev': 2,
    'prior': 1,
    * 'name': 'San Francisco Intl, CA, US',
    * 'clouds': [{'cover': 'FEW', 'base': 600}]
}
"""
