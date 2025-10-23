"""
Tests for logger.py module.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from logger import Logger


class TestLogger:
    """Test cases for Logger class."""

    @pytest.fixture
    def mock_channel(self):
        """Create a mock Discord channel."""
        channel = MagicMock()
        channel.send = AsyncMock()
        channel.mention = "<#123456789012345679>"
        return channel

    @pytest.fixture
    def logger(self, mock_channel):
        """Create a Logger instance with mock channel."""
        return Logger(mock_channel)

    @pytest.mark.asyncio
    async def test_init_with_channel(self, mock_channel):
        """Test Logger initialization with channel."""
        logger = Logger(mock_channel)
        assert logger.log_channel == mock_channel

    @pytest.mark.asyncio
    async def test_set_channel(self, logger, mock_channel):
        """Test setting log channel."""
        new_channel = MagicMock()
        new_channel.send = AsyncMock()
        new_channel.mention = "<#123456789012345680>"

        await logger.setChannel(new_channel)

        assert logger.log_channel == new_channel
        new_channel.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_info_message(self, logger, mock_channel):
        """Test sending info message."""
        message = "Test info message"

        await logger.info(message)

        mock_channel.send.assert_called_once_with(message)

    @pytest.mark.asyncio
    async def test_error_message(self, logger, mock_channel):
        """Test sending error message."""
        message = "Test error message"

        await logger.error(message)

        mock_channel.send.assert_called_once_with(f"**ERROR:** {message}")

    @pytest.mark.asyncio
    async def test_info_with_none_channel(self):
        """Test info method with None channel."""
        logger = Logger(None)

        # Should not raise an exception
        await logger.info("Test message")

    @pytest.mark.asyncio
    async def test_error_with_none_channel(self):
        """Test error method with None channel."""
        logger = Logger(None)

        # Should not raise an exception
        await logger.error("Test message")

    @pytest.mark.asyncio
    async def test_info_channel_send_failure(self, mock_channel):
        """Test info method when channel.send fails."""
        logger = Logger(mock_channel)
        mock_channel.send.side_effect = Exception("Send failed")

        # Should not raise an exception, should handle gracefully
        with patch("builtins.print") as mock_print:
            await logger.info("Test message")
            mock_print.assert_called_once()

    @pytest.mark.asyncio
    async def test_error_channel_send_failure(self, mock_channel):
        """Test error method when channel.send fails."""
        logger = Logger(mock_channel)
        mock_channel.send.side_effect = Exception("Send failed")

        # Should not raise an exception, should handle gracefully
        with patch("builtins.print") as mock_print:
            await logger.error("Test message")
            mock_print.assert_called_once()

    @pytest.mark.asyncio
    async def test_empty_message(self, logger, mock_channel):
        """Test sending empty message."""
        await logger.info("")
        await logger.error("")

        assert mock_channel.send.call_count == 2

    @pytest.mark.asyncio
    async def test_long_message(self, logger, mock_channel):
        """Test sending long message."""
        long_message = "a" * 2000

        await logger.info(long_message)
        await logger.error(long_message)

        assert mock_channel.send.call_count == 2
        mock_channel.send.assert_any_call(long_message)
        mock_channel.send.assert_any_call(f"**ERROR:** {long_message}")
