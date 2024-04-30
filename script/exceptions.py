from script import logger


class ElementInteractionError(Exception):
    """Custom exception for handling specific errors."""

    def __init__(self, message="An error occurred."):
        self.message = message
        super().__init__(self.message)
        self.logger = logger.setup_logger(__name__, './output/browser_action.log')

    def log_error(self, message: str):
        """Log the error message."""
        self.logger.error(message)
