import requests
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def check_api_availability():
    """Проверка доступности API endpoints"""
    base_url = "https://stellarburgers.education-services.ru/api"
    
    endpoints = {
        "GET /ingredients": f"{base_url}/ingredients",
        "POST /auth/register": f"{base_url}/auth/register",
        "POST /auth/login": f"{base_url}/auth/login", 
        "POST /orders": f"{base_url}/orders",
    }
    
    test_user = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }
    
    logger.info("Проверка доступности API Stellar Burgers")
    logger.info("=" * 50)
    
    results = {}
    
    for endpoint_name, url in endpoints.items():
        logger.info(f"Тестируем {endpoint_name}")
        logger.info(f"URL: {url}")
        
        try:
            if endpoint_name == "GET /ingredients":
                response = requests.get(url, timeout=10)
            elif endpoint_name == "POST /auth/register":
                response = requests.post(url, json=test_user, timeout=10)
            elif endpoint_name == "POST /auth/login":
                response = requests.post(url, json=test_user, timeout=10)
            elif endpoint_name == "POST /orders":
                response = requests.post(url, json={"ingredients": []}, timeout=10)
            
            logger.info(f"Статус: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    logger.info(f"Success: {data.get('success', 'N/A')}")
                    if endpoint_name == "GET /ingredients" and "data" in data:
                        logger.info(f"Ингредиентов: {len(data['data'])}")
                except json.JSONDecodeError:
                    logger.error(f"Ответ не в JSON формате: {response.text[:100]}...")
            else:
                logger.info(f"Ответ: {response.text[:200]}...")
                
            results[endpoint_name] = {
                "status": response.status_code,
                "success": True
            }
                
        except requests.exceptions.ConnectionError:
            logger.error("Ошибка соединения")
            results[endpoint_name] = {"status": "ConnectionError", "success": False}
        except requests.exceptions.Timeout:
            logger.error("Таймаут запроса")
            results[endpoint_name] = {"status": "Timeout", "success": False}
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            results[endpoint_name] = {"status": str(e), "success": False}
    
    return results


if __name__ == "__main__":
    check_api_availability()