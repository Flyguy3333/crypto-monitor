√import logging

def setup_logger(name, log_file, level=logging.INFO):
    """Function to set up as many loggers as needed"""
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Create a logger for the signal generator
signal_logger = setup_logger('signals', 'logs/signals.log')
