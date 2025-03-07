from src.exceptions.object import ObjectAlreadyExistsException, ObjectNotFoundException


class AccountAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Счет уже существует"


class AccountNotFoundException(ObjectNotFoundException):
    detail = "Счет не найден"
