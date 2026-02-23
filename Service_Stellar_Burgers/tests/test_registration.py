import pytest
import time
from pages.registration_page import RegistrationPage
from utils.data import generate_email, generate_password, generate_name
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures('driver')
class TestRegistration:
    def test_successful_registration(self, driver):
        driver.get("https://stellarburgers.nomoreparties.site/register")
        reg_page = RegistrationPage(driver)
        email = generate_email()
        password = generate_password()
        reg_page.register_user(generate_name(), email, password)
        
        # Ждем редиректа на login page после успешной регистрации
        WebDriverWait(driver, 10).until(EC.url_contains("login"))
        assert "login" in driver.current_url

    def test_registration_with_short_password(self, driver):
        driver.get("https://stellarburgers.nomoreparties.site/register")
        reg_page = RegistrationPage(driver)
        reg_page.register_user(generate_name(), generate_email(), "123")
        
        # Ждем появления ошибки
        error_text = WebDriverWait(driver, 10).until(
            lambda d: reg_page.get_password_error() or reg_page.get_error_message()
        )
        assert error_text == "Некорректный пароль"