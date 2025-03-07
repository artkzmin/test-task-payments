from src.services import AuthService
from src.schemes import UserAuthRequest
from src.config import settings


def test_create_access_token(db) -> None:
    data = {"user_id": 1}
    jwt_token = AuthService(db).create_access_token(data)
    assert jwt_token
    assert isinstance(jwt_token, str)


async def test_login_logout(ac) -> None:
    response = await ac.post(
        "/auth/login", json={"email": "not_email", "password": "1234"}
    )
    assert response.status_code == 422

    user = UserAuthRequest(email=settings.ADMIN_EMAIL, password=settings.ADMIN_PASSWORD)
    response = await ac.post("/auth/login", json=user.model_dump())
    assert response.status_code == 200
    assert ac.cookies["access_token"]
    assert isinstance(ac.cookies["access_token"], str)

    response = await ac.post("/auth/logout")
    assert response.status_code == 200
    assert not ac.cookies.get("access_token")

    user = UserAuthRequest(
        email=settings.ADMIN_EMAIL, password=f"{settings.ADMIN_PASSWORD}1"
    )
    response = await ac.post("/auth/login", json=user.model_dump())
    assert response.status_code == 401
