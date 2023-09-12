# GeoFS Events Discord Bot

Welcome to the GeoFS Events Discord Bot repository! 
This bot is designed to enhance the GeoFS Events Discord Server by providing useful features and functionality.

## Directory Structure

- **events_bot.py**: Main Driver File
- **bot_init.py**: Initializes and Creates the Bot Object
- **bot_utils.py**: Functions that Check That the Bot Is Running Correctly
- **data.py**: File That Contains Important Variables Used by Other Files
- Commands (Directory):
  - **atis_metar.py**: Uses an API to Get ATIS and METAR Info and Sends It to Discord When Called
  - **member_commands.py**: Commands That Members Can Use in the Server
  - **mod_commands.py**: Commands Issued by Mods for Server Configuration
  - **random_commands.py**: Random Commands Just for Fun
- Logs (Directory):
  - **message_logs.py**: Logs Deleted/Edited Messages in the Server
  - **member_logs.py**: Logs New/Left Members + Role/Nickname Updates in the Server
  - **mod_logs.py**: Logs Moderation Actions (Kicks/Bans/Timeouts, etc.)
  - **server_logs.py**: Logs Changes to the Server
  - **voice_logs.py**: Logs Members Joining/Leaving/Switching Voice Channels
  - **event_logs.py**: Logs the Flight Hours of All Members as They Participate in Events

## Contributing

If you would like to contribute to this project, please send a message to `the._.pickle` on Discord.
