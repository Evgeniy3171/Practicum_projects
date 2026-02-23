import pytest
from pages.main_page import MainPage
from pages.personal_account_page import PersonalAccountPage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from utils.data import generate_email, generate_password, generate_name
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.locators import MainPageLocators

@pytest.mark.usefixtures('driver')
class TestPersonalAccount:
    def test_go_to_personal_account(self, driver):
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
        
        # Ждем, пока загрузится главная страница после входа
        WebDriverWait(driver, 10).until(
            EC.url_contains("stellarburgers")
        )
        
        # Ждем, пока станет доступна кнопка личного кабинета
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        )
        
        # Затем переходим в личный кабинет
        main_page.click_personal_account_button()
        
        # Ждем загрузки личного кабинета
        WebDriverWait(driver, 10).until(
            EC.url_contains("account")
        )
        
        personal_account_page = PersonalAccountPage(driver)
        personal_account_page.wait_for_account_page_load()
        
        # Проверяем видимость профиля
        assert personal_account_page.is_profile_visible()

    def test_go_from_personal_account_to_constructor(self, driver):
        # Регистрируем и логинимся
        driver.get("https://stellarburgers.nomoreparties.site/register")
        reg_page = RegistrationPage(driver)
        email = generate_email()
        password = generate_password()
        reg_page.register_user(generate_name(), email, password)
        WebDriverWait(driver, 10).until(EC.url_contains("login"))
        
        driver.get("https://stellarburgers.nomoreparties.site")
        main_page = MainPage(driver)
        main_page.click_login_button()
        login_page = LoginPage(driver)
        login_page.login(email, password)
        
        # Ждем загрузки главной страницы
        WebDriverWait(driver, 10).until(
            EC.url_contains("stellarburgers")
        )
        
        # Ждем, пока станет доступна кнопка личного кабинета
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        )
        
        main_page.click_personal_account_button()
        
        # Ждем загрузки личного кабинета
        WebDriverWait(driver, 10).until(
            EC.url_contains("account")
        )
        
        personal_account_page = PersonalAccountPage(driver)
        personal_account_page.wait_for_account_page_load()
        
        # Возвращаемся в конструктор через кнопку "Конструктор"
        # Ждем, пока станет доступна кнопка конструктора
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.CONSTRUCTOR_BUTTON)
        )
        main_page.click_constructor_button()
        
        # Ждем возврата на главную страницу
        WebDriverWait(driver, 10).until(
            EC.url_contains("stellarburgers")
        )
        
        assert "account" not in driver.current_url

    def test_go_from_personal_account_via_logo(self, driver):
        # Регистрируем и логинимся
        driver.get("https://stellarburgers.nomoreparties.site/register")
        reg_page = RegistrationPage(driver)
        email = generate_email()
        password = generate_password()
        reg_page.register_user(generate_name(), email, password)
        WebDriverWait(driver, 10).until(EC.url_contains("login"))
        
        driver.get("https://stellarburgers.nomoreparties.site")
        main_page = MainPage(driver)
        main_page.click_login_button()
        login_page = LoginPage(driver)
        login_page.login(email, password)
        
        # Ждем загрузки главной страницы
        WebDriverWait(driver, 10).until(
            EC.url_contains("stellarburgers")
        )
        
        # Ждем, пока станет доступна кнопка личного кабинета
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        )
        
        main_page.click_personal_account_button()
        
        # Ждем загрузки личного кабинета
        WebDriverWait(driver, 10).until(
            EC.url_contains("account")
        )
        
        personal_account_page = PersonalAccountPage(driver)
        personal_account_page.wait_for_account_page_load()
        
        # Возвращаемся на главную через логотип
        # Ждем, пока станет доступен логотип
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.LOGO)
        )
        main_page.click_logo()
        
        # Ждем возврата на главную страницу
        WebDriverWait(driver, 10).until(
            EC.url_contains("stellarburgers")
        )
        
        assert "account" not in driver.current_url