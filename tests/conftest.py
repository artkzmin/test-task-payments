# ruff: noqa: E402 F403
from dotenv import load_dotenv

load_dotenv(".test.env", override=True)

import pytest
import logging
from httpx import AsyncClient

from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


from src.api.app import app
from src.config import settings
from src.database import BaseOrm, engine_null_pool
from src.models import *
from src.api.dependencies import get_db
from src.schemes import (
    UserAddRequest,
    UserRoleEnum,
    UserAuthRequest,
    TransactionAddRequest,
)
from src.services import AuthService


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode() -> None:
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> DBManager:
    async with DBManager(async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function", autouse=True)
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode) -> None:
    logging.info("Начало инициализации БД")
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.drop_all)
        await conn.run_sync(BaseOrm.metadata.create_all)
    logging.info("БД успешно создана")


@pytest.fixture(scope="session", autouse=True)
async def register_common_user(setup_database) -> None:
    common_user = UserAddRequest(
        email=settings.COMMON_EMAIL,
        role=UserRoleEnum.COMMON,
        name=settings.COMMON_NAME,
        surname=settings.COMMON_SURNAME,
        patronymic=settings.COMMON_PATRONYMIC,
        password=settings.COMMON_PASSWORD,
    )
    async with DBManager(async_session_maker_null_pool) as db:
        common_user = await AuthService(db).register_user(common_user)
    assert common_user


@pytest.fixture(scope="session", autouse=True)
async def register_admin_user(setup_database, register_common_user) -> None:
    admin = UserAddRequest(
        email=settings.ADMIN_EMAIL,
        role=UserRoleEnum.ADMIN,
        name=settings.ADMIN_NAME,
        surname=settings.ADMIN_SURNAME,
        patronymic=settings.ADMIN_PATRONYMIC,
        password=settings.ADMIN_PASSWORD,
    )
    async with DBManager(async_session_maker_null_pool) as db:
        admin = await AuthService(db).register_user(admin)
    assert admin


@pytest.fixture(scope="session")
async def authenticated_admin_user_ac(ac, register_admin_user) -> AsyncClient:
    user = UserAuthRequest(email=settings.ADMIN_EMAIL, password=settings.ADMIN_PASSWORD)
    response = await ac.post("/auth/login", json=user.model_dump())
    assert response.status_code == 200
    assert ac.cookies["access_token"]
    assert isinstance(ac.cookies["access_token"], str)
    yield ac


@pytest.fixture(scope="function")
async def authenticated_common_user_ac(ac, register_common_user) -> AsyncClient:
    user = UserAuthRequest(
        email=settings.COMMON_EMAIL, password=settings.COMMON_PASSWORD
    )
    response = await ac.post("/auth/login", json=user.model_dump())
    assert response.status_code == 200
    assert ac.cookies["access_token"]
    assert isinstance(ac.cookies["access_token"], str)
    yield ac


@pytest.fixture(scope="session")
async def create_transaction(ac, register_common_user) -> None:
    transaction = TransactionAddRequest(
        amount="100",
        transaction_id="5eae174f-7cd0-472c-bd36-35660f00132b",
        signature="7b47e41efe564a062029da3367bde8844bea0fb049f894687cee5d57f2858bc8",
        user_id=1,
        account_id=1,
    )
    response = await ac.post("/transaction/", json=transaction.model_dump())
    assert response.status_code == 200
