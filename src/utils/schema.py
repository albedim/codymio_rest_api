
SCHEMA = [
    {
        "name": "SIGNIN_USER",
        "schema": {
            "email": str,
            "password": str
        }
    },
    {
        "name": "GITHUB_ACCESS",
        "schema": {
            "code": str
        }
    },
    {
        "name": "CHANGE",
        "schema": {
            "email": str,
            "complete_name": str,
            "password": str
        }
    },
    {
        "name": "CHANGE_PASSWORD",
        "schema": {
            "user_id": int,
            "password": str
        }
    }
]