"""Файл с исключениями."""

class SendMessageError(Exception):
    pass

class ApiRequestError(Exception):
    pass

class ApiResponseTypeError(Exception):
    pass

class HwStatusUnknown(Exception):
    pass