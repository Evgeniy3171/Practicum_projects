# pages/base_page.py
import allure
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
from config.urls import Urls

logger = logging.getLogger(__name__)

class BasePage:
    @allure.step("Инициализация BasePage для драйвера")
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.urls = Urls()
        logger.debug(f"Initialized BasePage for {driver.name}")
    
    @allure.step("Найти элемент {locator}")
    def find_element(self, locator):
        logger.debug(f"Finding element: {locator}")
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise
    
    @allure.step("Найти элементы {locator}")
    def find_elements(self, locator):
        logger.debug(f"Finding elements: {locator}")
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            logger.error(f"Elements not found: {locator}")
            return []
    
    @allure.step("Кликнуть на элемент {locator}")
    def click(self, locator):
        logger.debug(f"Clicking on element: {locator}")
        try:
            element = self.find_element(locator)
            element.click()
        except (ElementClickInterceptedException, StaleElementReferenceException):
            logger.warning(f"Click failed, using JavaScript click for: {locator}")
            # Всегда используем JavaScript клик как запасной вариант
            self.click_js(locator)
    
    @allure.step("Кликнуть через JavaScript на элемент {locator}")
    def click_js(self, locator):
        logger.debug(f"Clicking with JavaScript on element: {locator}")
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)
    
    @allure.step("Ожидать исчезновения элемента {locator}")
    def wait_for_element_to_disappear(self, locator, timeout=10):
        logger.debug(f"Waiting for element to disappear: {locator}")
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
    
    @allure.step("Проверить видимость элемента {locator}")
    def is_element_visible(self, locator):
        try:
            is_visible = self.find_element(locator).is_displayed()
            logger.debug(f"Element visibility {locator}: {is_visible}")
            return is_visible
        except Exception:
            logger.debug(f"Element not visible: {locator}")
            return False
    
    @allure.step("Прокрутить к элементу {locator}")
    def scroll_to_element(self, locator):
        logger.debug(f"Scrolling to element: {locator}")
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    @allure.step("Ожидать загрузки страницы")
    def wait_for_page_loaded(self, timeout=15):
        logger.debug("Waiting for page to load")
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
    
    @allure.step("Перейти по URL: {url}")
    def go_to_url(self, url):
        logger.info(f"Navigating to URL: {url}")
        self.driver.get(url)
        self.wait_for_page_loaded()
    
    @allure.step("Получить текущий URL")
    def get_current_url(self):
        current_url = self.driver.current_url
        logger.debug(f"Current URL: {current_url}")
        return current_url
    
    @allure.step("Выполнить JavaScript код: {script}")
    def execute_script(self, script, *args):
        logger.debug(f"Executing JavaScript: {script}")
        return self.driver.execute_script(script, *args)
    
    @allure.step("Получить текст элемента {locator}")
    def get_element_text(self, locator):
        logger.debug(f"Getting text from element: {locator}")
        element = self.find_element(locator)
        return element.text
    
    @allure.step("Ввести текст '{text}' в элемент {locator}")
    def enter_text(self, locator, text):
        logger.debug(f"Entering text '{text}' into element: {locator}")
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    @allure.step("Ожидать появления элемента {locator}")
    def wait_for_element_present(self, locator, timeout=10):
        logger.debug(f"Waiting for element to be present: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
    
    @allure.step("Ожидать кликабельности элемента {locator}")
    def wait_for_element_clickable(self, locator, timeout=10):
        logger.debug(f"Waiting for element to be clickable: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    @allure.step("Получить атрибут '{attribute}' элемента {locator}")
    def get_element_attribute(self, locator, attribute):
        logger.debug(f"Getting attribute '{attribute}' from element: {locator}")
        element = self.find_element(locator)
        return element.get_attribute(attribute)
    
    @allure.step("Перейти на главную страницу")
    def go_to_main_page(self):
        logger.info("Navigating to main page")
        self.go_to_url(self.urls.MAIN_PAGE)
        self.wait_for_page_loaded()
    
    @allure.step("Перейти на страницу ленты заказов")
    def go_to_order_feed(self):
        logger.info("Navigating to order feed page")
        self.go_to_url(self.urls.ORDER_FEED)
        self.wait_for_page_loaded()
    
    @allure.step("Перейти на страницу авторизации")
    def go_to_login_page(self):
        logger.info("Navigating to login page")
        self.go_to_url(self.urls.LOGIN_PAGE)
        self.wait_for_page_loaded()
    
    @allure.step("Перейти на страницу профиля")
    def go_to_profile_page(self):
        logger.info("Navigating to profile page")
        self.go_to_url(self.urls.PROFILE_PAGE)
        self.wait_for_page_loaded()
    
    @allure.step("Перейти на страницу регистрации")
    def go_to_register_page(self):
        logger.info("Navigating to register page")
        self.go_to_url(self.urls.REGISTER_PAGE)
        self.wait_for_page_loaded()
    
    @allure.step("Перейти на страницу восстановления пароля")
    def go_to_forgot_password_page(self):
        logger.info("Navigating to forgot password page")
        self.go_to_url(self.urls.FORGOT_PASSWORD_PAGE)
        self.wait_for_page_loaded()
    
    @allure.step("Перейти на страницу сброса пароля")
    def go_to_reset_password_page(self):
        logger.info("Navigating to reset password page")
        self.go_to_url(self.urls.RESET_PASSWORD_PAGE)
        self.wait_for_page_loaded()
    
    @allure.step("Обновить страницу")
    def refresh_page(self):
        logger.debug("Refreshing page")
        self.driver.refresh()
        self.wait_for_page_loaded()
    
    @allure.step("Вернуться назад")
    def go_back(self):
        logger.debug("Going back in browser history")
        self.driver.back()
        self.wait_for_page_loaded()
    
    @allure.step("Перейти вперед")
    def go_forward(self):
        logger.debug("Going forward in browser history")
        self.driver.forward()
        self.wait_for_page_loaded()
    
    @allure.step("Получить заголовок страницы")
    def get_page_title(self):
        title = self.driver.title
        logger.debug(f"Page title: {title}")
        return title
    
    @allure.step("Получить исходный код страницы")
    def get_page_source(self):
        logger.debug("Getting page source")
        return self.driver.page_source
    
    @allure.step("Сделать скриншот")
    def take_screenshot(self, filename=None):
        logger.debug("Taking screenshot")
        if filename:
            self.driver.save_screenshot(filename)
        return self.driver.get_screenshot_as_png()
    
    @allure.step("Переключиться на окно по индексу {index}")
    def switch_to_window(self, index):
        logger.debug(f"Switching to window with index: {index}")
        windows = self.driver.window_handles
        if index < len(windows):
            self.driver.switch_to.window(windows[index])
    
    @allure.step("Закрыть текущее окно")
    def close_current_window(self):
        logger.debug("Closing current window")
        self.driver.close()
    
    @allure.step("Принять alert")
    def accept_alert(self):
        logger.debug("Accepting alert")
        alert = self.driver.switch_to.alert
        alert.accept()
    
    @allure.step("Отклонить alert")
    def dismiss_alert(self):
        logger.debug("Dismissing alert")
        alert = self.driver.switch_to.alert
        alert.dismiss()
    
    @allure.step("Получить текст alert")
    def get_alert_text(self):
        logger.debug("Getting alert text")
        alert = self.driver.switch_to.alert
        return alert.text
    
    @allure.step("Ожидать что URL содержит {expected_url}")
    def wait_for_url_contains(self, expected_url, timeout=10):
        logger.debug(f"Waiting for URL to contain: {expected_url}")
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(expected_url)
        )
    
    @allure.step("Ожидать что URL равен {expected_url}")
    def wait_for_url_to_be(self, expected_url, timeout=10):
        logger.debug(f"Waiting for URL to be: {expected_url}")
        return WebDriverWait(self.driver, timeout).until(
            EC.url_to_be(expected_url)
        )
    
    @allure.step("Проверить что URL содержит {expected_url}")
    def is_url_contains(self, expected_url):
        current_url = self.get_current_url()
        contains = expected_url in current_url
        logger.debug(f"URL contains '{expected_url}': {contains}")
        return contains
    
    @allure.step("Проверить что URL равен {expected_url}")
    def is_url_equal_to(self, expected_url):
        current_url = self.get_current_url()
        equals = current_url == expected_url
        logger.debug(f"URL equals '{expected_url}': {equals}")
        return equals
    
    @allure.step("Безопасный клик с повторными попытками")
    def safe_click(self, locator, max_attempts=3):
        """Выполняет клик с повторными попытками при ошибках"""
        logger.debug(f"Safe clicking on element: {locator}")
        
        for attempt in range(max_attempts):
            try:
                self.click(locator)
                return True
            except (ElementClickInterceptedException, StaleElementReferenceException) as e:
                logger.warning(f"Click attempt {attempt + 1} failed: {e}")
                if attempt == max_attempts - 1:
                    logger.error(f"All {max_attempts} click attempts failed for: {locator}")
                    raise
        
        return False
    
    @allure.step("Выполнить drag&drop элемента {source_locator} в {target_locator}")
    def drag_and_drop(self, source_locator, target_locator):
        """Выполняет drag&drop элемента"""
        logger.debug(f"Dragging {source_locator} to {target_locator}")
        try:
            source_element = self.find_element(source_locator)
            target_element = self.find_element(target_locator)
            
            # JavaScript для drag&drop
            script = """
            function createEvent(type) {
                var event = new Event(type, { bubbles: true });
                event.dataTransfer = {
                    setData: function() {},
                    getData: function() { return ''; },
                    setDragImage: function() {}
                };
                return event;
            }
            
            var source = arguments[0];
            var target = arguments[1];
            
            source.dispatchEvent(createEvent('dragstart'));
            target.dispatchEvent(createEvent('dragover'));
            target.dispatchEvent(createEvent('drop'));
            source.dispatchEvent(createEvent('dragend'));
            """
            
            self.execute_script(script, source_element, target_element)
            logger.info("Drag&drop completed successfully")
            return True
            
        except Exception as e:
            logger.warning(f"Drag&drop failed: {e}")
            return False