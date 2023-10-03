import logging
import logging.handlers
from json_formatter import JsonFormatter

# Create a Logger Object
logger = logging.getLogger('events_bot_logger')
logger.setLevel(logging.INFO)

# Create a JSON file handler to write log messages to a file with rotation
file_handler = logging.handlers.RotatingFileHandler('log_file.json', maxBytes = 5 * (2**20), backupCount = 1)

# Create a custom JSON formatter
json_formatter = JsonFormatter()

# Set the formatter for the file handler
file_handler.setFormatter(json_formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)
