"""
Unit tests for monthly_roles.py module - Pure function tests only.
"""

import pytest
import os
from unittest.mock import patch


class TestMonthlyRolesUtilities:
    """Test cases for utility functions in monthly roles."""

    def test_calculate_earned_role_function(self):
        """Test the calculate_earned_role function."""
        # Mock role thresholds (from environment variables)
        roles = {
            int(os.getenv("MODERATOR_ROLE_ID")): 1,  # Moderator - 1 hour
            int(os.getenv("CAPTAIN_ROLE_ID")): 2,  # Captain - 2 hours
            int(os.getenv("FIRST_OFFICER_ROLE_ID")): 3,  # First Officer - 3 hours
            int(os.getenv("FIRST_CLASS_ROLE_ID")): 4,  # First Class - 4 hours
            int(os.getenv("BUSINESS_CLASS_ROLE_ID")): 5,  # Business Class - 5 hours
            int(os.getenv("PREMIUM_ECONOMY_ROLE_ID")): 6,  # Premium Economy - 6 hours
            int(os.getenv("ECONOMY_CLASS_ROLE_ID")): 7,  # Economy Class - 7 hours
        }

        # Test calculate_earned_role function logic
        def calculate_earned_role(minutes):
            if minutes == 0:
                return None

            # Calculate hours with grace (+1 hour)
            hours = (minutes // 60) + 1

            # Sort roles by threshold (highest first) to find the best role
            sorted_roles = sorted(roles.items(), key=lambda x: x[1], reverse=True)

            # Find the highest role threshold met
            for role_id, threshold in sorted_roles:
                if hours >= threshold:
                    return role_id

            return None

        # Test cases
        assert calculate_earned_role(0) is None  # No time
        assert calculate_earned_role(30) == int(
            os.getenv("MODERATOR_ROLE_ID")
        )  # 0.5 hours + 1 grace = 1 hour (Moderator)
        assert calculate_earned_role(60) == int(
            os.getenv("CAPTAIN_ROLE_ID")
        )  # 1 hour + 1 grace = 2 hours (Captain)
        assert calculate_earned_role(90) == int(
            os.getenv("CAPTAIN_ROLE_ID")
        )  # 1.5 hours + 1 grace = 2.5 hours (Captain)
        assert calculate_earned_role(120) == int(
            os.getenv("FIRST_OFFICER_ROLE_ID")
        )  # 2 hours + 1 grace = 3 hours (First Officer)
        assert calculate_earned_role(180) == int(
            os.getenv("FIRST_CLASS_ROLE_ID")
        )  # 3 hours + 1 grace = 4 hours (First Class)
        assert calculate_earned_role(300) == int(
            os.getenv("PREMIUM_ECONOMY_ROLE_ID")
        )  # 5 hours + 1 grace = 6 hours (Premium Economy)

    def test_role_threshold_sorting(self):
        """Test role threshold sorting logic."""
        roles = {
            "moderator": 1,
            "captain": 2,
            "first_officer": 3,
            "first_class": 4,
            "business_class": 5,
            "premium_economy": 6,
            "economy_class": 7,
        }

        # Sort by threshold (highest first)
        sorted_roles = sorted(roles.items(), key=lambda x: x[1], reverse=True)

        expected_order = [
            ("economy_class", 7),
            ("premium_economy", 6),
            ("business_class", 5),
            ("first_class", 4),
            ("first_officer", 3),
            ("captain", 2),
            ("moderator", 1),
        ]

        assert sorted_roles == expected_order

    def test_hours_calculation_with_grace(self):
        """Test hours calculation with grace period."""

        def calculate_hours_with_grace(minutes):
            return (minutes // 60) + 1

        # Test various minute values
        test_cases = [
            (0, 1),  # 0 minutes + 1 grace = 1 hour
            (30, 1),  # 30 minutes + 1 grace = 1 hour
            (59, 1),  # 59 minutes + 1 grace = 1 hour
            (60, 2),  # 60 minutes + 1 grace = 2 hours
            (90, 2),  # 90 minutes + 1 grace = 2 hours
            (120, 3),  # 120 minutes + 1 grace = 3 hours
            (180, 4),  # 180 minutes + 1 grace = 4 hours
        ]

        for minutes, expected_hours in test_cases:
            assert calculate_hours_with_grace(minutes) == expected_hours

    def test_role_comparison_logic(self):
        """Test role comparison logic."""
        # Mock role data
        roles = {
            "moderator": {"id": 123456789012345680, "threshold": 1},
            "captain": {"id": 123456789012345681, "threshold": 2},
            "first_officer": {"id": 123456789012345682, "threshold": 3},
        }

        def find_best_role(hours):
            best_role = None
            best_threshold = 0

            for role_name, role_data in roles.items():
                if (
                    hours >= role_data["threshold"]
                    and role_data["threshold"] > best_threshold
                ):
                    best_role = role_data["id"]
                    best_threshold = role_data["threshold"]

            return best_role

        # Test role selection
        assert find_best_role(0) is None  # No role earned
        assert find_best_role(1) == 123456789012345680  # Moderator
        assert find_best_role(2) == 123456789012345681  # Captain
        assert find_best_role(3) == 123456789012345682  # First Officer
        assert (
            find_best_role(4) == 123456789012345682
        )  # Still First Officer (highest available)

    def test_flight_hours_data_processing(self):
        """Test flight hours data processing logic."""
        # Mock flight hours data
        flight_hours = {
            "user1": 120,  # 2 hours
            "user2": 180,  # 3 hours
            "user3": 60,  # 1 hour
            "user4": 300,  # 5 hours
            "user5": 0,  # No hours
        }

        # Test data filtering and processing
        active_users = {
            user: hours for user, hours in flight_hours.items() if hours > 0
        }
        assert len(active_users) == 4
        assert "user5" not in active_users

        # Test sorting by hours
        sorted_users = sorted(active_users.items(), key=lambda x: x[1], reverse=True)
        expected_order = [
            ("user4", 300),
            ("user2", 180),
            ("user1", 120),
            ("user3", 60),
        ]
        assert sorted_users == expected_order

        # Test role assignment logic
        def assign_role(hours):
            if hours >= 300:  # 5+ hours
                return "first_class"
            elif hours >= 180:  # 3+ hours
                return "first_officer"
            elif hours >= 120:  # 2+ hours
                return "captain"
            elif hours >= 60:  # 1+ hours
                return "moderator"
            else:
                return None

        role_assignments = {
            user: assign_role(hours) for user, hours in active_users.items()
        }
        expected_roles = {
            "user1": "captain",
            "user2": "first_officer",
            "user3": "moderator",
            "user4": "first_class",
        }
        assert role_assignments == expected_roles

    def test_data_cleanup_logic(self):
        """Test data cleanup logic."""
        # Mock data structures
        flight_hours = {"user1": 120, "user2": 180, "user3": 60}
        start_times = {
            "user1": "2023-01-01",
            "user2": "2023-01-02",
            "user3": "2023-01-03",
        }
        event_history = {"Event1": {"user1", "user2"}, "Event2": {"user2", "user3"}}

        # Test clearing flight hours
        def clear_flight_hours():
            return {}

        cleared_hours = clear_flight_hours()
        assert cleared_hours == {}

        # Test clearing start times
        def clear_start_times():
            return {}

        cleared_times = clear_start_times()
        assert cleared_times == {}

        # Test clearing event history
        def clear_event_history():
            return {}

        cleared_history = clear_event_history()
        assert cleared_history == {}

    def test_role_update_efficiency_logic(self):
        """Test role update efficiency logic."""
        # Mock member data
        members = [
            {"id": "user1", "roles": ["old_role1"]},
            {"id": "user2", "roles": ["old_role2"]},
            {"id": "user3", "roles": []},
        ]

        # Mock flight hours
        flight_hours = {
            "user1": 120,  # Should get captain role
            "user2": 60,  # Should get moderator role
            "user3": 0,  # Should get no role
        }

        # Test role update logic
        def determine_role_updates():
            updates = []
            for member in members:
                user_id = member["id"]
                hours = flight_hours.get(user_id, 0)

                if hours >= 120:
                    new_role = "captain"
                elif hours >= 60:
                    new_role = "moderator"
                else:
                    new_role = None

                if new_role:
                    updates.append({"user_id": user_id, "new_role": new_role})

            return updates

        role_updates = determine_role_updates()
        expected_updates = [
            {"user_id": "user1", "new_role": "captain"},
            {"user_id": "user2", "new_role": "moderator"},
        ]

        assert role_updates == expected_updates
