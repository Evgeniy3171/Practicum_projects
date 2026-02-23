import pytest
import allure
from helpers.api_client import ApiClient
from data.urls import Urls
from data.test_data import UserData, ResponseMessages, ErrorCodes


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestCreateUser:
    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, generate_unique_user):
        api_client = ApiClient(Urls.API_URL)
        user_data = generate_unique_user()
        
        response = api_client.create_user(user_data)
        
        api_client.check_response_status(response, 200)
        api_client.check_response_success(response, True)
        
        response_data = response.json()
        assert "user" in response_data
        assert response_data["user"]["email"] == user_data["email"]
        assert response_data["user"]["name"] == user_data["name"]
        assert "accessToken" in response_data

    @allure.title("Создание пользователя с уже существующим email")
    def test_create_user_with_existing_email(self, registered_user):
        api_client = ApiClient(Urls.API_URL)
        
        response = api_client.create_user({
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"]
        })
        
        api_client.check_response_status(response, ErrorCodes.FORBIDDEN)
        api_client.check_response_success(response, False)
        assert response.json().get("message") == ResponseMessages.USER_EXISTS

    @allure.title("Создание пользователя без обязательного поля email")
    def test_create_user_without_email(self, generate_unique_user):
        api_client = ApiClient(Urls.API_URL)
        user_data = generate_unique_user()
        user_data.pop("email")
        
        response = api_client.create_user(user_data)
        
        api_client.check_response_status(response, ErrorCodes.FORBIDDEN)
        api_client.check_response_success(response, False)
        assert response.json().get("message") == ResponseMessages.REQUIRED_FIELDS

    @allure.title("Создание пользователя без обязательного поля password")
    def test_create_user_without_password(self, generate_unique_user):
        api_client = ApiClient(Urls.API_URL)
        user_data = generate_unique_user()
        user_data.pop("password")
        
        response = api_client.create_user(user_data)
        
        api_client.check_response_status(response, ErrorCodes.FORBIDDEN)
        api_client.check_response_success(response, False)
        assert response.json().get("message") == ResponseMessages.REQUIRED_FIELDS

    @allure.title("Создание пользователя без обязательного поля name")
    def test_create_user_without_name(self, generate_unique_user):
        api_client = ApiClient(Urls.API_URL)
        user_data = generate_unique_user()
        user_data.pop("name")
        
        response = api_client.create_user(user_data)
        
        api_client.check_response_status(response, ErrorCodes.FORBIDDEN)
        api_client.check_response_success(response, False)
        assert response.json().get("message") == ResponseMessages.REQUIRED_FIELDS