from .base_page import BasePage
from utils.locators import MainPageLocators

class MainPage(BasePage):
    def click_login_button(self):
        self.click_element(MainPageLocators.LOGIN_BUTTON)

    def click_personal_account_button(self):
        self.click_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)

    def click_constructor_button(self):
        self.click_element(MainPageLocators.CONSTRUCTOR_BUTTON)

    def click_logo(self):
        self.click_element(MainPageLocators.LOGO)