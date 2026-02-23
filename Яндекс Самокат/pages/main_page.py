from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class MainPage(BasePage):
    # Локаторы
    SCOOTER_LOGO = (By.XPATH, "//a[@href='/']")
    YANDEX_LOGO = (By.XPATH, "//a[@href='//yandex.ru']")
    ORDER_BUTTON_TOP = (By.XPATH, "//button[text()='Заказать' and contains(@class, 'Button_Button__ra12g')]")
    ORDER_BUTTON_BOTTOM = (By.XPATH, "//div[contains(@class, 'Home_FinishButton')]//button[text()='Заказать']")
    
    # Локаторы для вопросов
    QUESTION_LOCATOR = "//div[contains(text(), '{}')]/.."
    ANSWER_LOCATOR = "//div[contains(text(), '{}')]/../following-sibling::div//p"

    @allure.step("Нажать на вопрос: {question_text}")
    def click_question(self, question_text):
        question_locator = (By.XPATH, self.QUESTION_LOCATOR.format(question_text))
        self.scroll_to_element(question_locator)
        self.wait_for_clickable(question_locator)
        self.click_element(question_locator)
        
        answer_locator = (By.XPATH, self.ANSWER_LOCATOR.format(question_text))
        self.wait_for_visibility(answer_locator)
        return self.find_element(answer_locator).text

    @allure.step("Нажать на логотип Самоката")
    def click_scooter_logo(self):
        self.click_element(self.SCOOTER_LOGO)

    @allure.step("Нажать на логотип Яндекса")
    def click_yandex_logo(self):
        self.click_element(self.YANDEX_LOGO)

    @allure.step("Нажать верхнюю кнопку заказа")
    def click_top_order_button(self):
        self.click_element(self.ORDER_BUTTON_TOP)

    @allure.step("Нажать нижнюю кнопку заказа")
    def click_bottom_order_button(self):
        self.scroll_to_bottom()
        self.wait_for_visibility(self.ORDER_BUTTON_BOTTOM)
        self.click_element(self.ORDER_BUTTON_BOTTOM)