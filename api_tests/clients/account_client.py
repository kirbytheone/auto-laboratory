from api_tests.clients.base_client import BaseClient


class AccountClient(BaseClient):
    def register(self, payload: dict):
        return self.post('/api/auth/register/', json=payload)

    def obtain_token_pair(self, username: str, password: str):
        return self.post(
            '/api/auth/token',
            json={
                'username': username,
                'password': password,
            },
        )

    def refresh_access_token(self, refresh_token: str):
        return self.post(
            '/api/auth/token/refresh/',
            json={
                'refresh': refresh_token,
            },
        )
