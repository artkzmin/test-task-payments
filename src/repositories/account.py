from src.repositories.base import BaseRepository
from src.repositories.mappers import AccountDataMapper
from src.models import AccountOrm


class AccountRepository(BaseRepository):
    model: AccountOrm = AccountOrm
    mapper: AccountDataMapper = AccountDataMapper
