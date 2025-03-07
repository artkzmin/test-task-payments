from src.api.exceptions.object import ObjectAlreadyExistsHTTPException


class AccountAlreadyExistsHTTPException(ObjectAlreadyExistsHTTPException):
    detail = "Счет уже существует"
