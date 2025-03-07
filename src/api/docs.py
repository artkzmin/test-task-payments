# Модуль для строк документации API

from src.schemes import UserRoleEnum


class DocsStrings:
    ABOUT_CURRENT_AUTH_USER = "Данные текущего аутентифицированного пользователя берутся из токена доступа **access_token**"
    JUST_COMMON_USER_ACCESS = "Доступ к запросу есть только у пользователей с ролью **common**"
    JUST_ADMIN_USER_ACCESS = "Доступ к запросу есть только у пользователей с ролью **admin**"
    USER_ID_DESCRIPTION = "Уникальный идентификатор пользователя"
    USER_ID_TITLE = "ID пользователя"


class DocsExamples:
    USER_EXAMPLES = {
        "1": {
            "summary": "Обычный пользователь Игорь",
            "value": {
                "name": "Игорь",
                "surname": "Игорев",
                "patronymic": "Игоревич",
                "email": "igor@igor.com",
                "password": "UBVBPD?qCKY$JVE352D#",
                "role": UserRoleEnum.COMMON,
            },
        },
        "2": {
            "summary": "Обычный пользователь Андрей",
            "value": {
                "name": "Андрей",
                "surname": "Андреев",
                "patronymic": "Андреевич",
                "email": "andrey@andrey.com",
                "password": "l45GIJh5OHJh8q06{vv1",
                "role": UserRoleEnum.COMMON,
            },
        },
        "3": {
            "summary": "Администратор Вадим",
            "value": {
                "name": "Вадим",
                "surname": "Вадимов",
                "patronymic": "Вадимович",
                "email": "vadim@vadim.com",
                "password": "bInoP{yG{J}5TR@ba6O{",
                "role": UserRoleEnum.ADMIN,
            },
        },
    }

    TRANSACTION_EXAMPLES = {
        "1": {
            "summary": "Транзакция 5eae174f-7cd0-472c-bd36-35660f00132b",
            "value": {
                "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
                "user_id": 1,
                "account_id": 1,
                "amount": 100,
                "signature": "7b47e41efe564a062029da3367bde8844bea0fb049f894687cee5d57f2858bc8",
            },
        }
    }
