from uuid import uuid4


def build_user_payload() -> dict:
    unique_id = uuid4().hex[:8]

    username = f'api_user_{unique_id}'

    return {
        'username': username,
        'email': f'{username}@example.com',
        'password': 'StrongPassword123!',
        'password_confirmation': 'StrongPassword123!',
    }
