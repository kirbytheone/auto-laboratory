import requests

class JsonPlaceholderClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def get_post(self, post_id: int):
        url = f'{self.BASE_URL}/posts/{post_id}'
        return requests.get(url)