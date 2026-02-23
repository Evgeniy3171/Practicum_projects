import requests

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None

    def create_order(self, ingredients, token=None):
        headers = {'Authorization': token} if token else {}
        response = requests.post(
            f"{self.base_url}/api/orders",
            json={"ingredients": ingredients},
            headers=headers
        )
        return response.json()