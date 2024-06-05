import logging

def setup_logger():
    # Create logger
    logger = logging.getLogger('employees_logger')
    logger.setLevel(logging.INFO)  # Set log level to INFO or desired level

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create file handler
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.INFO)  # Set log level to INFO or desired level
    file_handler.setFormatter(formatter)

    # Add file handler to logger
    logger.addHandler(file_handler)

    return logger