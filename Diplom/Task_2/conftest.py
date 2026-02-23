import pytest
import requests
import random
import string
from data.urls import Urls
from data.test_data import UserData


@pytest.fixture
def generate_unique_user():
    """Генерация уникального пользователя со сложной логикой"""
    def _generate():
        email = UserData.generate_email()
        return {
            "email": email,
            "password": UserData.VALID_PASSWORD,
            "name": f"{UserData.VALID_NAME}{random.randint(1000, 9999)}"
        }
    return _generate


@pytest.fixture
def registered_user(generate_unique_user):
    """Создание зарегистрированного пользователя с обработкой ошибок"""
    user_data = generate_unique_user()
    
    # Регистрируем пользователя
    response = requests.post(Urls.REGISTER, json=user_data, timeout=10)
    
    if response.status_code != 200:
        pytest.fail(f"Failed to register test user: {response.status_code} - {response.text}")
    
    response_data = response.json()
    
    # Добавляем токен к данным пользователя
    user_data.update({
        "access_token": response_data.get("accessToken"),
        "refresh_token": response_data.get("refreshToken")
    })
    
    yield user_data
    

@pytest.fixture
def get_ingredients():
    """Получение списка ингредиентов с обработкой ошибок"""
    try:
        response = requests.get(Urls.INGREDIENTS, timeout=10)
        
        if response.status_code != 200:
            pytest.skip(f"Cannot fetch ingredients: {response.status_code}")
            
        data = response.json()
        
        if not data.get('success'):
            pytest.skip("Ingredients endpoint returned unsuccessful response")
            
        ingredients = data.get('data', [])
        
        if not ingredients:
            pytest.skip("No ingredients available for testing")
            
        return ingredients
        
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Cannot connect to ingredients endpoint: {e}")


@pytest.fixture
def valid_ingredients(get_ingredients):
    """Валидные ингредиенты для заказа"""
    return [ingredient["_id"] for ingredient in get_ingredients[:2]]


@pytest.fixture
def invalid_ingredients():
    """Невалидные ингредиенты"""
    return ["invalid_hash_1", "invalid_hash_2"]