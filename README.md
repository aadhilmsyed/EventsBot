# GeoFS Events CoPilot Discord Bot

Welcome to the GeoFS Events CoPilot! This bot is designed to enhance the [GeoFS Events Discord Server](https://discord.gg/nCWhNgN) by providing useful features and functionality, such as airport METAR information retrieval, flight hour tracking automation, role assignment automation, and other member commands such as dotspam, flight hours leaderboards, and individual flight times.

## Table of Contents

1. [Introduction](#introduction)
2. [Key Features](#key-features)
3. [File Structure](#file-structure)
4. [Contributing](#contributing)
5. [Usage Terms](#usage-terms)

## Introduction

The GeoFS Events CoPilot is your trusted companion in the world of Flight Simulation at GeoFS Events. It seamlessly integrates with the GeoFS Events Discord Server, providing a suite of indispensable tools and utilities designed to enhance the virtual flight experience.

## Key Features

Here's a glimpse of what the GeoFS Events CoPilot brings to the table:

- **Airport METAR Information**: Instantly retrieve real-time METAR data for any airport, ensuring you have up-to-date weather information for your flights.

- **Flight Hour Tracking Automation**: Say goodbye to manual record-keeping. The bot automates the logging of flight hours during events, ensuring that your valuable time is not gone to waste.

- **Role Assignment Automation**: Your hard-earned flight hours are rewarded with automated role assignments issued by server administrators.

- **Member Commands**: Don't worry. This bot also has many commands dedicated just for the members. From dotspam to flight hours leaderboards and individual flight time tracking, this bot is designed to be compatible for public use.

- **Staff Management Tools**: Comprehensive moderation and administration commands for First Officers and Captains, including channel management, member blacklisting, and flight time management.

- **Server Booster Support**: Special privileges for server boosters with role-based command access and enhanced permissions.

- **Role-Based Command System**: Tiered command access based on flight hours and server roles (Economy Class, Premium Economy, Business Class, First Class).

- **Comprehensive Help System**: Separate help commands for members (`!help`), First Officers (`!mod_help`), and Captains (`!admin_help`).

## File Structure

Here's an overview of the project's file structure to help you navigate the codebase:

### Core Files
- `main.py`: The main entry point of the program.
- `bot.py`: Bot initialization and core event handlers.
- `config.py`: Configuration management and data persistence with environment variable support.
- `logger.py`: Logging functionality for Discord channels.

### Command Modules
- `help.py`: Help system with member, moderator, and admin help commands.
- `member_commands.py`: Commands available to all members with role-based restrictions.
- `mod_commands.py`: Commands for First Officers and Captains.
- `metar.py`: Weather information commands (METAR/ATIS).
- `monthly_roles.py`: Role management and flight hour calculations.

### Event Handling
- `flight_logs.py`: Automatic flight hour logging during events.

### Utilities
- `validation.py`: Input validation and sanitization utilities.

### Data Directory
- `/data/`: Organized data storage structure:
  - `config/`: Bot configuration files
  - `flight_hours/`: Flight hour data and backups
  - `events/`: Event history and attendance
  - `logs/`: System logs and role update history

### Documentation
- `STAFF_COMMANDS.md`: Comprehensive staff command documentation.
- `requirements.txt`: Python dependencies.

## Contributing

For contributions, please message `the._.pickle` on Discord.

## Usage Terms

This source code is provided solely for the purpose of running the GeoFS Events CoPilot Discord Bot in the context of the [GeoFS Events Discord Server](https://discord.gg/nCWhNgN). Any use, reproduction, modification, or distribution of this source code for other projects or purposes is strictly prohibited.

© GeoFS Flights Channel 2025. All Rights Reserved.

# CI Trigger Update
