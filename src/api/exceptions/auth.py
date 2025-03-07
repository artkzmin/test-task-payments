from src.api.exceptions.base import BaseHTTPException, status


class UnauthorizedHTTPException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Ошибка авторизации"


class NoAccessTokenHTTPException(UnauthorizedHTTPException):
    detail = "Не предоставлен токен"


class IncorrectPasswordHTTPException(UnauthorizedHTTPException):
    detail = "Пароль неверный"


class UserNotRegisteredHTTPException(UnauthorizedHTTPException):
    detail = "Пользователь не зарегистрирован"


class IncorrectTokenHTTPException(UnauthorizedHTTPException):
    detail = "Некорректный токен"


class TokenExpiredHTTPException(UnauthorizedHTTPException):
    detail = "Срок действия токена истёк"
