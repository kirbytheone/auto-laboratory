import requests

class BaseClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _request(self, method: str, endpoint: str, **kwargs):
        url = f'{self.base_url}{endpoint}'

        print(f"\n[REQUEST] {method} {url}")
        if "json" in kwargs:
            print(f'[PAYLOAD] {kwargs["json"]}')

        response = requests.request(method, url, **kwargs)

        print(f'[RESPONSE] Status: {response.status_code}')
        try:
            print(f'[RESPONSE BODY] {response.json()}')
        except Exception:
            print(f'[RESPONSE BODY] Not JSON')

        return response

    def get(self, endpoint: str, **kwargs):
        return self._request('GET', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self._request('POST', endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        return self._request('PUT', endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._request('DELETE', endpoint, **kwargs)
