import logging
from colorlog import ColoredFormatter


class Logger:
    """
    A simple console logger class that outputs colorized logs.
    """

    def __init__(self, name: str, verbosity_level: int = 0) -> None:
        """
        Initialize a colorized console logger.

        Parameters:
        name (str): Name of the logger which is typically the name of the module creating the logger.
        verbosity_level (int): The verbosity level of the logger. 0 = ERROR, 1 = WARNING, 2 = INFO, 3 = DEBUG.
        """
        # Create a logger
        self.logger = logging.getLogger(name)
        if verbosity_level == 1:
            self.logger.setLevel(logging.WARNING)
        if verbosity_level == 2:
            self.logger.setLevel(logging.INFO)
        elif verbosity_level >= 3:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.ERROR)

        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Create colored formatter
        formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s => [%(levelname)s]%(reset)s %(white)s%(message)s",
            datefmt="%H:%M:%S",
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
            secondary_log_colors={},
            style="%",
        )

        # Add formatter to console handler
        ch.setFormatter(formatter)

        # Add ch to logger
        self.logger.addHandler(ch)

    def get_logger(self) -> logging.Logger:
        """
        Returns the configured logger with colorized output.
        """
        return self.logger


if __name__ == "__main__":
    logger = Logger(__name__).get_logger()
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
