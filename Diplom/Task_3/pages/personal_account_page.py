# pages/personal_account_page.py
import allure
import logging
from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class PersonalAccountPage(BasePage):
    # Элементы личного кабинета
    PROFILE_LINK = (By.XPATH, "//a[contains(text(), 'Профиль')]")
    ORDER_HISTORY_LINK = (By.XPATH, "//a[contains(text(), 'История заказов')]")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выход')]")
    
    # Поля профиля
    NAME_INPUT = (By.XPATH, "//input[@name='name']")
    EMAIL_INPUT = (By.XPATH, "//input[@name='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='password']")
    
    # Кнопки
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(), 'Сохранить')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(), 'Отмена')]")
    
    @allure.step("Перейти на страницу личного кабинета")
    def go_to_personal_account(self):
        self.go_to_profile_page()  # Используем метод из BasePage
        self.wait_for_page_load()
    
    @allure.step("Ожидать загрузки страницы личного кабинета")
    def wait_for_page_load(self):
        logger.debug("Waiting for personal account page to load")
        self.wait.until(EC.presence_of_element_located(self.PROFILE_LINK))
    
    @allure.step("Нажать на профиль")
    def click_profile(self):
        logger.debug("Clicking on profile")
        self.click(self.PROFILE_LINK)
    
    @allure.step("Нажать на историю заказов")
    def click_order_history(self):
        logger.debug("Clicking on order history")
        self.click(self.ORDER_HISTORY_LINK)
    
    @allure.step("Выйти из аккаунта")
    def logout(self):
        logger.info("Logging out from personal account")
        self.click(self.LOGOUT_BUTTON)
    
    @allure.step("Ввести имя: {name}")
    def enter_name(self, name):
        logger.debug(f"Entering name: {name}")
        self.enter_text(self.NAME_INPUT, name)
    
    @allure.step("Ввести email: {email}")
    def enter_email(self, email):
        logger.debug(f"Entering email: {email}")
        self.enter_text(self.EMAIL_INPUT, email)
    
    @allure.step("Ввести пароль")
    def enter_password(self, password):
        logger.debug("Entering password")
        self.enter_text(self.PASSWORD_INPUT, password)
    
    @allure.step("Нажать кнопку сохранить")
    def click_save_button(self):
        logger.debug("Clicking save button")
        self.click(self.SAVE_BUTTON)
    
    @allure.step("Нажать кнопку отмена")
    def click_cancel_button(self):
        logger.debug("Clicking cancel button")
        self.click(self.CANCEL_BUTTON)
    
    @allure.step("Проверить что находимся в личном кабинете")
    def is_personal_account_page(self):
        current_url = self.get_current_url()
        is_account_page = self.urls.PROFILE_PAGE in current_url
        logger.debug(f"Is personal account page: {is_account_page}")
        return is_account_page
    
    @allure.step("Проверить отображение ссылки профиля")
    def is_profile_link_displayed(self):
        return self.is_element_visible(self.PROFILE_LINK)
    
    @allure.step("Проверить отображение ссылки истории заказов")
    def is_order_history_link_displayed(self):
        return self.is_element_visible(self.ORDER_HISTORY_LINK)
    
    @allure.step("Проверить отображение кнопки выхода")
    def is_logout_button_displayed(self):
        return self.is_element_visible(self.LOGOUT_BUTTON)