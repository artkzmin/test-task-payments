from passlib.context import CryptContext
import jwt
from datetime import datetime, timezone, timedelta

from src.config import settings
from src.services.base import BaseService
from src.schemes.user import UserAddRequest, UserAdd, User
from src.exceptions import (
    UserAlreadyExistsException,
    UserNotRegisteredException,
    IncorrectPasswordException,
    IncorrectTokenException,
    TokenExpiredException,
    ObjectAlreadyExistsException,
)


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenExpiredException

    async def register_user(self, data: UserAddRequest) -> User:
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(hashed_password=hashed_password, **data.model_dump())
        try:
            user = await self.db.user.add_user(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex
        return user

    async def login_user(self, data: UserAddRequest) -> str:
        user = await self.db.user.get_user_with_hashed_password(email=data.email)
        if not user:
            raise UserNotRegisteredException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token({"user_id": user.id})
        return access_token
