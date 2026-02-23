from .base_page import BasePage
from utils.locators import MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ConstructorPage(BasePage):
    def click_buns_section(self):
        # Прокручиваем к элементу перед кликом
        self.scroll_to_element(MainPageLocators.BUNS_SECTION)
        self.click_element(MainPageLocators.BUNS_SECTION)

    def click_sauces_section(self):
        self.scroll_to_element(MainPageLocators.SAUCES_SECTION)
        self.click_element(MainPageLocators.SAUCES_SECTION)

    def click_toppings_section(self):
        self.scroll_to_element(MainPageLocators.TOPPINGS_SECTION)
        self.click_element(MainPageLocators.TOPPINGS_SECTION)

    def is_section_active(self, section_locator):
        element = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(section_locator)
        )
        return "tab_tab_type_current" in element.get_attribute("class")