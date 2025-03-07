async def test_account_me(authenticated_common_user_ac) -> None:
    response = await authenticated_common_user_ac.get("/account/me")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
