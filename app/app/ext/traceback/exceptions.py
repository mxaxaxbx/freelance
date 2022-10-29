from enum import Enum

class ECustomException(Enum):
    OPERATION_ERROR = 0
    RESOURCE_NOT_FOUND = 1
    INVALID_PARAMETER = 2
    NO_DATABASE_CONNECTION = 3
    QUERY_EXECUTION_ERROR = 4
    INVALID_TRANSFORMATION = 5
    INVALID_TYPE = 6
    INVALID_VALUES = 7
    INVALID_CREDENTIALS = 8
    EMPTY_RESULTS = 9

class CustomException(Exception):

    def __init__(self, _type: ECustomException = ECustomException.OPERATION_ERROR,
                 message: str = "", inner_exception: Exception = None, *args):
        self._type = _type
        self._message = message
        self._inner_exception = inner_exception
        super().__init__(*args)

    @property
    def message(self):
        return self._message

    @property
    def type(self):
        return self._type

    @property
    def inner_exception(self):
        return self._inner_exception

class ResourceNotFoundException(CustomException):

    def __init__(self, message: str = "", inner_exception: Exception = None, *args):
        super(CustomException, self).__init__(ECustomException.RESOURCE_NOT_FOUND, message, inner_exception, *args)
