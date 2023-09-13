import logging

# Create a logger object
logger = logging.getLogger('events_bot_logger')

# Set the log level
logger.setLevel(logging.ERROR)  # Log only error messages or higher

# Create a file handler to write log messages to a file
file_handler = logging.FileHandler('bot_error.txt')

# Create a formatter with the desired format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the formatter for the file handler
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)
