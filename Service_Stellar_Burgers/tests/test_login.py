import pytest
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.registration_page import RegistrationPage
from utils.data import generate_email, generate_password, generate_name
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.locators import LoginPageLocators

@pytest.mark.usefixtures('driver')
class TestLogin:
    def test_login_via_main_page_button(self, driver):
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
        
        assert login_page.is_login_successful()

    def test_login_via_personal_account_button(self, driver):
        # Сначала регистрируем нового пользователя
        driver.get("https://stellarburgers.nomoreparties.site/register")
        reg_page = RegistrationPage(driver)
        email = generate_email()
        password = generate_password()
        reg_page.register_user(generate_name(), email, password)
        
        # Ждем редиректа на логин
        WebDriverWait(driver, 10).until(EC.url_contains("login"))
        
        # Теперь логинимся через личный кабинет
        driver.get("https://stellarburgers.nomoreparties.site")
        main_page = MainPage(driver)
        main_page.click_personal_account_button()
        
        login_page = LoginPage(driver)
        login_page.login(email, password)
        
        assert login_page.is_login_successful()

    def test_login_via_registration_page(self, driver):
        # Сначала регистрируем нового пользователя
        driver.get("https://stellarburgers.nomoreparties.site/register")
        reg_page = RegistrationPage(driver)
        email = generate_email()
        password = generate_password()
        reg_page.register_user(generate_name(), email, password)
        
        # Ждем редиректа на логин
        WebDriverWait(driver, 10).until(EC.url_contains("login"))
        
        # Теперь логинимся через страницу регистрации
        driver.get("https://stellarburgers.nomoreparties.site/register")
        login_page = LoginPage(driver)
        login_page.click_element(LoginPageLocators.LOGIN_LINK)
        
        login_page.login(email, password)
        
        assert login_page.is_login_successful()

    def test_login_via_password_recovery_page(self, driver):
        # Сначала регистрируем нового пользователя
        driver.get("https://stellarburgers.nomoreparties.site/register")
        reg_page = RegistrationPage(driver)
        email = generate_email()
        password = generate_password()
        reg_page.register_user(generate_name(), email, password)
        
        # Ждем редиректа на логин
        WebDriverWait(driver, 10).until(EC.url_contains("login"))
        
        # Теперь логинимся через страницу восстановления пароля
        driver.get("https://stellarburgers.nomoreparties.site/forgot-password")
        login_page = LoginPage(driver)
        login_page.click_element(LoginPageLocators.LOGIN_LINK)
        
        login_page.login(email, password)
        
        assert login_page.is_login_successful()