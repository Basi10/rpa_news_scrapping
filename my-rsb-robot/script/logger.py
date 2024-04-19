import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """
    Function to set up a logger with a specified name, log file, and log level.
    
    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.
        level (int, optional): Log level (defaults to INFO).
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.dirname(log_file)
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Add file handler to logger
    logger.addHandler(file_handler)
    
    return logger
