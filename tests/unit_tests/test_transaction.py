import json

from src.schemes import TransactionAddRequest


async def test_transaction_me(authenticated_common_user_ac) -> None:
    response = await authenticated_common_user_ac.get("/transaction/me")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_create_transaction(authenticated_common_user_ac) -> None:
    with open("tests/mock/mock_transactions.json", encoding="utf-8") as f:
        transactions = json.load(f)
    transactions = [TransactionAddRequest(**t) for t in transactions]
    for t in transactions:
        response = await authenticated_common_user_ac.post(
            "/transaction/", json=t.model_dump()
        )
        assert response.status_code == 200

    for t in transactions:
        response = await authenticated_common_user_ac.post(
            "/transaction/", json=t.model_dump()
        )
        assert response.status_code == 403
    response = await authenticated_common_user_ac.post(
        "/transaction/",
        json={
            "transaction_id": "999",
            "user_id": 999,
            "account_id": 999,
            "amount": 999,
            "signature": "999",
        },
    )
    assert response.status_code == 409
