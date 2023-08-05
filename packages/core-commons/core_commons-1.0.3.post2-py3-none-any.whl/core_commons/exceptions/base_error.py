class BaseError(Exception):
    """Base error with self display, map logic, and optional encapsulation."""

    def __init__(self, message, code, caused_by=None):
        """
        Instantiates a new default error.

        :param str message: Error message.
        :param str or int code: Error code.
        :param Exception caused_by: The exception that this one wraps, if any.
        """
        Exception.__init__(self)
        self.message = message
        self.code = code
        self.caused_by = caused_by

    def __str__(self):
        """
        Generates an string error output for the exception.

        :return: The exception as an error string.
        :rtype: str
        """
        if self.caused_by is not None:
            return "(%s): %s\nCaused by: %s" % (self.__class__.__name__, self.message, str(self.caused_by))
        else:
            return "(%s): %s" % (self.__class__.__name__, self.message)

    def to_dict(self):
        """
        Retrieves an data representation of the error.

        :return: The exception as error data.
        :rtype: dict[str, Any]
        """
        err_dict = {"type": self.__class__.__name__, "message": self.message, "code": self.code}
        if self.caused_by is not None:
            err_dict["cause"] = self.caused_by.to_dict() if hasattr(self.caused_by, "to_dict") else str(self.caused_by)
        return err_dict
