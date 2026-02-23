# pages/login_page.py
import allure
import logging
from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    # Поля ввода
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль']")
    
    # Кнопки
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")
    REGISTER_LINK = (By.XPATH, "//a[contains(text(), 'Зарегистрироваться')]")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(text(), 'Восстановить пароль')]")
    
    @allure.step("Перейти на страницу авторизации")
    def go_to_login_page(self):
        logger.info("Navigating to login page")
        # Используем метод из BasePage, а не рекурсивный вызов
        self.go_to_url(self.urls.LOGIN_PAGE)
        self.wait_for_page_load()
    
    @allure.step("Ожидать загрузки страницы авторизации")
    def wait_for_page_load(self):
        logger.debug("Waiting for login page to load")
        self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT))
    
    @allure.step("Ввести email: {email}")
    def enter_email(self, email):
        logger.debug(f"Entering email: {email}")
        self.enter_text(self.EMAIL_INPUT, email)
    
    @allure.step("Ввести пароль")
    def enter_password(self, password):
        logger.debug("Entering password")
        self.enter_text(self.PASSWORD_INPUT, password)
    
    @allure.step("Нажать кнопку входа")
    def click_login_button(self):
        logger.debug("Clicking login button")
        self.click(self.LOGIN_BUTTON)
    
    @allure.step("Нажать ссылку регистрации")
    def click_register_link(self):
        logger.debug("Clicking register link")
        self.click(self.REGISTER_LINK)
    
    @allure.step("Нажать ссылку восстановления пароля")
    def click_forgot_password_link(self):
        logger.debug("Clicking forgot password link")
        self.click(self.FORGOT_PASSWORD_LINK)
    
    @allure.step("Выполнить авторизацию с email: {email}")
    def login(self, email, password):
        logger.info(f"Logging in with email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
    
    @allure.step("Проверить что находимся на странице логина")
    def is_login_page(self):
        current_url = self.get_current_url()
        is_login = self.urls.LOGIN_PAGE in current_url
        logger.debug(f"Is login page: {is_login}")
        return is_login
    
    @allure.step("Проверить отображение поля email")
    def is_email_field_displayed(self):
        return self.is_element_visible(self.EMAIL_INPUT)
    
    @allure.step("Проверить отображение поля пароля")
    def is_password_field_displayed(self):
        return self.is_element_visible(self.PASSWORD_INPUT)
    
    @allure.step("Проверить отображение кнопки входа")
    def is_login_button_displayed(self):
        return self.is_element_visible(self.LOGIN_BUTTON)
    
    @allure.step("Проверить отображение ссылки регистрации")
    def is_register_link_displayed(self):
        return self.is_element_visible(self.REGISTER_LINK)
    
    @allure.step("Проверить отображение ссылки восстановления пароля")
    def is_forgot_password_link_displayed(self):
        return self.is_element_visible(self.FORGOT_PASSWORD_LINK)