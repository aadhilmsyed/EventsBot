# EventsBot Test Suite

This directory contains a comprehensive test suite for the EventsBot Discord bot. The test suite uses pytest and provides extensive coverage of all major bot functionality.

## Test Structure

### Test Files

- `conftest.py` - Pytest configuration and shared fixtures
- `test_validation.py` - Tests for input validation and sanitization
- `test_logger.py` - Tests for the logging system
- `test_member_commands.py` - Tests for member-accessible commands
- `test_mod_commands.py` - Tests for moderator commands
- `test_flight_logs.py` - Tests for flight logging functionality
- `test_monthly_roles.py` - Tests for role management system
- `test_help.py` - Tests for help command system
- `test_bot.py` - Tests for core bot functionality
- `test_main.py` - Tests for main application entry point
- `test_events_bot.py` - Legacy test file (kept for reference)

### Test Coverage

The test suite covers:

1. **Input Validation** - All validation functions in `validation.py`
2. **Logging System** - Logger class functionality
3. **Member Commands** - All user-accessible commands
4. **Moderator Commands** - All staff commands with proper role checks
5. **Flight Logging** - Voice channel monitoring and event tracking
6. **Role Management** - Monthly role updates and calculations
7. **Help System** - Dynamic help commands based on user roles
8. **Bot Events** - Core bot event handlers
9. **Main Application** - Environment setup and module imports

## Running Tests

### Prerequisites

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running All Tests

```bash
pytest tests/
```

### Running Specific Test Files

```bash
pytest tests/test_validation.py
pytest tests/test_member_commands.py
```

### Running with Coverage

```bash
pytest tests/ --cov=. --cov-report=html
```

### Running Specific Test Classes

```bash
pytest tests/test_validation.py::TestSanitizeEventName
```

### Running Specific Test Methods

```bash
pytest tests/test_validation.py::TestSanitizeEventName::test_valid_event_name
```

## Test Configuration

### Environment Variables

The tests use mock environment variables defined in `conftest.py`:

- `DISCORD_TOKEN` - Bot token
- `GUILD_ID` - Discord server ID
- `LOG_CHANNEL_ID` - Logging channel ID
- `MODERATOR_ROLE_ID` - Moderator role ID
- `CAPTAIN_ROLE_ID` - Captain role ID
- `FIRST_OFFICER_ROLE_ID` - First Officer role ID
- `FIRST_CLASS_ROLE_ID` - First Class role ID
- `BUSINESS_CLASS_ROLE_ID` - Business Class role ID
- `PREMIUM_ECONOMY_ROLE_ID` - Premium Economy role ID
- `ECONOMY_CLASS_ROLE_ID` - Economy Class role ID
- `SERVER_BOOSTER_ROLE_ID` - Server Booster role ID

### Fixtures

The test suite provides several reusable fixtures:

- `mock_guild` - Mock Discord guild
- `mock_channel` - Mock text channel
- `mock_voice_channel` - Mock voice channel
- `mock_member` - Mock Discord member
- `mock_role` - Mock Discord role
- `mock_context` - Mock command context
- `mock_bot` - Mock Discord bot
- `mock_logger` - Mock logger
- `mock_config` - Mock configuration
- `mock_flight_hours_manager` - Mock flight hours manager
- `mock_voice_state` - Mock voice state
- `mock_scheduled_event` - Mock scheduled event

## Test Categories

### Unit Tests

- Individual function testing
- Input validation
- Role calculations
- Command logic

### Integration Tests

- Command execution with proper mocking
- Event handling
- Role management workflows

### Async Tests

- All Discord bot interactions are properly tested with async/await
- Voice state updates
- Scheduled event handling

## CI/CD Integration

The test suite is integrated with GitHub Actions CI/CD pipeline:

1. **Test Job** - Runs tests on Python 3.9, 3.10, and 3.11
2. **Lint Job** - Code formatting and style checks
3. **Security Job** - Security vulnerability scanning

## Writing New Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### Example Test Structure

```python
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

class TestNewFeature:
    """Test cases for new feature."""
    
    @pytest.mark.asyncio
    async def test_feature_success(self, mock_context, mock_config):
        """Test successful feature execution."""
        # Arrange
        mock_config.some_setting = "value"
        
        # Act
        with patch('module.config', mock_config):
            from module import new_command
            await new_command(mock_context)
        
        # Assert
        mock_context.send.assert_called()
```

### Best Practices

1. Use descriptive test names
2. Follow AAA pattern (Arrange, Act, Assert)
3. Mock external dependencies
4. Test both success and failure cases
5. Use appropriate fixtures
6. Add docstrings to test methods
7. Group related tests in classes

## Debugging Tests

### Verbose Output

```bash
pytest tests/ -v
```

### Stop on First Failure

```bash
pytest tests/ -x
```

### Run Last Failed Tests

```bash
pytest tests/ --lf
```

### Debug Mode

```bash
pytest tests/ --pdb
```

## Coverage Goals

- **Minimum Coverage**: 80%
- **Target Coverage**: 90%+
- **Critical Paths**: 100% coverage for validation, logging, and core bot functionality

## Maintenance

### Adding New Commands

1. Create test file: `test_new_command.py`
2. Add comprehensive test cases
3. Update this README
4. Ensure CI passes

### Updating Existing Tests

1. Maintain backward compatibility
2. Update fixtures if needed
3. Update documentation
4. Run full test suite

## Troubleshooting

### Common Issues

1. **Import Errors** - Ensure all modules are properly mocked
2. **Async Issues** - Use `@pytest.mark.asyncio` decorator
3. **Mock Issues** - Verify mock setup and assertions
4. **Environment Issues** - Check environment variable setup

### Getting Help

1. Check test output for specific error messages
2. Review fixture setup in `conftest.py`
3. Verify mock configurations
4. Run individual tests to isolate issues
