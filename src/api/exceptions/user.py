from src.api.exceptions.base import BaseHTTPException, status
from src.api.exceptions.object import ObjectAlreadyExistsHTTPException


class UserNotFoundHTTPException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не найден"


class CommonUserNotFoundHTTPException(UserNotFoundHTTPException):
    detail = "Обычный пользователь не найден"


class UserAlreadyExistsHTTPException(ObjectAlreadyExistsHTTPException):
    detail = "Пользователь с такой почтой уже существует"


class NoAccessHTTPException(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Нет доступа"


class UserNotAdminHTTPException(NoAccessHTTPException):
    detail = "Пользователь не является администратором, доступ ограничен"


class UserNotCommonHTTPException(NoAccessHTTPException):
    detail = "Пользователь не является обычным пользователем, доступ ограничен"
