import logging


class AwsPy:
    """
    Internal class to act as a common base for AWS services configuration
    """

    def __init__(
        self, raise_errors: bool = True, logger: logging.Logger = None
    ) -> None:
        """
        Configure instance
        :param raise_errors: Bool, halt execution and raise exceptions if True
        :param logger: Python logging instance to log to
        """

        self._raise_errors = raise_errors
        if logger:
            self._logger = logger
        else:
            self._logger = logging.getLogger(__name__)
