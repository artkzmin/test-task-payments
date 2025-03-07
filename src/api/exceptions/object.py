from src.api.exceptions.base import BaseHTTPException, status


class ObjectAlreadyExistsHTTPException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Объект уже существует"
