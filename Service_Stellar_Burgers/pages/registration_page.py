from .base_page import BasePage
from utils.locators import RegistrationPageLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class RegistrationPage(BasePage):
    def register_user(self, name, email, password):
        self.input_text(RegistrationPageLocators.NAME_INPUT, name)
        self.input_text(RegistrationPageLocators.EMAIL_INPUT, email)
        self.input_text(RegistrationPageLocators.PASSWORD_INPUT, password)
        self.click_element(RegistrationPageLocators.REGISTER_BUTTON)

    def get_error_message(self):
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(RegistrationPageLocators.ERROR_MESSAGE))
            return element.text
        except:
            return None

    def get_password_error(self):
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(RegistrationPageLocators.PASSWORD_ERROR))
            return element.text
        except:
            return None