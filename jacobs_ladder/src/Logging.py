import logging

import logging

def setup_logging(app_name: str, level: int = 20) -> logging.Logger:
    """Setup logging for the MidiManager class

    Args:
        app_name (str): the name of the app and subsequently the name of the logfile
        level (int, optional): 10: DEBUG, 20: INFO, 30: WARNING, 40: ERROR, 50: CRITICAL. Defaults to 20.

    Returns:
        logging.Logger
    """
    log_filename = f"./jacobs_ladder/logs/{app_name}.log"
    
    loglevel = logging.getLevelName(level)
    
    # Create a logger
    logger = logging.getLogger(app_name)
    logger.setLevel(loglevel)
    
    # Create file handler with UTF-8 encoding
    file_handler = logging.FileHandler(log_filename, mode="w", encoding="utf-8")
    file_handler.setLevel(loglevel)
    
    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(file_handler)
    
    # Prevent log messages from being propagated to the root logger
    logger.propagate = False
    
    return logger
