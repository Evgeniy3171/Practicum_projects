# debug_page_structure.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_page_structure():
    """Диагностика структуры страницы для понимания локаторов"""
    options = Options()
    options.add_argument("--window-size=1920,1080")
    
    service = Service("drivers/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get("https://stellarburgers.education-services.ru/")
        time.sleep(3)
        
        print("🔍 ДИАГНОСТИКА СТРАНИЦЫ:")
        print("=" * 50)
        
        # Ищем ингредиенты
        print("\n🧪 ИНГРЕДИЕНТЫ:")
        ingredient_selectors = [
            "//div[contains(@class, 'ingredient')]",
            "//a[contains(@class, 'ingredient')]",
            "//section[contains(@class, 'BurgerIngredients')]//div",
            "//div[contains(text(), 'булка') or contains(text(), 'соус') or contains(text(), 'начинка')]",
            "//*[contains(@class, 'BurgerIngredient_ingredient')]"
        ]
        
        for selector in ingredient_selectors:
            elements = driver.find_elements(By.XPATH, selector)
            print(f"Селектор: {selector} - найдено: {len(elements)}")
            for i, elem in enumerate(elements[:3]):
                print(f"  {i+1}. Текст: {elem.text[:50] if elem.text else 'No text'}")
                print(f"     Классы: {elem.get_attribute('class')}")
        
        # Ищем модальные окна
        print("\n🪟 МОДАЛЬНЫЕ ОКНА:")
        modal_selectors = [
            "//div[contains(@class, 'modal')]",
            "//div[contains(@class, 'Modal')]",
            "//section[contains(@class, 'modal')]",
            "//div[contains(@class, 'popup')]"
        ]
        
        for selector in modal_selectors:
            elements = driver.find_elements(By.XPATH, selector)
            print(f"Селектор: {selector} - найдено: {len(elements)}")
        
        # Кликаем на первый ингредиент и проверяем модальное окно
        print("\n🧪 ТЕСТ КЛИКА НА ИНГРЕДИЕНТ:")
        first_ingredient = None
        for selector in ingredient_selectors:
            elements = driver.find_elements(By.XPATH, selector)
            if elements:
                first_ingredient = elements[0]
                print(f"Кликаем на ингредиент: {selector}")
                first_ingredient.click()
                time.sleep(2)
                break
        
        if first_ingredient:
            # Проверяем модальные окна после клика
            for selector in modal_selectors:
                elements = driver.find_elements(By.XPATH, selector)
                print(f"После клика - {selector}: {len(elements)}")
                for elem in elements:
                    print(f"  Видимый: {elem.is_displayed()}, Текст: {elem.text[:100] if elem.text else 'No text'}")
        
        # Сохраняем скриншот
        driver.save_screenshot("debug_page.png")
        print("\n📸 Скриншот сохранен: debug_page.png")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_page_structure()