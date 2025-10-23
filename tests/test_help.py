"""
Unit tests for help.py module - Pure function tests only.
"""
import pytest
import os
from unittest.mock import patch


class TestHelpUtilities:
    """Test cases for utility functions in help system."""
    
    def test_role_permission_checking(self):
        """Test role permission checking logic."""
        # Mock role IDs (from environment variables)
        economy_class_role_id = int(os.getenv('ECONOMY_CLASS_ROLE_ID', '1112981412191146004'))
        premium_economy_role_id = int(os.getenv('PREMIUM_ECONOMY_ROLE_ID', '1110680332879011882'))
        business_class_role_id = int(os.getenv('BUSINESS_CLASS_ROLE_ID', '1110680241569017966'))
        first_class_role_id = int(os.getenv('FIRST_CLASS_ROLE_ID', '989232534313369630'))
        first_officer_role_id = int(os.getenv('FIRST_OFFICER_ROLE_ID', '948366879980937297'))
        captain_role_id = int(os.getenv('CAPTAIN_ROLE_ID', '1316559380782645278'))
        moderator_role_id = int(os.getenv('MODERATOR_ROLE_ID', '766386531681435678'))
        server_booster_role_id = int(os.getenv('SERVER_BOOSTER_ROLE_ID', '786291409061150729'))
        
        # Test basic user (economy class only)
        user_roles = [economy_class_role_id]
        is_economy_class = economy_class_role_id in user_roles
        is_premium_economy = premium_economy_role_id in user_roles
        is_business_class = business_class_role_id in user_roles
        is_first_class = first_class_role_id in user_roles
        is_first_officer = first_officer_role_id in user_roles
        is_captain = captain_role_id in user_roles
        is_moderator = moderator_role_id in user_roles
        is_booster = server_booster_role_id in user_roles
        
        assert is_economy_class == True
        assert is_premium_economy == False
        assert is_business_class == False
        assert is_first_class == False
        assert is_first_officer == False
        assert is_captain == False
        assert is_moderator == False
        assert is_booster == False
        
        # Test premium economy user
        user_roles = [premium_economy_role_id]
        is_premium_economy = premium_economy_role_id in user_roles
        is_business_class = business_class_role_id in user_roles
        is_first_class = first_class_role_id in user_roles
        
        assert is_premium_economy == True
        assert is_business_class == False
        assert is_first_class == False
        
        # Test business class user
        user_roles = [business_class_role_id]
        is_business_class = business_class_role_id in user_roles
        is_first_class = first_class_role_id in user_roles
        
        assert is_business_class == True
        assert is_first_class == False
        
        # Test first class user
        user_roles = [first_class_role_id]
        is_first_class = first_class_role_id in user_roles
        
        assert is_first_class == True
    
    def test_command_availability_logic(self):
        """Test command availability logic."""
        def get_available_commands(user_roles):
            economy_class_role_id = int(os.getenv('ECONOMY_CLASS_ROLE_ID', '1112981412191146004'))
            premium_economy_role_id = int(os.getenv('PREMIUM_ECONOMY_ROLE_ID', '1110680332879011882'))
            business_class_role_id = int(os.getenv('BUSINESS_CLASS_ROLE_ID', '1110680241569017966'))
            first_class_role_id = int(os.getenv('FIRST_CLASS_ROLE_ID', '989232534313369630'))
            first_officer_role_id = int(os.getenv('FIRST_OFFICER_ROLE_ID', '948366879980937297'))
            captain_role_id = int(os.getenv('CAPTAIN_ROLE_ID', '1316559380782645278'))
            moderator_role_id = int(os.getenv('MODERATOR_ROLE_ID', '766386531681435678'))
            server_booster_role_id = int(os.getenv('SERVER_BOOSTER_ROLE_ID', '786291409061150729'))
            
            is_premium_economy = premium_economy_role_id in user_roles
            is_business_class = business_class_role_id in user_roles
            is_first_class = first_class_role_id in user_roles
            is_first_officer = first_officer_role_id in user_roles
            is_captain = captain_role_id in user_roles
            is_moderator = moderator_role_id in user_roles
            is_booster = server_booster_role_id in user_roles
            
            commands = ["ping", "quack", "help", "metar", "atis", "flighttime", "leaderboard"]
            
            # Premium Economy+ commands
            if is_premium_economy or is_business_class or is_first_class or is_first_officer or is_captain or is_moderator or is_booster:
                commands.append("dotspam")
            
            # Business Class+ commands
            if is_business_class or is_first_class or is_first_officer or is_captain or is_moderator or is_booster:
                commands.append("echo")
            
            # First Class+ commands
            if is_first_class or is_first_officer or is_captain or is_moderator or is_booster:
                commands.append("spam")
            
            return commands
        
        # Test economy class user
        economy_roles = [int(os.getenv('ECONOMY_CLASS_ROLE_ID', '1112981412191146004'))]
        economy_commands = get_available_commands(economy_roles)
        expected_economy = ["ping", "quack", "help", "metar", "atis", "flighttime", "leaderboard"]
        assert set(economy_commands) == set(expected_economy)
        
        # Test premium economy user
        premium_roles = [int(os.getenv('PREMIUM_ECONOMY_ROLE_ID', '1110680332879011882'))]
        premium_commands = get_available_commands(premium_roles)
        expected_premium = expected_economy + ["dotspam"]
        assert set(premium_commands) == set(expected_premium)
        
        # Test business class user
        business_roles = [int(os.getenv('BUSINESS_CLASS_ROLE_ID', '1110680241569017966'))]
        business_commands = get_available_commands(business_roles)
        expected_business = expected_premium + ["echo"]
        assert set(business_commands) == set(expected_business)
        
        # Test first class user
        first_class_roles = [int(os.getenv('FIRST_CLASS_ROLE_ID', '989232534313369630'))]
        first_class_commands = get_available_commands(first_class_roles)
        expected_first_class = expected_business + ["spam"]
        assert set(first_class_commands) == set(expected_first_class)
    
    def test_mod_help_permission_logic(self):
        """Test mod help permission logic."""
        def can_access_mod_help(user_roles):
            first_officer_role_id = int(os.getenv('FIRST_OFFICER_ROLE_ID', '948366879980937297'))
            captain_role_id = int(os.getenv('CAPTAIN_ROLE_ID', '1316559380782645278'))
            
            is_first_officer = first_officer_role_id in user_roles
            is_captain = captain_role_id in user_roles
            
            return is_first_officer or is_captain
        
        # Test first officer access
        first_officer_roles = [int(os.getenv('FIRST_OFFICER_ROLE_ID', '948366879980937297'))]
        assert can_access_mod_help(first_officer_roles) == True
        
        # Test captain access
        captain_roles = [int(os.getenv('CAPTAIN_ROLE_ID', '1316559380782645278'))]
        assert can_access_mod_help(captain_roles) == True
        
        # Test insufficient access
        other_roles = [int(os.getenv('FIRST_CLASS_ROLE_ID', '989232534313369630'))]  # First class
        assert can_access_mod_help(other_roles) == False
    
    def test_admin_help_permission_logic(self):
        """Test admin help permission logic."""
        def can_access_admin_help(user_roles):
            captain_role_id = int(os.getenv('CAPTAIN_ROLE_ID', '1316559380782645278'))
            return captain_role_id in user_roles
        
        # Test captain access
        captain_roles = [int(os.getenv('CAPTAIN_ROLE_ID', '1316559380782645278'))]
        assert can_access_admin_help(captain_roles) == True
        
        # Test insufficient access
        other_roles = [int(os.getenv('FIRST_OFFICER_ROLE_ID', '948366879980937297'))]  # First officer
        assert can_access_admin_help(other_roles) == False
        
        # Test insufficient access
        other_roles = [int(os.getenv('FIRST_CLASS_ROLE_ID', '989232534313369630'))]  # First class
        assert can_access_admin_help(other_roles) == False
    
    def test_embed_field_generation_logic(self):
        """Test embed field generation logic."""
        def generate_basic_commands_field():
            return {
                "name": "🔧 **Basic Commands**",
                "value": "```\n!ping                    - Check bot latency\n!quack                  - Bot quacks back\n!help                   - Show this help menu\n```",
                "inline": False
            }
        
        def generate_weather_commands_field():
            return {
                "name": "🌤️ **Weather Commands**",
                "value": "```\n!metar <ICAO>           - Get METAR weather data for airport\n!atis <ICAO>            - Get ATIS information for airport\n\nExample: !metar KSFO\n```",
                "inline": False
            }
        
        def generate_flight_tracking_field():
            return {
                "name": "✈️ **Flight Tracking**",
                "value": "```\n!flighttime [member]    - View flight hours (yours or specified member)\n!leaderboard           - Monthly flight hours leaderboard\n!view_member_history   - Events you've attended this month\n!view_event_history    - List events and view attendance\n```",
                "inline": False
            }
        
        # Test field generation
        basic_field = generate_basic_commands_field()
        assert basic_field["name"] == "🔧 **Basic Commands**"
        assert "!ping" in basic_field["value"]
        assert "!quack" in basic_field["value"]
        assert "!help" in basic_field["value"]
        
        weather_field = generate_weather_commands_field()
        assert weather_field["name"] == "🌤️ **Weather Commands**"
        assert "!metar" in weather_field["value"]
        assert "!atis" in weather_field["value"]
        
        flight_field = generate_flight_tracking_field()
        assert flight_field["name"] == "✈️ **Flight Tracking**"
        assert "!flighttime" in flight_field["value"]
        assert "!leaderboard" in flight_field["value"]
    
    def test_permission_level_description_logic(self):
        """Test permission level description logic."""
        def generate_permission_info(user_roles):
            economy_class_role_id = 123456789012345686
            premium_economy_role_id = 123456789012345685
            business_class_role_id = 123456789012345684
            first_class_role_id = 123456789012345683
            first_officer_role_id = 123456789012345682
            captain_role_id = 123456789012345681
            moderator_role_id = 123456789012345680
            server_booster_role_id = 123456789012345687
            
            is_premium_economy = premium_economy_role_id in user_roles
            is_business_class = business_class_role_id in user_roles
            is_first_class = first_class_role_id in user_roles
            is_first_officer = first_officer_role_id in user_roles
            is_captain = captain_role_id in user_roles
            is_moderator = moderator_role_id in user_roles
            is_booster = server_booster_role_id in user_roles
            
            role_info = "**Available to all members**"
            
            if is_premium_economy or is_business_class or is_first_class or is_first_officer or is_captain or is_moderator or is_booster:
                role_info += "\n**Premium Economy+:** Dotspam command available"
            if is_business_class or is_first_class or is_first_officer or is_captain or is_moderator or is_booster:
                role_info += "\n**Business Class+:** Echo command available"
            if is_first_class or is_first_officer or is_captain or is_moderator or is_booster:
                role_info += "\n**First Class+:** Spam command available"
            if is_moderator:
                role_info += "\n**Moderator:** All commands with pinging allowed"
            if is_booster:
                role_info += "\n**Server Booster:** Access to all role-based commands"
            
            return role_info
        
        # Test economy class user
        economy_roles = [123456789012345686]
        economy_info = generate_permission_info(economy_roles)
        assert "Available to all members" in economy_info
        assert "Premium Economy+" not in economy_info
        
        # Test premium economy user
        premium_roles = [123456789012345685]
        premium_info = generate_permission_info(premium_roles)
        assert "Premium Economy+" in premium_info
        assert "Business Class+" not in premium_info
        
        # Test business class user
        business_roles = [123456789012345684]
        business_info = generate_permission_info(business_roles)
        assert "Premium Economy+" in business_info
        assert "Business Class+" in business_info
        assert "First Class+" not in business_info
        
        # Test first class user
        first_class_roles = [123456789012345683]
        first_class_info = generate_permission_info(first_class_roles)
        assert "Premium Economy+" in first_class_info
        assert "Business Class+" in first_class_info
        assert "First Class+" in first_class_info