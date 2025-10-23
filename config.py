# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Other Necessary Libraries
from datetime import datetime as time
import pytz
import json
import os
import threading
import shutil
import tempfile
from collections import OrderedDict


class Configurations:

    def __init__(self):
        # Load Discord IDs from environment variables (no defaults - must be in .env)
        guild_id_str = os.getenv("GUILD_ID")
        if not guild_id_str:
            raise ValueError("GUILD_ID environment variable is required!")
        self.guild_id = int(guild_id_str)

        log_channel_id_str = os.getenv("LOG_CHANNEL_ID")
        if not log_channel_id_str:
            raise ValueError("LOG_CHANNEL_ID environment variable is required!")
        self.log_channel_id = int(log_channel_id_str)

        # Role IDs from environment variables (no defaults - must be in .env)
        moderator_role_id_str = os.getenv("MODERATOR_ROLE_ID")
        if not moderator_role_id_str:
            raise ValueError("MODERATOR_ROLE_ID environment variable is required!")
        self.moderator_role_id = int(moderator_role_id_str)

        captain_role_id_str = os.getenv("CAPTAIN_ROLE_ID")
        if not captain_role_id_str:
            raise ValueError("CAPTAIN_ROLE_ID environment variable is required!")
        self.captain_role_id = int(captain_role_id_str)

        first_officer_role_id_str = os.getenv("FIRST_OFFICER_ROLE_ID")
        if not first_officer_role_id_str:
            raise ValueError("FIRST_OFFICER_ROLE_ID environment variable is required!")
        self.first_officer_role_id = int(first_officer_role_id_str)

        first_class_role_id_str = os.getenv("FIRST_CLASS_ROLE_ID")
        if not first_class_role_id_str:
            raise ValueError("FIRST_CLASS_ROLE_ID environment variable is required!")
        self.first_class_role_id = int(first_class_role_id_str)

        business_class_role_id_str = os.getenv("BUSINESS_CLASS_ROLE_ID")
        if not business_class_role_id_str:
            raise ValueError("BUSINESS_CLASS_ROLE_ID environment variable is required!")
        self.business_class_role_id = int(business_class_role_id_str)

        premium_economy_role_id_str = os.getenv("PREMIUM_ECONOMY_ROLE_ID")
        if not premium_economy_role_id_str:
            raise ValueError(
                "PREMIUM_ECONOMY_ROLE_ID environment variable is required!"
            )
        self.premium_economy_role_id = int(premium_economy_role_id_str)

        economy_class_role_id_str = os.getenv("ECONOMY_CLASS_ROLE_ID")
        if not economy_class_role_id_str:
            raise ValueError("ECONOMY_CLASS_ROLE_ID environment variable is required!")
        self.economy_class_role_id = int(economy_class_role_id_str)

        server_booster_role_id_str = os.getenv("SERVER_BOOSTER_ROLE_ID")
        if not server_booster_role_id_str:
            raise ValueError("SERVER_BOOSTER_ROLE_ID environment variable is required!")
        self.server_booster_role_id = int(server_booster_role_id_str)

        # Server and Log Channel
        self.guild = None
        self.log_channel = None

        # Server Staff Roles
        self.captain_role = None
        self.first_officer_role = None

        # Server Member Roles
        self.first_class_role = None
        self.business_class_role = None
        self.premium_economy_role = None
        self.economy_class_role = None
        self.member_role = None

        # Long Haul Roles
        self.flight_deck_role = None
        self.lh_first_class_role = None
        self.lh_business_class_role = None
        self.lh_premium_economy_role = None
        self.lh_economy_class_role = None
        self.check_in_role = None
        self.security_role = None

        # Long Haul Channels
        self.cockpit_channel = None
        self.baggage_claim_channel = None
        self.lh_first_class_channel = None
        self.lh_business_class_channel = None
        self.lh_premium_economy_channel = None
        self.lh_economy_class_channel = None
        self.check_in_channel = None
        self.security_channel = None
        self.boarding_lounge_channel = None
        self.customs_channel = None

        # Restricted Channels & Blacklist
        self.restricted_channels = []
        self.blacklist = []

        # Roles - using environment variable IDs
        self.roles = {  # Role ID, Hours
            self.first_class_role_id: 8,
            self.business_class_role_id: 5,
            self.premium_economy_role_id: 2,
            self.economy_class_role_id: 1,
        }

    def save(self, file_path="/data/config/bot_settings.json"):
        """Save configuration with atomic write and backup"""
        data = {
            "restricted_channels": self.restricted_channels,
            "blacklist_members": self.blacklist,
        }

        # Create backup if file exists
        if os.path.exists(file_path):
            backup_path = f"{file_path}.backup"
            shutil.copy2(file_path, backup_path)

        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Atomic write using temporary file
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", dir=os.path.dirname(file_path), delete=False
            ) as temp_file:
                json.dump(data, temp_file, indent=2)
                temp_path = temp_file.name

            # Atomic move
            shutil.move(temp_path, file_path)

        except Exception as e:
            # Clean up temp file if it exists
            if "temp_path" in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e

    def load(self, file_path="/data/config/bot_settings.json"):
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                data = json.load(file)
                self.restricted_channels = data.get("restricted_channels", [])
                self.blacklist = data.get("blacklist_members", [])


class FlightHours:
    def __init__(self):

        # Class Attributes
        self.flight_hours = {}  # Key: Member ID (str) | Value: Minutes (int)
        self.start_time = {}  # Key: Member ID (str) | Value: Time (datetime)
        self.event_history = (
            OrderedDict()
        )  # Key: Event Name (str) | Value: ID of Members Joined (Set of str)
        self.member_history = (
            {}
        )  # Key: Member ID (str) | Value: Events Joined (Set of str)
        self.active_event = None
        self.voice_channels = []

        # Thread lock for preventing race conditions
        self._lock = threading.Lock()

    def log_start_time(self, member_id, member=None):
        # Ensure member_id is always a string for consistency
        member_id_str = str(member_id)

        # Check if this is a bot (if member object is provided)
        if member and member.bot:
            return False  # Don't log bots

        # Additional safety check: if we can't verify it's not a bot, skip logging
        # This prevents any potential bot logging if member object is not provided
        if not member:
            # Try to get member from guild to check if it's a bot
            try:
                guild_member = (
                    self.guild.get_member(int(member_id_str)) if self.guild else None
                )
                if guild_member and guild_member.bot:
                    return False  # Don't log bots
            except (ValueError, AttributeError):
                # If we can't determine, err on the side of caution and don't log
                return False

        with self._lock:
            # Only track the start time - don't add to history yet
            if member_id_str not in self.start_time:
                self.start_time[member_id_str] = time.now(pytz.utc)

        return True  # Successfully logged

    def log_end_time(self, member_id, member=None):
        # Ensure member_id is always a string for consistency
        member_id_str = str(member_id)

        # Check if this is a bot (if member object is provided)
        if member and member.bot:
            return 0  # Don't log bots

        # Additional safety check: if we can't verify it's not a bot, skip logging
        if not member:
            # Try to get member from guild to check if it's a bot
            try:
                guild_member = (
                    self.guild.get_member(int(member_id_str)) if self.guild else None
                )
                if guild_member and guild_member.bot:
                    return 0  # Don't log bots
            except (ValueError, AttributeError):
                # If we can't determine, err on the side of caution and don't log
                return 0

        with self._lock:
            if member_id_str in self.start_time:

                # Calculate how long the member was in the voice channel for
                elapsed = time.now(pytz.utc) - self.start_time[member_id_str]
                minutes_flown = int(elapsed.total_seconds() // 60)

                # Validate calculated time (prevent negative or excessive values)
                if minutes_flown < 0:
                    minutes_flown = 0
                elif minutes_flown > 1440:  # More than 24 hours
                    minutes_flown = 1440

                # Check if member stayed for more than 5 minutes
                if minutes_flown >= 5:
                    # Add to history only if they stayed for 5+ minutes
                    if member_id_str not in self.member_history:
                        self.member_history[member_id_str] = set()

                    # Add the member to the event history and the event to member history
                    self.event_history[self.active_event].add(member_id_str)
                    self.member_history[member_id_str].add(self.active_event)

                    # If the member is not in the flight hours dictionary, add them to it
                    if member_id_str not in self.flight_hours:
                        self.flight_hours[member_id_str] = 0

                    # Add the elapsed minutes to the total flight hours for the member
                    self.flight_hours[member_id_str] += minutes_flown

                    # Validate total flight hours (prevent excessive accumulation)
                    if self.flight_hours[member_id_str] > 10080:  # More than a week
                        self.flight_hours[member_id_str] = 10080

                # Remove the start time entry for the member regardless of duration
                del self.start_time[member_id_str]

                # Return the minutes flown
                return minutes_flown

            else:
                return 0  # Extra layer of protection

    def save(self, file_path="/data/flight_hours/current.json"):
        """Save flight hours with atomic write and backup"""
        with self._lock:
            # Convert non-parseable data types to parseable data types
            start_time_str = {k: v.isoformat() for k, v in self.start_time.items()}
            member_history_list = {k: list(v) for k, v in self.member_history.items()}
            event_history_list = {k: list(v) for k, v in self.event_history.items()}
            voice_channel_ids = [channel.id for channel in self.voice_channels]

            # Store the data in JSON format
            data = {
                "active_event": self.active_event,
                "voice_channels": voice_channel_ids,
                "flight_hours": self.flight_hours,
                "start_time": start_time_str,
                "member_history": member_history_list,
                "event_history": event_history_list,
            }

            # Create backup if file exists
            if os.path.exists(file_path):
                backup_path = f"{file_path}.backup"
                shutil.copy2(file_path, backup_path)

            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Atomic write using temporary file
            try:
                with tempfile.NamedTemporaryFile(
                    mode="w", dir=os.path.dirname(file_path), delete=False
                ) as temp_file:
                    json.dump(data, temp_file, indent=2)
                    temp_path = temp_file.name

                # Atomic move
                shutil.move(temp_path, file_path)

            except Exception as e:
                # Clean up temp file if it exists
                if "temp_path" in locals() and os.path.exists(temp_path):
                    os.unlink(temp_path)
                raise e

    def load(self, file_path="/data/flight_hours/current.json"):
        """Load flight hours with error handling and backup recovery"""
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    # Retrieve the JSON data from the file
                    data = json.load(file)
                    self.active_event = data.get("active_event", None)
                    # Filter out None values (deleted channels) to prevent memory leaks
                    self.voice_channels = [
                        config.guild.get_channel(vc_id)
                        for vc_id in data.get("voice_channels", [])
                        if config.guild.get_channel(vc_id) is not None
                    ]
                    self.flight_hours = data.get("flight_hours", {})
                    self.start_time = {
                        k: time.fromisoformat(v)
                        for k, v in data.get("start_time", {}).items()
                    }
                    self.member_history = {
                        k: set(v) for k, v in data.get("member_history", {}).items()
                    }
                    # Convert event_history back to OrderedDict to maintain order
                    event_history_data = data.get("event_history", {})
                    self.event_history = OrderedDict(
                        (k, set(v)) for k, v in event_history_data.items()
                    )

            except (json.JSONDecodeError, ValueError, KeyError) as e:
                # Try to restore from backup
                backup_path = f"{file_path}.backup"
                if os.path.exists(backup_path):
                    try:
                        with open(backup_path, "r") as file:
                            data = json.load(file)
                            self.active_event = data.get("active_event", None)
                            self.voice_channels = [
                                config.guild.get_channel(vc_id)
                                for vc_id in data.get("voice_channels", [])
                                if config.guild.get_channel(vc_id) is not None
                            ]
                            self.flight_hours = data.get("flight_hours", {})
                            self.start_time = {
                                k: time.fromisoformat(v)
                                for k, v in data.get("start_time", {}).items()
                            }
                            self.member_history = {
                                k: set(v)
                                for k, v in data.get("member_history", {}).items()
                            }
                            # Convert event_history back to OrderedDict to maintain order
                            event_history_data = data.get("event_history", {})
                            self.event_history = OrderedDict(
                                (k, set(v)) for k, v in event_history_data.items()
                            )
                            print(
                                f"Restored flight hours from backup due to corruption: {e}"
                            )
                    except Exception as backup_error:
                        print(f"Failed to restore from backup: {backup_error}")
                        # Initialize with empty data
                        self.active_event = None
                        self.voice_channels = []
                        self.flight_hours = {}
                        self.start_time = {}
                        self.member_history = {}
                        self.event_history = OrderedDict()
                else:
                    print(f"No backup available, initializing with empty data: {e}")
                    # Initialize with empty data
                    self.active_event = None
                    self.voice_channels = []
                    self.flight_hours = {}
                    self.start_time = {}
                    self.member_history = {}
                    self.event_history = OrderedDict()

    def create_backup(self, file_path="/data/flight_hours/current.json"):
        """Create a timestamped backup of flight hours data"""
        if os.path.exists(file_path):
            timestamp = time.now(pytz.utc).strftime("%Y%m%d_%H%M%S")
            backup_path = f"/data/backups/flight_hours_backup_{timestamp}.json"

            # Ensure backup directory exists
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)

            # Copy current file to backup
            shutil.copy2(file_path, backup_path)
            return backup_path
        return None

    async def export(self, file_path):
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:

            # Iterate through the dictionary
            for member_id, minutes in self.flight_hours.items():

                # Check if the member exists
                member = None
                try:
                    member = await config.guild.fetch_member(member_id)
                except Exception as e:
                    member = None

                # Calculate the flight time
                hours, minutes = divmod(minutes, 60)

                # Write the flight time to the file
                if member:
                    file.write(f"{member.name}: {hours} hours {minutes} minutes\n")


# Create Objects
config = Configurations()
flight_hours_manager = FlightHours()
