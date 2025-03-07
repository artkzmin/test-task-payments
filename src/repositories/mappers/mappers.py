from src.repositories.mappers.base import DataMapper
from src.schemes import Account, Transaction, User, UserWithReals
from src.models import AccountOrm, TransactionOrm, UserOrm


class AccountDataMapper(DataMapper):
    db_model = AccountOrm
    schema = Account


class TransactionDataMapper(DataMapper):
    db_model = TransactionOrm
    schema = Transaction


class UserDataMapper(DataMapper):
    db_model = UserOrm
    schema = User


class UserWithRealsDataMapper(UserDataMapper):
    schema = UserWithReals
