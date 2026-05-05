from api_tests.clients.base_client import BaseClient

class JsonPlaceholderClient(BaseClient):

    def __init__(self):
        super().__init__("https://jsonplaceholder.typicode.com")

    def get_post(self, post_id: int):
        return self.get(f'/posts/{post_id}')

    def create_post(self, payload: dict):
        return self.post("/posts", json=payload)

    def update_post(self, post_id: int, payload: dict):
        return self.put(f'/posts/{post_id}', json=payload)

    def delete_post(self, post_id: int):
        return self.delete(f'/posts/{post_id}')
