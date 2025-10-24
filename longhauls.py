import asyncio
import random

import discord
from discord.ext import commands

from bot import bot
from config import config
from logger import logger

# Global lock to prevent race conditions with long haul data
lh_lock = asyncio.Lock()


@bot.command()
async def set_lh_departure(ctx, *, airport: str):
    """
    Description:
        Set the departure airport for the long haul event
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return

    # Set the departure airport
    config.lh_mh_attributes["departure_airport"] = airport
    await ctx.send(f"Departure airport set to {airport}")
    await logger.info(
        f"Departure airport set to {airport} by {ctx.message.author.mention}"
    )

    # Save the updated configuration
    config.save()


@bot.command()
async def set_lh_arrival(ctx, *, airport: str):
    """
    Description:
        Set the arrival airport for the long haul event
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return

    # Set the arrival airport
    config.lh_mh_attributes["arrival_airport"] = airport
    await ctx.send(f"Arrival airport set to {airport}")
    await logger.info(
        f"Arrival airport set to {airport} by {ctx.message.author.mention}"
    )

    # Save the updated configuration
    config.save()


@bot.command()
async def set_lh_airline(ctx, *, airline: str):
    """
    Description:
        Set the airline for the long haul event
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return

    # Set the airline
    config.lh_mh_attributes["airline"] = airline
    await ctx.send(f"Airline set to {airline}")
    await logger.info(f"Airline set to {airline} by {ctx.message.author.mention}")

    # Save the updated configuration
    config.save()


@bot.command()
async def set_lh_flight_number(ctx, *, flight_number: str):
    """
    Description:
        Set the flight number for the long haul event
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return
        
    # Set the flight number
    config.lh_mh_attributes["flight_number"] = flight_number
    await ctx.send(f"Flight number set to {flight_number}")
    await logger.info(
        f"Flight number set to {flight_number} by {ctx.message.author.mention}"
    )

    # Save the updated configuration
    config.save()


@bot.command()
async def set_lh_date(ctx, *, date: str):
    """
    Description:
        Set the date for the long haul event
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return
        
    # Set the date
    config.lh_mh_attributes["date"] = date
    await ctx.send(f"Date set to {date}")
    await logger.info(f"Date set to {date} by {ctx.message.author.mention}")

    # Save the updated configuration
    config.save()


@bot.command()
async def set_lh_boarding_time(ctx, *, boarding_time: str):
    """
    Description:
        Set the boarding time for the long haul event
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return
        
    # Set the boarding time
    config.lh_mh_attributes["boarding_time"] = boarding_time
    await ctx.send(f"Boarding time set to {boarding_time}")
    await logger.info(
        f"Boarding time set to {boarding_time} by {ctx.message.author.mention}"
    )

    # Save the updated configuration
    config.save()


@bot.command()
async def set_lh_departure_time(ctx, *, departure_time: str):
    """
    Description:
        Set the departure time for the long haul event
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return
        
    # Set the departure time
    config.lh_mh_attributes["departure_time"] = departure_time
    await ctx.send(f"Departure time set to {departure_time}")
    await logger.info(
        f"Departure time set to {departure_time} by {ctx.message.author.mention}"
    )

    # Save the updated configuration
    config.save()


@bot.command()
async def set_lh_available_economy_seats(ctx, *, seats: str):
    """
    Description:
        Set the available economy seats for the long haul event
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return
        
    # Set the available economy seats
    async with lh_lock:
        config.lh_mh_attributes["available_economy_seats"] = seats.split(" ")
    await ctx.send(f"Available economy seats set to {seats}")
    await logger.info(
        f"Available economy seats set to {seats} by {ctx.message.author.mention}"
    )

    # Save the updated configuration
    config.save()


@bot.command()
async def set_lh_available_premium_economy_seats(ctx, *, seats: str):
    """
    Description:
        Set the available premium economy seats for the long haul event
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return
        
    # Set the available premium economy seats
    async with lh_lock:
        config.lh_mh_attributes["available_premium_economy_seats"] = seats.split(" ")
    await ctx.send(f"Available premium economy seats set to {seats}")
    await logger.info(
        f"Available premium economy seats set to {seats} by {ctx.message.author.mention}"
    )

    # Save the updated configuration
    config.save()


@bot.command()
async def set_lh_available_business_seats(ctx, *, seats: str):
    """
    Description:
        Set the available business seats for the long haul event
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return
        
    # Set the available business seats
    async with lh_lock:
        config.lh_mh_attributes["available_business_seats"] = seats.split(" ")
    await ctx.send(f"Available business seats set to {seats}")
    await logger.info(
        f"Available business seats set to {seats} by {ctx.message.author.mention}"
    )

    # Save the updated configuration
    config.save()


@bot.command()
async def set_lh_available_first_class_seats(ctx, *, seats: str):
    """
    Description:
        Set the available first class seats for the long haul event
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return
        
    # Set the available first class seats
    async with lh_lock:
        config.lh_mh_attributes["available_first_class_seats"] = seats.split(" ")
    await ctx.send(f"Available first class seats set to {seats}")
    await logger.info(
        f"Available first class seats set to {seats} by {ctx.message.author.mention}"
    )

    # Save the updated configuration
    config.save()


@bot.command()
async def set_lh_available_gates(ctx, *, gates: str):
    """
    Description:
        Set the available gates for the long haul event
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return
        
    # Set the available gates
    async with lh_lock:
        config.lh_mh_attributes["available_gates"] = gates.split(" ")
    await ctx.send(f"Available gates set to {gates}")
    await logger.info(f"Available gates set to {gates} by {ctx.message.author.mention}")

    # Save the updated configuration
    config.save()


@bot.command()
async def view_lh_attributes(ctx):
    """
    Description:
        View the current long haul event attributes
    """ 

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return
        
    # View the current long haul event attributes
    attributes = config.lh_mh_attributes
    
    # Format the response nicely
    response = "## Current Long Haul Event Attributes:\n"
    response += f"- **Departure:** {attributes['departure_airport']}\n"
    response += f"- **Arrival:** {attributes['arrival_airport']}\n"
    response += f"- **Airline:** {attributes['airline']}\n"
    response += f"- **Flight Number:** {attributes['flight_number']}\n"
    response += f"- **Date:** {attributes['date']}\n"
    response += f"- **Boarding Time:** {attributes['boarding_time']}\n"
    response += f"- **Departure Time:** {attributes['departure_time']}\n"
    
    # Add seat information
    response += f"\n**Seats Available:**\n"
    response += f"- **Economy:** {len(attributes['available_economy_seats'])} seats\n"
    response += f"- **Premium Economy:** {len(attributes['available_premium_economy_seats'])} seats\n"
    response += f"- **Business:** {len(attributes['available_business_seats'])} seats\n"
    response += f"- **First Class:** {len(attributes['available_first_class_seats'])} seats\n"
    response += f"- **Gates:** {len(attributes['available_gates'])} gates\n"
    
    # Check if response is too long for Discord (2000 char limit)
    if len(response) > 1900:  # Leave some buffer
        # Send basic info first
        basic_info = "**Current Long Haul Event Attributes:**\n"
        basic_info += f"- **Departure:** {attributes['departure_airport']}\n"
        basic_info += f"- **Arrival:** {attributes['arrival_airport']}\n"
        basic_info += f"- **Airline:** {attributes['airline']}\n"
        basic_info += f"- **Flight Number:** {attributes['flight_number']}\n"
        basic_info += f"- **Date:** {attributes['date']}\n"
        basic_info += f"- **Boarding Time:** {attributes['boarding_time']}\n"
        basic_info += f"- **Departure Time:** {attributes['departure_time']}\n"
        
        await ctx.send(basic_info)
        
        # Send seat counts
        seat_info = "**Seats Available:**\n"
        seat_info += f"- **Economy:** {len(attributes['available_economy_seats'])} seats\n"
        seat_info += f"- **Premium Economy:** {len(attributes['available_premium_economy_seats'])} seats\n"
        seat_info += f"- **Business:** {len(attributes['available_business_seats'])} seats\n"
        seat_info += f"- **First Class:** {len(attributes['available_first_class_seats'])} seats\n"
        seat_info += f"- **Gates:** {len(attributes['available_gates'])} gates\n"
        
        await ctx.send(seat_info)
    else:
        await ctx.send(response)


@bot.command()
async def clear_lh_attributes(ctx):
    """
    Description:
        Clear the current long haul event attributes
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return
        
    # Clear the current long haul event attributes
    async with lh_lock:
        for key in config.lh_mh_attributes:
            config.lh_mh_attributes[key] = "N/A"
        config.lh_mh_attributes["available_economy_seats"] = []
        config.lh_mh_attributes["available_premium_economy_seats"] = []
        config.lh_mh_attributes["available_business_seats"] = []
        config.lh_mh_attributes["available_first_class_seats"] = []
        config.lh_mh_attributes["available_gates"] = []

    await ctx.send("Long haul event attributes cleared")
    await logger.info(
        f"Long haul event attributes cleared by {ctx.message.author.mention}"
    )

    # Save the updated configuration
    config.save()


@bot.command()
async def start_lh_checkin(ctx):
    """
    Description:
        Start the check-in process for the long haul event
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return

    # Verify that the check-in process is not already started
    if config.checkin_start:
        await ctx.send("Check-in process is already started.")
        return

    # Verify that the departure airport is set
    if config.lh_mh_attributes["departure_airport"] == "N/A":
        await ctx.send(
            "Departure airport is not set. Please set the departure airport using !set_lh_departure <airport>."
        )
        return

    # Verify that the arrival airport is set
    if config.lh_mh_attributes["arrival_airport"] == "N/A":
        await ctx.send(
            "Arrival airport is not set. Please set the arrival airport using !set_lh_arrival <airport>."
        )
        return

    # Verify that the airline is set
    if config.lh_mh_attributes["airline"] == "N/A":
        await ctx.send(
            "Airline is not set. Please set the airline using !set_lh_airline <airline>."
        )
        return

    # Verify that the flight number is set
    if config.lh_mh_attributes["flight_number"] == "N/A":
        await ctx.send(
            "Flight number is not set. Please set the flight number using !set_lh_flight_number <flight_number>."
        )
        return

    # Verify that the date is set
    if config.lh_mh_attributes["date"] == "N/A":
        await ctx.send("Date is not set. Please set the date using !set_lh_date <date>.")
        return

    # Verify that the boarding time is set
    if config.lh_mh_attributes["boarding_time"] == "N/A":
        await ctx.send(
            "Boarding time is not set. Please set the boarding time using !set_lh_boarding_time <boarding_time>."
        )
        return

    # Verify that the departure time is set
    if config.lh_mh_attributes["departure_time"] == "N/A":
        await ctx.send(
            "Departure time is not set. Please set the departure time using !set_lh_departure_time <departure_time>."
        )
        return

    # Verify that the available seats are set
    if len(config.lh_mh_attributes["available_economy_seats"]) == 0:
        await ctx.send(
            "Available economy seats are not set. Please set the available economy seats using !set_lh_available_economy_seats <seats>."
        )
        return

    # Verify that the available premium economy seats are set
    if len(config.lh_mh_attributes["available_premium_economy_seats"]) == 0:
        await ctx.send(
            "Available premium economy seats are not set. Please set the available premium economy seats using !set_lh_available_premium_economy_seats <seats>."
        )
        return

    # Verify that the available business seats are set
    if len(config.lh_mh_attributes["available_business_seats"]) == 0:
        await ctx.send(
            "Available business seats are not set. Please set the available business seats using !set_lh_available_business_seats <seats>."
        )
        return

    # Verify that the available first class seats are set
    if len(config.lh_mh_attributes["available_first_class_seats"]) == 0:
        await ctx.send(
            "Available first class seats are not set. Please set the available first class seats using !set_lh_available_first_class_seats <seats>."
        )
        return

    # Verify that the available gates are set
    if len(config.lh_mh_attributes["available_gates"]) == 0:
        await ctx.send(
            "Available gates are not set. Please set the available gates using !set_lh_available_gates <gates>."
        )
        return

    # Start the check-in process
    config.checkin_start = True
    await ctx.send("Check-in process started")
    await logger.info(f"Check-in process started by {ctx.message.author.mention}")

    # Save the updated configuration
    config.save()


@bot.command()
async def stop_lh_checkin(ctx):
    """
    Description:
        Stop the check-in process for the long haul event
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return

    # Verify that the check-in process is started
    if not config.checkin_start:
        await ctx.send("Check-in process is not started.")
        return

    # Stop the check-in process
    config.checkin_start = False
    await ctx.send("Check-in process stopped")
    await logger.info(f"Check-in process stopped by {ctx.message.author.mention}")

    # Clear the long haul event attributes
    async with lh_lock:
        for key in config.lh_mh_attributes:
            config.lh_mh_attributes[key] = "N/A"
        config.lh_mh_attributes["available_economy_seats"] = []
        config.lh_mh_attributes["available_premium_economy_seats"] = []
        config.lh_mh_attributes["available_business_seats"] = []
        config.lh_mh_attributes["available_first_class_seats"] = []
        config.lh_mh_attributes["available_gates"] = []
    
    # Remove the check-in role from all members
    checkin_role = config.guild.get_role(config.lh_mh_checkin_role_id)
    for member in checkin_role.members: await member.remove_roles(checkin_role)

    # Save the updated configuration
    config.save()


@bot.command()
async def checkin(ctx):
    """
    Description:
        Checks in a Member for the Long/Medium Haul Event
        Assigns them a seat and gate from the available seats and gates
        Sends a boarding pass to the member as a DM in the form of an embed
    """

    # Verify that the check-in process is started
    if not config.checkin_start:
        await ctx.send(
            "Check-in process is not started. Please wait for the check-in process to start."
        )
        return

    # # Verify that the member is in the check-in channel
    # if ctx.channel.id != config.checkin_channel:
    #     await ctx.send("You are not in the check-in channel. Please join the check-in channel using the appropriate command.")
    #     return

    # Verify that the member is not already checked in
    checkin_role = config.guild.get_role(config.lh_mh_checkin_role_id)
    if checkin_role in ctx.message.author.roles:
        await ctx.send("You are already checked in.")
        return
    
    # Get the name, id, class, avatar, and color of the member
    name = ctx.message.author.display_name
    rewards_id = ctx.message.author.id
    class_name = "Economy Class"
    for role in ctx.message.author.roles:
        if role.id == config.first_class_role_id: class_name = "First Class"; break
        elif role.id == config.business_class_role_id: class_name = "Business Class"; break
        elif role.id == config.premium_economy_role_id: class_name = "Premium Economy"; break
    avatar = ctx.message.author.avatar.url
    color = max(ctx.message.author.roles, key=lambda role: role.position).color

    # Get the departure airport, arrival airport, airline, flight number, date, boarding time, and departure time
    departure_airport = config.lh_mh_attributes["departure_airport"]
    arrival_airport = config.lh_mh_attributes["arrival_airport"]
    airline = config.lh_mh_attributes["airline"]
    flight_number = config.lh_mh_attributes["flight_number"]
    date = config.lh_mh_attributes["date"]
    boarding_time = config.lh_mh_attributes["boarding_time"]
    departure_time = config.lh_mh_attributes["departure_time"]

    # Use lock to prevent race conditions during seat/gate assignment
    async with lh_lock:
        # Assign a gate and seat to the member
        if not config.lh_mh_attributes["available_gates"]:
            await ctx.send("Sorry, no gates are available for check-in.")
            return

        gate = random.choice(config.lh_mh_attributes["available_gates"])

        # Check if seats are available for the member's class
        if class_name == "First Class" and not config.lh_mh_attributes["available_first_class_seats"]:
            class_name = "Business Class"
        if class_name == "Business Class" and not config.lh_mh_attributes["available_business_seats"]:
            class_name = "Premium Economy"
        if class_name == "Premium Economy" and not config.lh_mh_attributes["available_premium_economy_seats"]:
            class_name = "Economy Class"
        if class_name == "Economy Class" and not config.lh_mh_attributes["available_economy_seats"]:
            await ctx.send(f"{ctx.message.author.mention}, No seats are available for check-in. Please contact a first officer to be assigned a seat.")
            return

        # Assign seat based on class
        if class_name == "First Class": 
            seat = random.choice(config.lh_mh_attributes["available_first_class_seats"])
            config.lh_mh_attributes["available_first_class_seats"].remove(seat)
        elif class_name == "Business Class": 
            seat = random.choice(config.lh_mh_attributes["available_business_seats"])
            config.lh_mh_attributes["available_business_seats"].remove(seat)
        elif class_name == "Premium Economy": 
            seat = random.choice(config.lh_mh_attributes["available_premium_economy_seats"])
            config.lh_mh_attributes["available_premium_economy_seats"].remove(seat)
        else: 
            seat = random.choice(config.lh_mh_attributes["available_economy_seats"])
            config.lh_mh_attributes["available_economy_seats"].remove(seat)
        
        # Remove gate immediately
        config.lh_mh_attributes["available_gates"].remove(gate)

    # Create a boarding pass embed
    boarding_pass_embed = discord.Embed(
        title=class_name,
        description=airline,
        color=color if color else discord.Color.blue(),
    )
    boarding_pass_embed.set_thumbnail(url=avatar)
    boarding_pass_embed.add_field(name="Departure Airport", value=departure_airport)
    boarding_pass_embed.add_field(name="Arrival Airport", value=arrival_airport)
    boarding_pass_embed.add_field(name="Flight Number", value=flight_number)
    boarding_pass_embed.add_field(name="Date", value=date)
    boarding_pass_embed.add_field(name="Boarding Time", value=boarding_time)
    boarding_pass_embed.add_field(name="Departure Time", value=departure_time)
    boarding_pass_embed.add_field(name="Gate", value=gate)
    boarding_pass_embed.add_field(name="Seat", value=seat)
    boarding_pass_embed.add_field(name="Rewards ID", value=rewards_id)
    boarding_pass_embed.set_footer(text=f"Generated by GeoFS Events CoPilot ({config.guild.id})")

    # Send the boarding pass embed to the member in DMs
    try: 
        await ctx.message.author.send(embed=boarding_pass_embed)
    except discord.Forbidden:
        # If DM fails, we need to restore the seat and gate
        async with lh_lock:
            # Restore the seat
            if class_name == "First Class": 
                config.lh_mh_attributes["available_first_class_seats"].append(seat)
            elif class_name == "Business Class": 
                config.lh_mh_attributes["available_business_seats"].append(seat)
            elif class_name == "Premium Economy": 
                config.lh_mh_attributes["available_premium_economy_seats"].append(seat)
            else: 
                config.lh_mh_attributes["available_economy_seats"].append(seat)
            
            # Restore the gate
            config.lh_mh_attributes["available_gates"].append(gate)
        
        await ctx.send(f"{ctx.message.author.mention}, please enable DMs to continue check-in.")
        return
    await logger.info(f"Boarding pass sent to {ctx.message.author.mention}.")

    # Add the member to the check-in role
    await ctx.message.author.add_roles(checkin_role)
    await logger.info(f"{ctx.message.author.mention} was assigned the check-in role for the long haul event.")

    # Save the updated configuration
    config.save()

    # Send a message to the channel
    msg = f"{ctx.message.author.mention}, your boarding pass has been sent to your DMs. "
    msg += "Proceed to Security Check with your boarding pass. Have a safe flight!"
    await ctx.send(msg)
    
@bot.command()
async def clear_lh_checkin_role(ctx):
    """
    Description:
        Clear the check-in role from all members
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return

    # Clear the check-in role from all members
    checkin_role = config.guild.get_role(config.lh_mh_checkin_role_id)
    msg = "The following members have been removed from the check-in role:\n"
    for member in checkin_role.members:
        await member.remove_roles(checkin_role)
        msg += f"- {member.mention}\n"
    await logger.info(msg)

    # Save the updated configuration
    config.save()

@bot.command()
async def clear_lh_security_role(ctx):
    """
    Description:
        Clear the security role from all members
    """

    # Verify that the member is a first officer
    manager_role = config.guild.get_role(config.first_officer_role_id)
    if manager_role not in ctx.message.author.roles:
        await ctx.send("Your role is not high enough to use this command.")
        return

    # Clear the security role from all members
    security_role = config.guild.get_role(config.lh_mh_security_role_id)
    msg = "The following members have been removed from the security role:\n"
    for member in security_role.members:
        await member.remove_roles(security_role)
        msg += f"- {member.mention}\n"
    await logger.info(msg)

    # Save the updated configuration
    config.save()