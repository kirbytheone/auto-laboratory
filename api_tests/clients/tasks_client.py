from api_tests.clients.base_client import BaseClient


class TasksClient(BaseClient):
    def list_tasks(self):
        return self.get('/api/tasks/')
