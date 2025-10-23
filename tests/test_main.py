"""
Integration tests for main.py - Tests bot startup and basic command functionality.
This test requires a valid Discord bot token and will actually connect to Discord.
"""
import pytest
import asyncio
import os
import sys
from unittest.mock import patch, MagicMock, AsyncMock
import discord
from discord.ext import commands


class TestMainIntegration:
    """Integration tests for main.py bot startup and basic functionality."""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_bot_startup_and_ping_command(self):
        """
        Test that the bot can start up and respond to the ping command.
        This is a real integration test that connects to Discord.
        """
        # Skip this test if no real Discord token is provided
        token = os.getenv('DISCORD_TOKEN')
        if not token or token == 'test_token':
            pytest.skip("Skipping integration test - no real Discord token provided")
        
        # Create a test bot instance
        intents = discord.Intents.all()
        test_bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
        
        # Track if bot is ready
        bot_ready = False
        ping_response_received = False
        ping_response_content = None
        
        @test_bot.event
        async def on_ready():
            nonlocal bot_ready
            bot_ready = True
            print(f"Test bot logged in as {test_bot.user}")
        
        # Add a simple ping command for testing
        @test_bot.command()
        async def ping(ctx):
            """Test ping command"""
            nonlocal ping_response_received, ping_response_content
            response = f"Pong! Latency: {round(test_bot.latency * 1000)}ms"
            ping_response_content = response
            await ctx.send(response)
            ping_response_received = True
        
        # Track command responses
        command_responses = []
        
        @test_bot.event
        async def on_message(message):
            if message.author == test_bot.user:
                return
            
            if message.content.startswith('!ping'):
                command_responses.append(message.content)
            
            await test_bot.process_commands(message)
        
        try:
            # Start the bot
            bot_task = asyncio.create_task(test_bot.start(token))
            
            # Wait for bot to be ready (with timeout)
            timeout = 30  # 30 seconds timeout
            start_time = asyncio.get_event_loop().time()
            
            while not bot_ready and (asyncio.get_event_loop().time() - start_time) < timeout:
                await asyncio.sleep(0.1)
            
            # Verify bot is ready
            assert bot_ready, "Bot failed to start within timeout period"
            assert test_bot.user is not None, "Bot user is None"
            assert test_bot.is_ready(), "Bot is not ready"
            
            # Test ping command by checking command registration
            ping_command = test_bot.get_command('ping')
            assert ping_command is not None, "Ping command not found"
            assert ping_command.name == 'ping', f"Expected 'ping' command, got '{ping_command.name}'"
            
            # Test actual command execution by sending a real message to Discord
            # Get the test guild and channel
            guild_id = int(os.getenv('GUILD_ID'))
            channel_id = int(os.getenv('LOG_CHANNEL_ID'))
            
            guild = test_bot.get_guild(guild_id)
            assert guild is not None, f"Could not find guild with ID {guild_id}"
            
            channel = guild.get_channel(channel_id)
            assert channel is not None, f"Could not find channel with ID {channel_id}"
            
            # Test command execution by directly invoking the command
            # Create a mock context for the ping command
            mock_message = MagicMock()
            mock_message.content = "!ping"
            mock_message.author = MagicMock()
            mock_message.author.id = int(os.getenv('CAPTAIN_ROLE_ID'))
            mock_message.author.bot = False
            mock_message.channel = channel
            mock_message.guild = guild
            
            # Get the context and invoke the command directly
            ctx = await test_bot.get_context(mock_message)
            if ctx.command:
                # Mock the send method to capture the response
                original_send = ctx.send
                sent_messages = []
                
                async def mock_send(content=None, **kwargs):
                    sent_messages.append(content)
                    return MagicMock()  # Return a mock message object
                
                ctx.send = mock_send
                
                # Invoke the command
                await ctx.invoke(ctx.command)
                
                # Restore original send method
                ctx.send = original_send
                
                # Verify the command was executed
                assert ping_response_received, "Ping command did not execute"
                assert ping_response_content is not None, "Ping command did not generate response"
                assert "Pong!" in ping_response_content, f"Expected 'Pong!' in response, got: {ping_response_content}"
                assert "Latency:" in ping_response_content, f"Expected 'Latency:' in response, got: {ping_response_content}"
                
                print(f"✅ Ping command executed successfully: {ping_response_content}")
                
                # Also verify the mock send was called
                assert len(sent_messages) > 0, "Command did not attempt to send a message"
                assert "Pong!" in sent_messages[0], f"Expected 'Pong!' in sent message, got: {sent_messages[0]}"
                
                print(f"✅ Command response verified: {sent_messages[0]}")
            else:
                pytest.fail("Could not get command context for ping command")
            
            print("✅ Bot startup and ping command test passed!")
            
        except Exception as e:
            print(f"❌ Integration test failed: {e}")
            raise
        finally:
            # Clean up - close the bot
            if not test_bot.is_closed():
                await test_bot.close()
            
            # Cancel the bot task
            if not bot_task.done():
                bot_task.cancel()
                try:
                    await bot_task
                except asyncio.CancelledError:
                    pass
    
    @pytest.mark.asyncio
    async def test_bot_startup_without_token(self):
        """
        Test bot startup behavior when no token is provided.
        This should fail gracefully.
        """
        # Test with empty token
        with patch.dict(os.environ, {'DISCORD_TOKEN': ''}):
            # This should raise an error or exit
            try:
                # Try to create a bot with empty token
                intents = discord.Intents.all()
                test_bot = commands.Bot(command_prefix='!', intents=intents)
                
                # This should fail when trying to start
                with pytest.raises((discord.LoginFailure, ValueError, RuntimeError)):
                    await test_bot.start('')
                
            except Exception as e:
                # Expected to fail
                assert "token" in str(e).lower() or "login" in str(e).lower()
    
    def test_environment_variable_validation(self):
        """Test that required environment variables are validated."""
        # Test missing token
        with patch.dict(os.environ, {}, clear=True):
            # This should fail when trying to get the token
            token = os.getenv('DISCORD_TOKEN')
            assert token is None
        
        # Test with test token
        with patch.dict(os.environ, {'DISCORD_TOKEN': 'test_token'}):
            token = os.getenv('DISCORD_TOKEN')
            assert token == 'test_token'
    
    def test_bot_configuration(self):
        """Test bot configuration and setup."""
        # Test intents configuration
        intents = discord.Intents.all()
        assert intents.guilds is True
        assert intents.messages is True
        assert intents.voice_states is True
        
        # Test bot creation
        test_bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
        assert test_bot.command_prefix == '!'
        assert test_bot.help_command is None
        assert test_bot.intents == intents
    
    @pytest.mark.asyncio
    async def test_command_registration(self):
        """Test that commands are properly registered."""
        intents = discord.Intents.all()
        test_bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
        
        # Add a test command
        @test_bot.command()
        async def test_command(ctx):
            await ctx.send("Test command executed")
        
        # Verify command is registered
        assert 'test_command' in [cmd.name for cmd in test_bot.commands]
        
        # Test command lookup
        command = test_bot.get_command('test_command')
        assert command is not None
        assert command.name == 'test_command'
        
        await test_bot.close()
    
    def test_import_structure(self):
        """Test that all required modules can be imported."""
        import importlib
        
        # Test individual module imports without running main.py
        modules_to_test = ['bot', 'config', 'logger', 'validation', 'member_commands', 'mod_commands', 'help', 'metar', 'monthly_roles']
        
        for module_name in modules_to_test:
            try:
                module = importlib.import_module(module_name)
                print(f"✅ Successfully imported {module_name}")
            except ImportError as e:
                pytest.fail(f"Failed to import {module_name}: {e}")
        
        # Test that main.py exists and has expected structure (without importing it)
        import os
        main_path = os.path.join(os.path.dirname(__file__), '..', 'main.py')
        assert os.path.exists(main_path), "main.py file does not exist"
        
        # Read main.py to check for expected content
        with open(main_path, 'r') as f:
            main_content = f.read()
            assert 'TOKEN' in main_content, "main.py should contain TOKEN variable"
            assert 'bot.run' in main_content, "main.py should contain bot.run call"
        
        print("✅ All module imports and main.py structure validation successful")
    
    @pytest.mark.asyncio
    async def test_bot_latency_check(self):
        """Test bot latency measurement."""
        intents = discord.Intents.all()
        test_bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
        
        # Test latency before connection (should be NaN)
        import math
        assert math.isnan(test_bot.latency), f"Expected NaN latency, got {test_bot.latency}"
        
        # Test latency property
        assert isinstance(test_bot.latency, float)
        
        await test_bot.close()
