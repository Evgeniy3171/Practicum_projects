import pytest
from pages.main_page import MainPage
from pages.personal_account_page import PersonalAccountPage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from utils.data import generate_email, generate_password, generate_name
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures('driver')
class TestLogout:
    def test_logout_from_personal_account(self, driver):
        # Сначала регистрируем нового пользователя
        driver.get("https://stellarburgers.nomoreparties.site/register")
        reg_page = RegistrationPage(driver)
        email = generate_email()
        password = generate_password()
        reg_page.register_user(generate_name(), email, password)
        
        # Ждем редиректа на логин
        WebDriverWait(driver, 10).until(EC.url_contains("login"))
        
        # Теперь логинимся
        driver.get("https://stellarburgers.nomoreparties.site")
        main_page = MainPage(driver)
        main_page.click_login_button()
        
        login_page = LoginPage(driver)
        login_page.login(email, password)
        
        # Переходим в личный кабинет
        main_page.click_personal_account_button()
        
        # Выходим из аккаунта
        personal_account_page = PersonalAccountPage(driver)
        personal_account_page.click_logout_button()
        personal_account_page.wait_for_logout()
        
        assert "login" in driver.current_url