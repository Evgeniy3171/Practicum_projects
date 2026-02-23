import pytest
import allure
from helpers.api_client import ApiClient
from data.urls import Urls
from data.test_data import ResponseMessages, ErrorCodes


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_auth_and_valid_ingredients(self, registered_user, valid_ingredients):
        api_client = ApiClient(Urls.API_URL)
        
        response = api_client.create_order(valid_ingredients, registered_user["access_token"])
        
        api_client.check_response_status(response, 200)
        api_client.check_response_success(response, True)
        
        response_data = response.json()
        assert "order" in response_data
        assert "number" in response_data["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, valid_ingredients):
        api_client = ApiClient(Urls.API_URL)
        
        response = api_client.create_order(valid_ingredients)
        
        api_client.check_response_status(response, 200)
        api_client.check_response_success(response, True)

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, registered_user):
        api_client = ApiClient(Urls.API_URL)
        
        response = api_client.create_order([], registered_user["access_token"])
        
        api_client.check_response_status(response, ErrorCodes.BAD_REQUEST)
        api_client.check_response_success(response, False)
        assert response.json().get("message") == ResponseMessages.INGREDIENTS_REQUIRED

    @allure.title("Создание заказа с невалидными ингредиентами")
    def test_create_order_with_invalid_ingredients(self, registered_user, invalid_ingredients):
        api_client = ApiClient(Urls.API_URL)
        
        response = api_client.create_order(invalid_ingredients, registered_user["access_token"])
        
        # В зависимости от API может возвращать 400 или 500
        assert response.status_code in [ErrorCodes.BAD_REQUEST, 500]

    @allure.title("Создание заказа с одним ингредиентом")
    def test_create_order_with_single_ingredient(self, registered_user, get_ingredients):
        api_client = ApiClient(Urls.API_URL)
        
        single_ingredient = [get_ingredients[0]["_id"]]
        response = api_client.create_order(single_ingredient, registered_user["access_token"])
        
        api_client.check_response_status(response, 200)
        api_client.check_response_success(response, True)