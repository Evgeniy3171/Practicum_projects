from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import allure
from data.urls import MAIN_PAGE_URL


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = MAIN_PAGE_URL

    @allure.step("Найти элемент {locator}")
    def find_element(self, locator, time=10):
        try:
            return WebDriverWait(self.driver, time).until(
                EC.visibility_of_element_located(locator),
                message=f"Can't find element by locator {locator}"
            )
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    @allure.step("Кликнуть на элемент {locator}")
    def click_element(self, locator, time=10):
        try:
            element = self.find_element(locator, time)
            element.click()
        except (ElementClickInterceptedException, TimeoutException):
            element = self.find_element(locator, time)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Открыть сайт")
    def go_to_site(self):
        self.driver.get(self.base_url)
        self.close_cookie_banner()

    @allure.step("Закрыть баннер cookie")
    def close_cookie_banner(self):
        try:
            cookie_banner = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.ID, "rcc-confirm-button"))
            )
            cookie_banner.click()
            # Ждем исчезновения баннера
            WebDriverWait(self.driver, 3).until(
                EC.invisibility_of_element_located((By.ID, "rcc-confirm-button"))
            )
        except Exception:
            pass

    @allure.step("Прокрутить к элементу {locator}")
    def scroll_to_element(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    @allure.step("Прокрутить к нижней части страницы")
    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    @allure.step("Ожидание видимости элемента {locator}")
    def wait_for_visibility(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Ожидание кликабельности элемента {locator}")
    def wait_for_clickable(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(locator)
        )