"""
Pytest configuration and fixtures for EventsBot tests - Unit tests only.
"""

import pytest
import os

# Set up test environment variables from .env file - NO FALLBACKS
os.environ["DISCORD_TOKEN"] = os.getenv("DISCORD_TOKEN")
os.environ["GUILD_ID"] = os.getenv("GUILD_ID")
os.environ["LOG_CHANNEL_ID"] = os.getenv("LOG_CHANNEL_ID")
os.environ["MODERATOR_ROLE_ID"] = os.getenv("MODERATOR_ROLE_ID")
os.environ["CAPTAIN_ROLE_ID"] = os.getenv("CAPTAIN_ROLE_ID")
os.environ["FIRST_OFFICER_ROLE_ID"] = os.getenv("FIRST_OFFICER_ROLE_ID")
os.environ["FIRST_CLASS_ROLE_ID"] = os.getenv("FIRST_CLASS_ROLE_ID")
os.environ["BUSINESS_CLASS_ROLE_ID"] = os.getenv("BUSINESS_CLASS_ROLE_ID")
os.environ["PREMIUM_ECONOMY_ROLE_ID"] = os.getenv("PREMIUM_ECONOMY_ROLE_ID")
os.environ["ECONOMY_CLASS_ROLE_ID"] = os.getenv("ECONOMY_CLASS_ROLE_ID")
os.environ["SERVER_BOOSTER_ROLE_ID"] = os.getenv("SERVER_BOOSTER_ROLE_ID")


@pytest.fixture
def mock_config():
    """Create a mock config object for unit tests."""
    config = {
        "guild_id": int(os.getenv("GUILD_ID")),
        "log_channel_id": int(os.getenv("LOG_CHANNEL_ID")),
        "moderator_role_id": int(os.getenv("MODERATOR_ROLE_ID")),
        "captain_role_id": int(os.getenv("CAPTAIN_ROLE_ID")),
        "first_officer_role_id": int(os.getenv("FIRST_OFFICER_ROLE_ID")),
        "first_class_role_id": int(os.getenv("FIRST_CLASS_ROLE_ID")),
        "business_class_role_id": int(os.getenv("BUSINESS_CLASS_ROLE_ID")),
        "premium_economy_role_id": int(os.getenv("PREMIUM_ECONOMY_ROLE_ID")),
        "economy_class_role_id": int(os.getenv("ECONOMY_CLASS_ROLE_ID")),
        "server_booster_role_id": int(os.getenv("SERVER_BOOSTER_ROLE_ID")),
        "blacklist": [],
        "restricted_channels": [],
        "event_vc": [],
        "roles": {
            int(os.getenv("MODERATOR_ROLE_ID")): 1,  # Moderator
            int(os.getenv("CAPTAIN_ROLE_ID")): 2,  # Captain
            int(os.getenv("FIRST_OFFICER_ROLE_ID")): 3,  # First Officer
            int(os.getenv("FIRST_CLASS_ROLE_ID")): 4,  # First Class
            int(os.getenv("BUSINESS_CLASS_ROLE_ID")): 5,  # Business Class
            int(os.getenv("PREMIUM_ECONOMY_ROLE_ID")): 6,  # Premium Economy
            int(os.getenv("ECONOMY_CLASS_ROLE_ID")): 7,  # Economy Class
        },
    }
    return config
