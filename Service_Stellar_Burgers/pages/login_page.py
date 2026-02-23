from .base_page import BasePage
from utils.locators import LoginPageLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class LoginPage(BasePage):
    def login(self, email, password):
        self.input_text(LoginPageLocators.EMAIL_INPUT, email)
        self.input_text(LoginPageLocators.PASSWORD_INPUT, password)
        self.click_element(LoginPageLocators.LOGIN_BUTTON)

    def click_register_link(self):
        self.click_element(LoginPageLocators.REGISTER_LINK)

    def click_forgot_password_link(self):
        self.click_element(LoginPageLocators.FORGOT_PASSWORD_LINK)

    def is_login_successful(self):
        # Проверяем, что появилась кнопка "Оформить заказ" на главной странице
        from utils.locators import MainPageLocators
        return self.is_element_visible(MainPageLocators.ORDER_BUTTON)