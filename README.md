# GeoFS Events CoPilot Discord Bot

Welcome to the GeoFS Events CoPilot! 
This bot is designed to enhance the GeoFS Events Discord Server by providing useful features and functionality, such as airport METAR information retrieval, flight hour tracking automation, role assignment automation, and other member commands such as the dotspam, flight hours leaderboard, and individual flight times.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [File Structure](#file-structure)
5. [Configuration](#configuration)
6. [Contributing](#contributing)
7. [License](#license)

## Introduction

The GeoFS Events CoPilot is your trusted companion in the world of Flight Simulation at GeoFS Events. It seamlessly integrates with the GeoFS Events Discord Server, providing a suite of indispensable tools and utilities designed to enhance the virtual flight experience.

## Key Features

Here's a glimpse of what the GeoFS Events CoPilot brings to the table:

- **Airport METAR Information**: Instantly retrieve real-time METAR data for any airport, ensuring you have up-to-date weather information for your flights.

- **Flight Hour Tracking Automation**: Say goodbye to manual record-keeping. The bot automates the logging of flight hours during events, ensuring that your valuable time is not gone to waste.

- **Role Assignment Automation**: Your hard-earned flight hours are rewarded with automated role assignments by a simple command issued by the server administrators.

- **Member Commands**: Don't worry. This bot also has many commands dedicated just for the members. From dotspam to flight hours leaderboards and individual flight time tracking, this bot is designed to be compatible for public use.

## File Structure

Explain the structure of your project's files and directories. This will help users navigate your codebase.

- `events_bot.py`: The main/driver file of the program.
- `config.py`: Contains configuration settings and global variables.
- `commands` (Directory):
  - `metar.py`: Module for getting Airport METAR.
  - `member_commands.py`: Commands that can be issued by members.
  - `mod_commands.py`: Commands that can be issued by moderators.
- `data` (Directory - contains sensitive information so included in .gitignore).
- `bot` (Directory):
  - `__init__.py`: Bot initialization file, contains bot object used by the rest of the program.
  - `events.py`: Implementation of `on_ready()` and `on_disconnect()` functions.
  - `logger` (Sub-directory):
    - `__init__.py`: Logger initialization file, contains logger object used by the rest of the program.
    - `formatter.py`: Module used to convert logger information into JSON format.
    - `parser.py`: Parses JSON file to CSV for exporting.
- `events` (Directory):
  - `flight_logs.py`: Contains module for automatically logging flight hours during events.
  - `send_saw.py`: Module that sends 'SAW' on deleted messages if not in a restricted channel.
  - `monthly_roles.py`: Module that updates roles based on each member's flight hours.


## Contributing

We welcome contributions from the GeoFS community! Whether you're a developer interested in enhancing the bot's capabilities or a user with suggestions for improvements, we encourage you to get involved. If you are interested in contributing to this bot, please message `the._.pickle` on discord.

## License

The GeoFS Events CoPilot is released under the [MIT License](LICENSE). This open-source license grants you the freedom to use, modify, and distribute the bot while ensuring that proper attribution is given.

© | GeoFS Flights Channel 2023

---
