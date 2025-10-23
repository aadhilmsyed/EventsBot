"""
Tests for validation.py module.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from validation import (sanitize_event_name, sanitize_message,
                        validate_flight_time, validate_icao_code,
                        validate_member_id)


class TestSanitizeEventName:
    """Test cases for sanitize_event_name function."""

    def test_valid_event_name(self):
        """Test sanitizing a valid event name."""
        result = sanitize_event_name("Test Event")
        assert result == "Test Event"

    def test_empty_event_name(self):
        """Test sanitizing an empty event name."""
        with pytest.raises(ValueError, match="Event name cannot be empty"):
            sanitize_event_name("")

    def test_whitespace_only_event_name(self):
        """Test sanitizing a whitespace-only event name."""
        with pytest.raises(ValueError, match="Event name cannot be empty"):
            sanitize_event_name("   ")

    def test_none_event_name(self):
        """Test sanitizing a None event name."""
        with pytest.raises(ValueError, match="Event name cannot be empty"):
            sanitize_event_name(None)

    def test_event_name_with_unicode(self):
        """Test sanitizing event name with Unicode characters."""
        result = sanitize_event_name("Test Event 🛩️")
        assert result == "Test Event 🛩️"


class TestValidateFlightTime:
    """Test cases for validate_flight_time function."""

    def test_valid_flight_time(self):
        """Test validating a valid flight time."""
        result = validate_flight_time(120)
        assert result == 120

    def test_zero_flight_time(self):
        """Test validating zero flight time."""
        result = validate_flight_time(0)
        assert result == 0

    def test_negative_flight_time(self):
        """Test validating negative flight time."""
        with pytest.raises(ValueError, match="Flight time cannot be negative"):
            validate_flight_time(-10)

    def test_excessive_flight_time(self):
        """Test validating excessive flight time."""
        with pytest.raises(
            ValueError, match="Flight time cannot exceed 10,080 minutes"
        ):
            validate_flight_time(10081)

    def test_maximum_flight_time(self):
        """Test validating maximum allowed flight time."""
        result = validate_flight_time(10080)
        assert result == 10080

    def test_non_integer_flight_time(self):
        """Test validating non-integer flight time."""
        with pytest.raises(ValueError, match="Flight time must be an integer"):
            validate_flight_time("120")

    def test_float_flight_time(self):
        """Test validating float flight time."""
        with pytest.raises(ValueError, match="Flight time must be an integer"):
            validate_flight_time(120.5)


class TestValidateMemberId:
    """Test cases for validate_member_id function."""

    def test_valid_string_member_id(self):
        """Test validating a valid string member ID."""
        result = validate_member_id("123456789012345678")
        assert result == "123456789012345678"

    def test_valid_integer_member_id(self):
        """Test validating a valid integer member ID."""
        result = validate_member_id(123456789012345678)
        assert result == "123456789012345678"

    def test_none_member_id(self):
        """Test validating None member ID."""
        with pytest.raises(ValueError, match="Invalid member ID"):
            validate_member_id(None)

    def test_empty_string_member_id(self):
        """Test validating empty string member ID."""
        with pytest.raises(ValueError, match="Invalid member ID"):
            validate_member_id("")

    def test_invalid_type_member_id(self):
        """Test validating invalid type member ID."""
        with pytest.raises(ValueError, match="Invalid member ID"):
            validate_member_id([])


class TestSanitizeMessage:
    """Test cases for sanitize_message function."""

    def test_valid_message(self):
        """Test sanitizing a valid message."""
        result = sanitize_message("Hello, world!")
        assert result == "Hello, world!"

    def test_empty_message(self):
        """Test sanitizing an empty message."""
        result = sanitize_message("")
        assert result == ""

    def test_none_message(self):
        """Test sanitizing a None message."""
        result = sanitize_message(None)
        assert result == ""

    def test_long_message(self):
        """Test sanitizing a message that exceeds Discord's limit."""
        long_message = "a" * 2001
        result = sanitize_message(long_message)
        assert len(result) == 2000
        assert result == "a" * 2000

    def test_message_with_whitespace(self):
        """Test sanitizing a message with excessive whitespace."""
        result = sanitize_message("  Hello   world  ")
        assert result == "Hello world"  # Function normalizes whitespace


class TestValidateIcaoCode:
    """Test cases for validate_icao_code function."""

    def test_valid_icao_code(self):
        """Test validating a valid ICAO code."""
        result = validate_icao_code("KSFO")
        assert result == "KSFO"

    def test_lowercase_icao_code(self):
        """Test validating a lowercase ICAO code."""
        result = validate_icao_code("ksfo")
        assert result == "KSFO"

    def test_icao_code_with_whitespace(self):
        """Test validating an ICAO code with whitespace."""
        result = validate_icao_code("  KSFO  ")
        assert result == "KSFO"

    def test_empty_icao_code(self):
        """Test validating an empty ICAO code."""
        with pytest.raises(ValueError, match="ICAO code cannot be empty"):
            validate_icao_code("")

    def test_none_icao_code(self):
        """Test validating a None ICAO code."""
        with pytest.raises(ValueError, match="ICAO code cannot be empty"):
            validate_icao_code(None)

    def test_short_icao_code(self):
        """Test validating a short ICAO code."""
        with pytest.raises(ValueError, match="ICAO code must be exactly 4 letters"):
            validate_icao_code("KSF")

    def test_long_icao_code(self):
        """Test validating a long ICAO code."""
        with pytest.raises(ValueError, match="ICAO code must be exactly 4 letters"):
            validate_icao_code("KSFOO")

    def test_icao_code_with_numbers(self):
        """Test validating an ICAO code with numbers."""
        with pytest.raises(ValueError, match="ICAO code must be exactly 4 letters"):
            validate_icao_code("KSF1")

    def test_icao_code_with_special_chars(self):
        """Test validating an ICAO code with special characters."""
        with pytest.raises(ValueError, match="ICAO code must be exactly 4 letters"):
            validate_icao_code("KS-F")
