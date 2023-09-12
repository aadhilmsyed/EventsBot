# GeoFS Events Discord Bot

Welcome to the GeoFS Events Discord Bot repository! This bot is designed to enhance your GeoFS Events Discord Server by providing useful features and functionality.

## Directory Structure

- **events_bot.py**: The main driver file for the bot.
- **bot_init.py**: Initializes and creates the Bot object.
- **bot_utils.py**: Contains functions that check the bot's status and health.
- **data.py**: Stores important variables used by other files.

### Commands

- **atis_metar**: Contains commands to fetch and send ATIS and METAR information using an API.
- **member_commands**: Commands that members can use within the server.
- **mod_commands**: Commands for server configuration, issued by moderators.
- **random_commands**: Fun and random commands for users.

### Logs

- **message_logs**: Logs deleted and edited messages within the server.
- **member_logs**: Logs new member joins, member leaves, and updates to roles and nicknames.
- **mod_logs**: Logs moderation actions like kicks, bans, timeouts, and more.
- **server_logs**: Logs changes made to the server settings.
- **voice_logs**: Logs member actions related to voice channels.
- **event_logs**: Logs flight hours of members participating in events.

## Usage

To use the GeoFS Events Discord Bot, follow the instructions in the main driver file `events_bot.py`. The bot's features and commands are organized into separate directories for easy management and customization.

## Contributing

If you would like to contribute to this project, please fork the repository, make your changes, and submit a pull request.

## Support

If you encounter any issues, have questions, or need assistance, please contact the bot owner or join our support server: [Support Server Link](https://discord.gg/your-server-invite).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
