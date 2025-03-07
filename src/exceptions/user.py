from src.exceptions.base import BaseException
from src.exceptions.object import ObjectAlreadyExistsException, ObjectNotFoundException


class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Пользователь уже существует"


class UserNotRegisteredException(BaseException):
    detail = "Пользователь не зарегистрирован"


class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь не найден"
