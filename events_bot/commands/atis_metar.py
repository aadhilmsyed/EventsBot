# Import Discord Libraries
import discord
from discord.ext import commands

# Import Other Necessary Libraries
import aiohttp

# Initialize the bot using the bot_init module
from bot_init import bot

# Global Variable to store the aviation weather API URL
aviation_weather_api_url = "https://aviationweather.gov/adds/dataserver_current/httpparam"

async def get_weather_info(airport_icao, info_type):
    """
    Fetch METAR or ATIS information for a specified airport ICAO code.

    Parameters:
        airport_icao (str): The ICAO code of the airport for which you want weather information.
        info_type (str): The type of weather information to fetch, either 'metar' or 'atis'.

    Returns:
        str: The METAR or ATIS information for the specified airport.
    """
    
    # Set the data source or METAR or ATIS
    data_source = "metars" if info_type == "metar" else "atis"
    
    # Connect with the API to get Information
    async with aiohttp.ClientSession() as session:
        async with session.get(aviation_weather_api_url, params = {
            "dataSource":    data_source,
            "requestType":   "retrieve",
            "format":        "json",
            "stationString": airport_icao,
        }) as response: data = await response.json()


    if info_type.upper() in data["response"]:
        return data["response"][info_type.upper()]
    else:
        return f"{info_type.upper()} not available for {airport_icao}"

@bot.command()
async def atis(ctx, airport_icao: str):
    """
    Description:
        Command to get ATIS information for a specified airport ICAO code.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        airport_icao (str): The ICAO code of the airport for which you want ATIS information.

    Returns:
        None
    """
    try:
        atis_info = await get_weather_info(airport_icao, "atis")

        # Create an embed to display the ATIS information
        embed = discord.Embed(
            title=f"ATIS Information for {airport_icao}",
            color=discord.Color.green()
        )
        embed.add_field(name="ATIS", value=atis_info, inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def metar(ctx, airport_icao: str):
    """
    Description:
        Command to get METAR information for a specified airport ICAO code.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        airport_icao (str): The ICAO code of the airport for which you want METAR information.

    Returns:
        None
    """
    try:
        metar_info = await get_weather_info(airport_icao, "metar")

        # Create an embed to display the METAR information
        embed = discord.Embed(
            title=f"METAR Information for {airport_icao}",
            color=discord.Color.blue()
        )
        embed.add_field(name="METAR", value=metar_info, inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
