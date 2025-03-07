from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound

from src.repositories.base import BaseRepository
from src.repositories.mappers import TransactionDataMapper
from src.models import TransactionOrm, AccountOrm
from src.schemes import Transaction
from src.exceptions import ObjectNotFoundException


class TransactionRepository(BaseRepository):
    model: TransactionOrm = TransactionOrm
    mapper: TransactionDataMapper = TransactionDataMapper

    # Функция для фильтрации по столбцам других таблиц
    async def get_transaction_by_user_id(self, user_id: int) -> list[Transaction]:
        query = (
            select(self.model)
            .options(selectinload(self.model.account))
            .filter(AccountOrm.user_id == user_id)
        )
        try:
            result = await self.session.execute(query)
        except NoResultFound:
            raise ObjectNotFoundException

        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
