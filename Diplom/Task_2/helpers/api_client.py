import requests
import allure
import pytest
from typing import Dict, Any, List


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    @allure.step("Проверить статус код ответа")
    def check_response_status(self, response: requests.Response, expected_status: int):
        """Проверка статуса ответа"""
        actual_status = response.status_code
        assert actual_status == expected_status, \
            f"Ожидался статус {expected_status}, получен {actual_status}. Ответ: {response.text}"

    @allure.step("Проверить поле success в ответе")
    def check_response_success(self, response: requests.Response, expected_success: bool):
        """Проверка поля success в ответе"""
        try:
            json_data = response.json()
            actual_success = json_data.get("success")
            assert actual_success == expected_success, \
                f"Ожидался success={expected_success}, получен {actual_success}"
        except ValueError:
            pytest.fail(f"Response is not valid JSON: {response.text}")

    @allure.step("Создать пользователя")
    def create_user(self, user_data: Dict[str, Any]) -> requests.Response:
        """Создание пользователя"""
        return requests.post(f"{self.base_url}/auth/register", json=user_data, timeout=10)

    @allure.step("Выполнить вход пользователя")
    def login_user(self, credentials: Dict[str, Any]) -> requests.Response:
        """Логин пользователя"""
        return requests.post(f"{self.base_url}/auth/login", json=credentials, timeout=10)

    @allure.step("Создать заказ")
    def create_order(self, ingredients: List[str], token: str = None) -> requests.Response:
        """Создание заказа"""
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = token
            
        return requests.post(
            f"{self.base_url}/orders",
            json={"ingredients": ingredients},
            headers=headers,
            timeout=10
        )