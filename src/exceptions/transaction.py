from src.exceptions.base import BaseException
from src.exceptions.object import ObjectAlreadyExistsException, ObjectNotFoundException


class IncorrectTransactionException(BaseException):
    detail = "Некорректная транзакция"


class TransactionAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Транзакция уже существует"


class TransactionNotFoundException(ObjectNotFoundException):
    detail = "Транзакция не найдена"
