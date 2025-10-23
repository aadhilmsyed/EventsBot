"""
Pytest configuration and fixtures for EventsBot tests - Unit tests only.
"""
import pytest
import os

# Set up test environment variables (token should come from environment)
os.environ['DISCORD_TOKEN'] = os.getenv('DISCORD_TOKEN', 'test_token')
os.environ['GUILD_ID'] = '553718744233541656'
os.environ['LOG_CHANNEL_ID'] = '1184292134258479176'
os.environ['MODERATOR_ROLE_ID'] = '766386531681435678'
os.environ['CAPTAIN_ROLE_ID'] = '1316559380782645278'
os.environ['FIRST_OFFICER_ROLE_ID'] = '948366879980937297'
os.environ['FIRST_CLASS_ROLE_ID'] = '989232534313369630'
os.environ['BUSINESS_CLASS_ROLE_ID'] = '1110680241569017966'
os.environ['PREMIUM_ECONOMY_ROLE_ID'] = '1110680332879011882'
os.environ['ECONOMY_CLASS_ROLE_ID'] = '1112981412191146004'
os.environ['SERVER_BOOSTER_ROLE_ID'] = '786291409061150729'


@pytest.fixture
def mock_config():
    """Create a mock config object for unit tests."""
    config = {
        'guild_id': 553718744233541656,
        'log_channel_id': 1184292134258479176,
        'moderator_role_id': 766386531681435678,
        'captain_role_id': 1316559380782645278,
        'first_officer_role_id': 948366879980937297,
        'first_class_role_id': 989232534313369630,
        'business_class_role_id': 1110680241569017966,
        'premium_economy_role_id': 1110680332879011882,
        'economy_class_role_id': 1112981412191146004,
        'server_booster_role_id': 786291409061150729,
        'blacklist': [],
        'restricted_channels': [],
        'event_vc': [],
        'roles': {
            766386531681435678: 1,  # Moderator
            1316559380782645278: 2,  # Captain
            948366879980937297: 3,  # First Officer
            989232534313369630: 4,  # First Class
            1110680241569017966: 5,  # Business Class
            1110680332879011882: 6,  # Premium Economy
            1112981412191146004: 7,  # Economy Class
        }
    }
    return config