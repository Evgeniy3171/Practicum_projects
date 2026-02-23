# test_basic.py
import pytest
import logging
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

def test_basic_functionality(driver):
    """Базовый тест для проверки работы драйвера"""
    logger.info("Starting basic functionality test")
    
    try:
        # Открываем правильный сайт
        driver.get("https://stellarburgers.education-services.ru/")
        
        logger.info(f"Page title: {driver.title}")
        logger.info(f"Current URL: {driver.current_url}")
        
        # Проверяем что страница загрузилась
        assert "stellarburgers" in driver.current_url
        assert driver.title is not None
        
        # Проверяем наличие ключевых элементов
        page_source = driver.page_source
        required_elements = ["Конструктор", "Лента заказов", "Булки"]
        found_elements = [elem for elem in required_elements if elem in page_source]
        
        logger.info(f"Found {len(found_elements)}/{len(required_elements)} required elements")
        
        # Делаем скриншот
        driver.save_screenshot("test_basic_screenshot.png")
        logger.info("Screenshot saved: test_basic_screenshot.png")
        
        assert len(found_elements) >= 2, f"Not enough elements found: {found_elements}"
        
        logger.info("Basic functionality test passed successfully")
        
    except Exception as e:
        logger.error(f"Basic functionality test failed: {e}")
        raise

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])