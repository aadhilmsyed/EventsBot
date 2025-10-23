# Import Discord Python Libraries
import math
import os
import time

# Import Other Necessary Libraries
import aiohttp
import discord
import requests
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
# Import Necessary Local Files
from config import config
from logger import logger
from validation import validate_icao_code


@bot.command()
async def metar(ctx, icao_code: str):
    """
    Command to fetch and display METAR information for a specified airport ICAO code.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        icao_code (str): The ICAO code of the airport for which METAR information is requested.

    Returns:
        None
    """
    try:
        # Validate ICAO code input
        validated_icao = validate_icao_code(icao_code)

        # Get the METAR data from the API
        metar_data = await get_metar_info(validated_icao)

        # Send Error Message and Exit Function if No Information was Retrieved
        if metar_data is None:
            await ctx.send(f"Unable to retrieve METAR info for {validated_icao}")
            return

        # Create an embed
        embed = discord.Embed(
            title=f"METAR for {metar_data['icaoId']}",
            description=f"{metar_data['name']}",
            color=discord.Color.blue(),
        )

        # Add Other Fields with safety checks for international airports
        embed.add_field(name="Latitude", value=f"{metar_data.get('lat', 'N/A')}")
        embed.add_field(name="Longitude", value=f"{metar_data.get('lon', 'N/A')}")
        embed.add_field(name="Altitude", value=f"{metar_data.get('elev', 'N/A')}")
        embed.add_field(
            name="Temperature (°C)", value=f"{metar_data.get('temp', 'N/A')}°C"
        )
        embed.add_field(
            name="Dew Point (°C)", value=f"{metar_data.get('dewp', 'N/A')}°C"
        )
        embed.add_field(
            name="Wind Direction", value=f"{metar_data.get('wdir', 'N/A')}°"
        )
        embed.add_field(
            name="Wind Speed (KT)", value=f"{metar_data.get('wspd', 'N/A')} KT"
        )
        embed.add_field(name="Visibility", value=f"{metar_data.get('visib', 'N/A')}")
        embed.add_field(
            name="Altimeter (mb)", value=f"{metar_data.get('altim', 'N/A')} mb"
        )
        embed.add_field(
            name="Sea Level Pressure (mb)", value=f"{metar_data.get('slp', 'N/A')} mb"
        )
        embed.add_field(
            name="Report Time", value=f"{metar_data.get('reportTime', 'N/A')}"
        )

        # Check if there are cloud cover data
        if "clouds" in metar_data:
            clouds = metar_data["clouds"]
            cloud_info = "\n".join(
                [f"{cloud['cover']} Clouds at {cloud['base']} feet" for cloud in clouds]
            )
            embed.add_field(name="Cloud Cover", value=cloud_info)

        # Add raw METAR Info to Embed
        embed.add_field(name="Raw METAR", value=f"{metar_data['rawOb']}")

        # Add airport picture as the thumbnail (only if URL is valid)
        weather_thumbnail_url = os.getenv("WEATHER_THUMBNAIL_URL")
        if weather_thumbnail_url and weather_thumbnail_url.startswith(
            ("http://", "https://")
        ):
            embed.set_thumbnail(url=weather_thumbnail_url)

        # Set Embed Footer
        text = "Data Provided by Aviation Weather Center API."
        embed.set_footer(text=text)

        await ctx.send(embed=embed)

    except ValueError as e:
        await ctx.send(f"Invalid ICAO code: {e}")
        await logger.error(f"Invalid ICAO code in metar command: {e}")
    except Exception as e:
        await logger.error(f"An error occurred in metar command: {e}")


async def get_metar_info(icao_code: str):
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
    metar_base_url = os.getenv(
        "METAR_API_BASE_URL", "https://aviationweather.gov/cgi-bin/data/metar.php"
    )
    api_url = f"{metar_base_url}?ids={icao_code}&format=json"

    try:
        # Send a GET request to the API with timeout
        response = requests.get(api_url, timeout=10)

        # Return the response if the request was successful
        if response.status_code == 200:
            data = response.json()
            return data[0] if data else None

        # If the request was unsuccessful, return nothing
        else:
            return None

    # Log any Errors
    except requests.exceptions.Timeout:
        await logger.error(
            f"Timeout occurred while fetching METAR data for {icao_code}"
        )
        return None
    except requests.exceptions.RequestException as e:
        await logger.error(f"Request error occurred in get_metar_info: {e}")
        return None
    except (ValueError, KeyError, IndexError) as e:
        await logger.error(f"JSON parsing error in get_metar_info: {e}")
        return None
    except Exception as e:
        await logger.error(f"An unexpected error occurred in get_metar_info: {e}")
        return None


@bot.command()
async def atis(ctx, icao_code: str):
    """
    Command to fetch and display ATIS information for a specified airport ICAO code.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        icao_code (str): The ICAO code of the airport for which ATIS information is requested.

    Returns:
        None
    """
    try:
        # Perform Input Validation on the ICAO Airport Code
        if not icao_code.isalnum() or not (len(icao_code) == 4):
            await ctx.send(
                "Invalid ICAO code format. It must be 4 alphanumeric characters."
            )
            return

        # Check if the ICAO code is a US ICAO Code
        if not icao_code.startswith("K"):
            await ctx.send("ATIS information is only available for US airports.")
            return

        # Get the ATIS data from the API
        atis_data = await get_atis_info(icao_code.upper())

        # Send Error Message and Exit Function if No Information was Retrieved
        if atis_data is None:
            await ctx.send(f"Unable to retrieve ATIS info for {icao_code}")
            return

        # Send the ATIS information as a simple message
        await ctx.send(atis_data["datis"])

    except Exception as e:
        await logger.error(f"An error occurred in atis command: {e}")


async def get_atis_info(icao_code: str):
    """
    Description:
        Fetches ATIS information for a specified airport ICAO code.

    Parameters:
        icao_code (str): The ICAO code of the airport for which ATIS information is requested.

    Returns:
        dict: A dictionary containing ATIS information, or None if the data couldn't be retrieved.

    Raises:
        requests.RequestException: If there is an issue with the HTTP request.
    """
    # API URL for ATIS info
    atis_base_url = os.getenv("ATIS_API_BASE_URL", "https://datis.clowd.io/api")
    api_url = f"{atis_base_url}/{icao_code}"

    try:
        # Send a GET request to the API with timeout
        response = requests.get(api_url, timeout=10)

        # Return the response if the request was successful
        if response.status_code == 200:
            data = response.json()
            return data[0] if data else None

        # If the request was unsuccessful, return nothing
        else:
            return None

    # Log any Errors
    except requests.exceptions.Timeout:
        await logger.error(f"Timeout occurred while fetching ATIS data for {icao_code}")
        return None
    except requests.exceptions.RequestException as e:
        await logger.error(f"Request error occurred in get_atis_info: {e}")
        return None
    except (ValueError, KeyError, IndexError) as e:
        await logger.error(f"JSON parsing error in get_atis_info: {e}")
        return None
    except Exception as e:
        await logger.error(f"An unexpected error occurred in get_atis_info: {e}")
        return None
