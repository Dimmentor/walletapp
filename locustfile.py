from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):

    @task
    def deposit_money(self):
        url = "/api/v1/wallets/123e4567-e89b-12d3-a456-426614174003/operation/"
        payload = {
            "operation_type": "DEPOSIT",
            "amount": 10
        }
        self.client.post(url, json=payload)


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0, 0.5)
    host = "http://127.0.0.1:8000"