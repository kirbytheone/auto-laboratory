from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class UserData:
    username: str
    email: str
    password: str

VALID_TEST_PASSWORD = 'StrongTestPassword123!'

def generate_user_data(password: str = VALID_TEST_PASSWORD) -> UserData:
    unique_id = uuid4().hex[:8]
    username = f'pw_user_{unique_id}'

    return UserData(
        username=username,
        email=f'{username}@example.com',
        password=password,
    )