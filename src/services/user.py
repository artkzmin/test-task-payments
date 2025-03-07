from src.services.base import BaseService
from src.schemes import (
    UserAdd,
    UserWithReals,
    User,
    UserAddRequest,
    UserPatchRequest,
    UserRoleEnum,
    UserPatch,
    UserWithFullName,
)
from src.exceptions import (
    ObjectNotFoundException,
    UserNotFoundException,
    ObjectAlreadyExistsException,
    UserAlreadyExistsException,
)
from src.services.auth import AuthService


class UserService(BaseService):
    async def get_user(self, id: int) -> User:
        try:
            return await self.db.user.get_one(id=id)
        except ObjectNotFoundException as ex:
            raise UserNotFoundException from ex

    async def get_user_with_full_name(self, id: int) -> UserWithFullName:
        try:
            user = await self.get_user(id)
        except UserNotFoundException as ex:
            raise ex
        return UserWithFullName(
            **user.model_dump(),
            full_name=f"{user.surname} {user.name} {user.patronymic}",
        )

    async def get_user_with_accounts(self, id: int) -> UserWithReals:
        try:
            return await self.db.user.get_one_filtered_with_reals(
                id=id, role=UserRoleEnum.COMMON
            )
        except ObjectNotFoundException as ex:
            raise UserNotFoundException from ex

    async def get_all_common_users_with_accounts(self) -> list[UserWithReals]:
        return await self.db.user.get_filtered_with_reals(role=UserRoleEnum.COMMON)

    async def add_user(self, data: UserAdd) -> User:
        try:
            user = await self.db.user.add_user(data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex
        return user

    async def delete_user(self, id: int) -> None:
        await self.db.user.delete(id=id)
        await self.db.commit()

    async def check_user_role(self, id: int, role: str) -> bool:
        try:
            user = await self.get_user(id)
            if user.role == role:
                return True
            return False
        except UserNotFoundException as ex:
            raise ex

    async def edit_user(self, id: int, data: UserAddRequest) -> None:
        hashed_password = AuthService(self.db).hash_password(data.password)
        new_data = UserAdd(hashed_password=hashed_password, **data.model_dump())
        await self.db.user.edit(data=new_data, id=id)
        await self.db.commit()

    async def partial_edit_user(self, id: int, data: UserPatchRequest) -> None:
        new_data = UserPatch(**data.model_dump(exclude_unset=True))
        if data.password:
            hashed_password = AuthService(self.db).hash_password(data.password)
            new_data.hashed_password = hashed_password
        await self.db.user.edit(data=new_data, exclude_unset=True, id=id)
        await self.db.commit()

    async def check_user_exists(self, id: int):
        try:
            await self.get_user(id)
        except UserNotFoundException as ex:
            raise ex
