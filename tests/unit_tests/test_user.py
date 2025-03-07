async def test_get_users(authenticated_admin_user_ac) -> None:
    response = await authenticated_admin_user_ac.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_user(authenticated_admin_user_ac) -> None:
    response = await authenticated_admin_user_ac.get("/user/1")
    assert response.status_code == 200

    response = await authenticated_admin_user_ac.get("/user/999")
    assert response.status_code == 404


async def test_crud_user(authenticated_admin_user_ac) -> None:
    user = {
        "email": "temp@temp.com",
        "name": "name",
        "surname": "surname",
        "patronymic": "patronymic",
        "role": "common",
        "password": "password",
    }
    response = await authenticated_admin_user_ac.post("/user/", json=user)
    print(response.json())
    assert response.status_code == 200
    id = response.json()["id"]

    user["name"] = "name_2"
    response = await authenticated_admin_user_ac.put(f"/user/{id}", json=user)
    assert response.status_code == 200

    user["name"] = "name_3"
    response = await authenticated_admin_user_ac.patch(f"/user/{id}", json=user)
    assert response.status_code == 200

    response = await authenticated_admin_user_ac.delete(f"/user/{id}")
    assert response.status_code == 200
