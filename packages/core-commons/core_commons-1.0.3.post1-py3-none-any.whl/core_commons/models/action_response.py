import json


class ActionResponse:
    """
    This class is the serialized response for actions, that the automation system should return. It's based on the
    JSend standard from the project (https://github.com/omniti-labs/jsend).
    """

    SUCCESS = "success"
    FAIL = "fail"
    ERROR = "error"

    def __init__(self, status, data=None, code=None, message=None):
        """
        Generates a new Action Response. Not be used directly, use the convenience methods success, fail and error.

        :param str status: The status of the action. Can be `success`, `fail` or `error`.
        :param dict[str, Any] data: The data to send with the response. Can be None. Must be json serializable.
        :param str code: Only set if an error is thrown. The error code thrown.
        :param str message: Only set if an error is thrown. The human readable message thrown.
        """
        self.status = status
        self.data = data
        self.code = code
        self.message = message

    def to_dict(self):
        """
        Retrieves a dictionary action response. If an optional field is None, it will not be in the output.

        :return: The action response as a dictionary.
        :rtype: dict[str, Any]
        """
        if self.status in [ActionResponse.SUCCESS, ActionResponse.FAIL]:
            payload = {
                "status": self.status,
                "data": self.data
            }
        else:
            payload = {"status": self.status}
            if self.message is not None:
                payload["message"] = self.message
            if self.code is not None:
                payload["code"] = self.code
            if self.data is not None:
                payload["data"] = self.data

        return payload

    def to_json(self, tidy=False):
        """
        Retrieves a action response as a json string. If an optional field is None, it will not be in the output.

        :param tidy: If set, the json returned will have spacing and human readable format.
        :return: A json string representation of the action response.
        :rtype: str
        """
        if not tidy:
            return json.dumps(self.to_dict(), separators=(',', ':'))
        else:
            return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def success(cls, data=None):
        """
        Convenience method to generate a success action response.

        :param dict[str, Any] data: The data to send with the response. Can be None. Must be json serializable.
        :return: An action response object with success status.
        :rtype: ActionResponse
        """
        return cls(ActionResponse.SUCCESS, data)

    @classmethod
    def fail(cls, data=None):
        """

        :param dict[str, Any] data: The data to send with the response. Can be None.
        :return: An action response object with fail status.
        :rtype: ActionResponse
        """
        return cls(ActionResponse.FAIL, data)

    @classmethod
    def error(cls, message, code=None, data=None):
        """

        :param str message: Only set if an error is thrown. The human readable message thrown.
        :param str code: The optional error code to throw.
        :param dict[str, Any] data: The optional data to send with the response.
        :return: An action response object with error status.
        :rtype: ActionResponse
        """
        return cls(ActionResponse.ERROR, data, code, message)
