import traceback

from .exceptions import CustomException

class ExceptionsService:

    @staticmethod
    def traceback(exception: Exception) -> str:
        if exception is None:
            return ""
        return ''.join(traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__))

    @staticmethod
    def extract_full_exceptions(custom_ex: CustomException):
        result = ''.join(traceback.format_exception(etype=type(custom_ex), value=custom_ex, tb=custom_ex.__traceback__))
        if hasattr(custom_ex, 'inner_exception'):
            result += "\n" + ExceptionsService.extract_full_exceptions(custom_ex.inner_exception)
        return result
