from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
import allure


class OrderPage(BasePage):
    # Локаторы для первой страницы заказа
    NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_STATION_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    METRO_STATION_OPTIONS = (By.CLASS_NAME, "select-search__option")
    PHONE_INPUT = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")
    
    # Локаторы для второй страницы заказа
    DATE_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    RENTAL_PERIOD_DROPDOWN = (By.XPATH, "//div[text()='* Срок аренды']")
    RENTAL_PERIOD_OPTIONS = (By.XPATH, "//div[@class='Dropdown-option']")
    COLOR_CHECKBOX = (By.ID, "{}")
    COMMENT_INPUT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Заказать' and contains(@class, 'Button_Middle')]")
    CONFIRM_BUTTON = (By.XPATH, "//button[text()='Да']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(text(), 'Заказ оформлен')]")

    @allure.step("Заполнить первую страницу формы заказа")
    def fill_order_form_first_step(self, name, last_name, address, metro_station, phone):
        self.find_element(self.NAME_INPUT).send_keys(name)
        self.find_element(self.LAST_NAME_INPUT).send_keys(last_name)
        self.find_element(self.ADDRESS_INPUT).send_keys(address)
        self.select_metro_station(metro_station)
        self.find_element(self.PHONE_INPUT).send_keys(phone)
        self.click_element(self.NEXT_BUTTON)

    @allure.step("Выбрать станцию метро: {station_name}")
    def select_metro_station(self, station_name):
        self.click_element(self.METRO_STATION_INPUT)
        self.find_element(self.METRO_STATION_INPUT).send_keys(station_name)
        
        # Ждем появления вариантов
        self.wait_for_visibility((By.CLASS_NAME, "select-search__select"))
        
        # Пробуем найти станцию по точному совпадению
        try:
            station_xpath = f"//div[text()='{station_name}']"
            station_option = self.wait_for_clickable((By.XPATH, station_xpath), time=5)
            station_option.click()
            return
        except TimeoutException:
            pass
        
        try:
            station_xpath = f"//div[contains(text(), '{station_name}')]"
            station_option = self.wait_for_clickable((By.XPATH, station_xpath), time=5)
            station_option.click()
            return
        except TimeoutException:
            pass
        
        first_option = self.find_element(self.METRO_STATION_OPTIONS)
        first_option.click()

    @allure.step("Заполнить вторую страницу формы заказа")
    def fill_order_form_second_step(self, date, period, color, comment):
        self.wait_for_visibility(self.DATE_INPUT)
        date_input = self.find_element(self.DATE_INPUT)
        date_input.clear()
        date_input.send_keys(date)
        date_input.send_keys(Keys.ENTER)
        self.select_rental_period(period)
        
        if color:
            color_locator = (By.ID, color)
            self.click_element(color_locator)
        
        if comment:
            self.find_element(self.COMMENT_INPUT).send_keys(comment)
        
        self.scroll_to_element(self.ORDER_BUTTON)
        self.click_element(self.ORDER_BUTTON)
        self.wait_for_clickable(self.CONFIRM_BUTTON)
        self.click_element(self.CONFIRM_BUTTON)

    @allure.step("Выбрать период аренды: {period}")
    def select_rental_period(self, period):
        self.click_element(self.RENTAL_PERIOD_DROPDOWN)
        self.wait_for_visibility((By.CLASS_NAME, "Dropdown-menu"))
        
        try:
            period_xpath = f"//div[text()='{period}']"
            period_option = self.wait_for_clickable((By.XPATH, period_xpath), time=5)
            period_option.click()
            return
        except TimeoutException:
            pass
        
        first_option = self.find_element(self.RENTAL_PERIOD_OPTIONS)
        first_option.click()

    @allure.step("Получить сообщение об успешном оформлении заказа")
    def get_success_message(self):
        self.wait_for_visibility(self.SUCCESS_MESSAGE)
        return self.find_element(self.SUCCESS_MESSAGE).text