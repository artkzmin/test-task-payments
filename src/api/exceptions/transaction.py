from src.api.exceptions.base import BaseHTTPException, status


class IncorrectTransactionHTTPException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Некорректная транзакция"


class NotUniqueTransactionHTTPException(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Транзакция уже существует"
