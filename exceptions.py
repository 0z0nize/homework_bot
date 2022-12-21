"""Файл с исключениями."""
class SendMessageError(Exception):
    pass

class RequestError(Exception):
    pass

class ApiResponseTypeError(Exception):
    pass

class HwStatusUnknown(Exception):
    pass