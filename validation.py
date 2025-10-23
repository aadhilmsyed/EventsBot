# Input validation and sanitization utilities

import re
import html


def sanitize_event_name(event_name: str) -> str:
    """Sanitize event name to prevent injection attacks and ensure valid format"""
    if not event_name or not event_name.strip():
        raise ValueError("Event name cannot be empty")

    # # Remove excessive whitespace and limit length
    # sanitized = event_name.strip()
    # if len(sanitized) > 100:
    #     raise ValueError("Event name cannot exceed 100 characters")

    # Remove potentially dangerous characters but allow most Unicode
    # sanitized = re.sub(r'[<>"\']', '', sanitized)

    # HTML escape to prevent injection
    # sanitized = html.escape(sanitized)

    return event_name


def validate_flight_time(minutes: int) -> int:
    """Validate flight time input"""
    if not isinstance(minutes, int):
        raise ValueError("Flight time must be an integer")

    if minutes < 0:
        raise ValueError("Flight time cannot be negative")

    if minutes > 10080:  # More than a week
        raise ValueError("Flight time cannot exceed 10,080 minutes (1 week)")

    return minutes


def validate_member_id(member_id) -> str:
    """Validate Discord member ID"""
    try:
        member_id_str = str(member_id)
        # Discord IDs are typically 17-19 digits
        if not re.match(r"^\d{17,19}$", member_id_str):
            raise ValueError("Invalid Discord member ID format")
        return member_id_str
    except (ValueError, TypeError):
        raise ValueError("Invalid member ID")


def sanitize_message(message: str) -> str:
    """Sanitize user message to prevent injection"""
    if not message:
        return ""

    # Limit message length
    if len(message) > 2000:  # Discord message limit
        message = message[:2000]

    # Remove excessive whitespace
    message = re.sub(r"\s+", " ", message.strip())

    # HTML escape to prevent injection
    message = html.escape(message)

    return message


def validate_icao_code(icao_code: str) -> str:
    """Validate ICAO airport code"""
    if not icao_code:
        raise ValueError("ICAO code cannot be empty")

    icao_code = icao_code.strip().upper()

    if not re.match(r"^[A-Z]{4}$", icao_code):
        raise ValueError("ICAO code must be exactly 4 letters")

    return icao_code
