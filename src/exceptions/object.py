from src.exceptions.base import BaseException


class ObjectNotFoundException(BaseException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(BaseException):
    detail = "Объект уже существует"
