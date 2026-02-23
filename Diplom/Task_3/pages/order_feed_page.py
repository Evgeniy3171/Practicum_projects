# pages/order_feed_page.py
import allure
import logging
from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class OrderFeedPage(BasePage):
    # Счётчики заказов
    TOTAL_ORDERS = (By.XPATH, "//p[contains(text(), 'Выполнено за всё время') or contains(text(), 'Выполнено за все время')]/following-sibling::p")
    TODAY_ORDERS = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")
    
    # Заказы в работе
    ORDERS_IN_PROGRESS_SECTION = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady') or contains(@class, 'orderListReady')]")
    ORDERS_IN_PROGRESS = (By.XPATH, ".//li")
    
    # Заголовок страницы
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(), 'Лента заказов')] | //h1[contains(., 'заказов')]")
    
    # Заказы в ленте
    ORDER_CARDS = (By.XPATH, "//div[contains(@class, 'OrderHistory_listContainer')]//li")
    
    @allure.step("Перейти на страницу ленты заказов")
    def go_to_order_feed(self):
        logger.info("Navigating to order feed page")
        # Используем метод из BasePage, а не рекурсивный вызов
        self.go_to_url(self.urls.ORDER_FEED)
        self.wait_for_page_load()
    
    @allure.step("Ожидать загрузки страницы ленты заказов")
    def wait_for_page_load(self, timeout=15):
        logger.debug("Waiting for order feed page to load")
        try:
            self.wait.until(EC.presence_of_element_located(self.PAGE_TITLE))
        except:
            try:
                self.wait.until(EC.presence_of_element_located(self.TOTAL_ORDERS))
            except:
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'заказ')]")))
    
    @allure.step("Получить количество заказов за всё время")
    def get_total_orders_count(self):
        try:
            count_text = self.get_element_text(self.TOTAL_ORDERS)
            count = int(count_text) if count_text.strip().isdigit() else 0
            logger.debug(f"Total orders count: {count}")
            return count
        except Exception as e:
            logger.warning(f"Error getting total orders count: {e}")
            return 0
    
    @allure.step("Получить количество заказов за сегодня")
    def get_today_orders_count(self):
        try:
            count_text = self.get_element_text(self.TODAY_ORDERS)
            count = int(count_text) if count_text.strip().isdigit() else 0
            logger.debug(f"Today orders count: {count}")
            return count
        except Exception as e:
            logger.warning(f"Error getting today orders count: {e}")
            return 0
    
    @allure.step("Получить список заказов в работе")
    def get_orders_in_progress(self):
        try:
            section = self.find_element(self.ORDERS_IN_PROGRESS_SECTION)
            orders = section.find_elements(*self.ORDERS_IN_PROGRESS)
            order_texts = [order.text.strip() for order in orders if order.text.strip()]
            logger.debug(f"Orders in progress: {len(order_texts)}")
            return order_texts
        except Exception as e:
            logger.warning(f"Error getting orders in progress: {e}")
            return []
    
    @allure.step("Получить количество заказов в ленте")
    def get_order_cards_count(self):
        try:
            orders = self.find_elements(self.ORDER_CARDS)
            count = len(orders)
            logger.debug(f"Order cards count: {count}")
            return count
        except Exception as e:
            logger.warning(f"Error getting order cards count: {e}")
            return 0
    
    @allure.step("Проверить что находимся на странице ленты заказов")
    def is_order_feed_page(self):
        current_url = self.get_current_url()
        is_feed_page = self.urls.ORDER_FEED in current_url
        logger.debug(f"Is order feed page: {is_feed_page}")
        return is_feed_page
    
    @allure.step("Проверить отображение счетчика за всё время")
    def is_total_orders_displayed(self):
        return self.is_element_visible(self.TOTAL_ORDERS)
    
    @allure.step("Проверить отображение счетчика за сегодня")
    def is_today_orders_displayed(self):
        return self.is_element_visible(self.TODAY_ORDERS)
    
    @allure.step("Проверить отображение раздела заказов в работе")
    def is_orders_in_progress_displayed(self):
        return self.is_element_visible(self.ORDERS_IN_PROGRESS_SECTION)
    
    @allure.step("Проверить отображение заголовка страницы")
    def is_page_title_displayed(self):
        return self.is_element_visible(self.PAGE_TITLE)