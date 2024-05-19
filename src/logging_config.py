import logging
import os

# Set the logging level
LOGGING_LEVEL = logging.INFO

# Set the logging file path
LOGGING_FILE = 'app.log'

# Create a logger
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(LOGGING_LEVEL)

# Create a file handler
file_handler = logging.FileHandler(LOGGING_FILE)
file_handler.setLevel(LOGGING_LEVEL)

# Create a formatter and set the formatter for the file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

def get_logger():
    return logger