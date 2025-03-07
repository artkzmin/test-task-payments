from src.exceptions.base import BaseException


class IncorrectPasswordException(BaseException):
    detail = "Неверный пароль"


class IncorrectTokenException(BaseException):
    detail = "Некорретный токен"


class TokenExpiredException(BaseException):
    detail = "Токен истёк"
