import pytest
import allure
from helpers.api_client import ApiClient
from data.urls import Urls
from data.test_data import UserData, ResponseMessages, ErrorCodes


@allure.epic("Stellar Burgers API")
@allure.feature("Авторизация пользователя")
class TestLoginUser:
    @allure.title("Успешный вход под существующим пользователем")
    def test_login_existing_user_success(self, registered_user):
        api_client = ApiClient(Urls.API_URL)
        
        response = api_client.login_user({
            "email": registered_user["email"],
            "password": registered_user["password"]
        })
        
        api_client.check_response_status(response, 200)
        api_client.check_response_success(response, True)
        
        response_data = response.json()
        assert "accessToken" in response_data
        assert "refreshToken" in response_data
        assert response_data["user"]["email"] == registered_user["email"]

    @allure.title("Вход с неверным email")
    def test_login_with_invalid_email(self, registered_user):
        api_client = ApiClient(Urls.API_URL)
        
        response = api_client.login_user({
            "email": "nonexistent@example.com",
            "password": registered_user["password"]
        })
        
        api_client.check_response_status(response, ErrorCodes.UNAUTHORIZED)
        api_client.check_response_success(response, False)
        assert response.json().get("message") == ResponseMessages.INVALID_CREDENTIALS

    @allure.title("Вход с неверным паролем")
    def test_login_with_invalid_password(self, registered_user):
        api_client = ApiClient(Urls.API_URL)
        
        response = api_client.login_user({
            "email": registered_user["email"],
            "password": UserData.INVALID_PASSWORD
        })
        
        api_client.check_response_status(response, ErrorCodes.UNAUTHORIZED)
        api_client.check_response_success(response, False)
        assert response.json().get("message") == ResponseMessages.INVALID_CREDENTIALS

    @allure.title("Вход без email")
    def test_login_without_email(self, registered_user):
        api_client = ApiClient(Urls.API_URL)
        
        response = api_client.login_user({
            "password": registered_user["password"]
        })
        
        api_client.check_response_status(response, ErrorCodes.UNAUTHORIZED)
        api_client.check_response_success(response, False)
        assert response.json().get("message") == ResponseMessages.INVALID_CREDENTIALS

    @allure.title("Вход без пароля")
    def test_login_without_password(self, registered_user):
        api_client = ApiClient(Urls.API_URL)
        
        response = api_client.login_user({
            "email": registered_user["email"]
        })
        
        api_client.check_response_status(response, ErrorCodes.UNAUTHORIZED)
        api_client.check_response_success(response, False)
        assert response.json().get("message") == ResponseMessages.INVALID_CREDENTIALS