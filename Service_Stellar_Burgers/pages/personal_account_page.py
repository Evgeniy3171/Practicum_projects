from .base_page import BasePage
from utils.locators import PersonalAccountLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PersonalAccountPage(BasePage):
    def click_logout_button(self):
        # Ждем пока кнопка выхода станет доступной
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(PersonalAccountLocators.LOGOUT_BUTTON)
        )
        self.click_element(PersonalAccountLocators.LOGOUT_BUTTON)

    def is_profile_visible(self, time=15):
        try:
            WebDriverWait(self.driver, time).until(
                EC.visibility_of_element_located(PersonalAccountLocators.PROFILE_LINK)
            )
            return True
        except:
            # Сохраняем скриншот для отладки
            self.driver.save_screenshot("profile_not_visible.png")
            return False

    def wait_for_logout(self):
        self.wait_for_url_contains("login")
    
    def wait_for_account_page_load(self):
        # Ждем загрузки страницы личного кабинета
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(PersonalAccountLocators.PROFILE_LINK)
        )