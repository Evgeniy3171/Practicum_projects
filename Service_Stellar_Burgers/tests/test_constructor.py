import pytest
from pages.constructor_page import ConstructorPage
from pages.main_page import MainPage
from utils.locators import MainPageLocators

@pytest.mark.usefixtures('driver')
class TestConstructor:
    def test_go_to_buns_section(self, driver):
        driver.get("https://stellarburgers.nomoreparties.site")
        constructor_page = ConstructorPage(driver)
        constructor_page.click_buns_section()
        
        assert constructor_page.is_section_active(MainPageLocators.BUNS_SECTION)

    def test_go_to_sauces_section(self, driver):
        driver.get("https://stellarburgers.nomoreparties.site")
        constructor_page = ConstructorPage(driver)
        constructor_page.click_sauces_section()
        
        assert constructor_page.is_section_active(MainPageLocators.SAUCES_SECTION)

    def test_go_to_toppings_section(self, driver):
        driver.get("https://stellarburgers.nomoreparties.site")
        constructor_page = ConstructorPage(driver)
        constructor_page.click_toppings_section()
        
        assert constructor_page.is_section_active(MainPageLocators.TOPPINGS_SECTION)

    