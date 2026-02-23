# utils/locator_helper.py
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)

def debug_locators(driver):
    logger.info("Debugging locators on the page")
    
    driver.get("https://stellarburgers.nomorepartiessite.ru/")
    
    test_selectors = [
        "//a[contains(@href, 'constructor')]",
        "//a[contains(text(), 'Конструктор')]",
        "//a[contains(@href, 'feed')]",
        "//a[contains(text(), 'Лента заказов')]",
        "//div[contains(@class, 'BurgerIngredients_ingredients__')]",
        "//section[contains(@class, 'BurgerConstructor')]",
        "//div[contains(@class, 'Modal_modal')]",
        "//button[contains(@class, 'button_button')]"
    ]
    
    for selector in test_selectors:
        try:
            elements = driver.find_elements(By.XPATH, selector)
            logger.info(f"Selector: {selector} - Found {len(elements)} elements")
            if elements:
                for i, elem in enumerate(elements[:3]):
                    logger.debug(f"  Element {i}: {elem.text[:50] if elem.text else 'No text'}")
        except Exception as e:
            logger.error(f"Selector: {selector} - Error: {e}")