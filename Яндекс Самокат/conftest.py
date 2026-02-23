import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import allure
from allure_commons.types import AttachmentType
import os

@pytest.fixture(scope="function")
def driver():
    # Для Firefox
    from webdriver_manager.firefox import GeckoDriverManager
    service = Service(executable_path=GeckoDriverManager().install())
    
    options = webdriver.FirefoxOptions()
    options.headless = False
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()
    
    yield driver
    
    # Делаем скриншот при падении теста
    if hasattr(driver, 'session_id') and driver.session_id is not None:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="screenshot",
            attachment_type=AttachmentType.PNG
        )
    driver.quit()