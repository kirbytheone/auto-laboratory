import requests


class BaseClient:
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def close(self):
        self.session.close()

    def _build_url(self, endpoint: str) -> str:
        return f'{self.base_url}/{endpoint.lstrip('/')}'

    def _request(self, method: str, endpoint: str, **kwargs):
        url = self._build_url(endpoint)

        kwargs.setdefault('timeout', self.timeout)

        response = self.session.request(
            method=method,
            url=url,
            **kwargs,
        )

        print(
            f'[API] {method.upper()} {endpoint} '
            f'-> {response.status_code} '
            f'({response.elapsed.total_seconds():.3f}s)'
        )

        return response

    def get(self, endpoint: str, **kwargs):
        return self._request('GET', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self._request('POST', endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        return self._request('PUT', endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs):
        return self._request('PATCH', endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._request('DELETE', endpoint, **kwargs)
