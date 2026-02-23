from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://stellarburgers.nomoreparties.site/"

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Can't find element by locator {locator}"
        )

    def click_element(self, locator, time=10):
        element = WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(locator),
            message=f"Element not clickable by locator {locator}"
        )
        
        # Попробуем кликнуть через JavaScript если обычный клик не работает
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def input_text(self, locator, text, time=10):
        element = WebDriverWait(self.driver, time).until(
            EC.visibility_of_element_located(locator),
            message=f"Element not visible by locator {locator}"
        )
        element.clear()
        element.send_keys(text)

    def is_element_visible(self, locator, time=5):
        try:
            WebDriverWait(self.driver, time).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, text, time=10):
        WebDriverWait(self.driver, time).until(
            EC.url_contains(text)
        )

    def scroll_to_element(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)