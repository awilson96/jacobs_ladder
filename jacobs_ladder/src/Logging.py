import logging
from datetime import datetime


def setup_logging(app_name: str) -> logging.Logger:
    log_filename = f"./jacobs_ladder/logs/{app_name}.log"
    
    # Create a logger
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.INFO)
    
    # Create file handler
    file_handler = logging.FileHandler(log_filename, mode="w")
    file_handler.setLevel(logging.INFO)
    
    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(file_handler)
    
    # Prevent log messages from being propagated to the root logger
    logger.propagate = False
    
    return logger