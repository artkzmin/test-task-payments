import logging
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import select
from pydantic import EmailStr

from src.repositories.base import BaseRepository
from src.repositories.mappers import UserDataMapper, UserWithRealsDataMapper
from src.models import UserOrm
from src.schemes import UserWithReals, User, UserAdd, UserWithHashedPassword
from src.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException


class UserRepository(BaseRepository):
    model: UserOrm = UserOrm
    mapper: UserDataMapper = UserDataMapper

    async def get_filtered_with_reals(self, **filter_by) -> list[UserWithReals]:
        query = select(self.model).options(selectinload(self.model.accounts)).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [
            UserWithRealsDataMapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_one_filtered_with_reals(self, **filter_by) -> UserWithReals:
        try:
            return (await self.get_filtered_with_reals(**filter_by))[0]
        except IndexError:
            raise ObjectNotFoundException

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return UserWithHashedPassword.model_validate(model)

    async def add_user(self, data: UserAdd) -> User:
        try:
            return await self.add(data)
        except IntegrityError as ex:
            logging.exception(f"Не удалось добавить данные в БД, входные данные={data}")
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            logging.exception(f"Незнакомая ошибка, входные данные={data}")
            raise ex
