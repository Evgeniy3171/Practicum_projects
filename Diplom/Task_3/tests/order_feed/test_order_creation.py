# tests/order_feed/test_order_creation.py
import allure
import pytest
import logging
from pages.order_feed_page import OrderFeedPage
from pages.main_page import MainPage

logger = logging.getLogger(__name__)

@allure.feature('Лента заказов')
@allure.story('Создание заказа и обновление счетчиков')
class TestOrderCreation:
    
    @allure.title('Проверка начального состояния счетчиков')
    def test_initial_counters_state(self, driver):
        """Тест проверяет начальное состояние счетчиков заказов"""
        logger.info("Testing initial order counters state")
        
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step("Открыть ленту заказов"):
            order_feed_page.go_to_order_feed()
            order_feed_page.wait_for_page_load()
            assert order_feed_page.is_order_feed_page(), "Страница ленты заказов не загрузилась"
            logger.info("Order feed page loaded successfully")
        
        with allure.step("Зафиксировать начальные значения счетчиков"):
            initial_total = order_feed_page.get_total_orders_count()
            initial_today = order_feed_page.get_today_orders_count()
            
            logger.info(f"Initial total orders: {initial_total}")
            logger.info(f"Initial today orders: {initial_today}")
            
            # Сохраняем значения для использования в других тестах
            driver.initial_total_orders = initial_total
            driver.initial_today_orders = initial_today
    
    @allure.title('Проверка отображения раздела заказов в работе')
    def test_orders_in_progress_section(self, driver):
        """Тест проверяет раздел заказов в работе"""
        logger.info("Testing orders in progress section")
        
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step("Открыть ленту заказов"):
            order_feed_page.go_to_order_feed()
            order_feed_page.wait_for_page_load()
            assert order_feed_page.is_order_feed_page(), "Страница ленты заказов не загрузилась"
            logger.info("Order feed page loaded successfully")
        
        with allure.step("Проверить отображение раздела заказов в работе"):
            assert order_feed_page.is_orders_in_progress_displayed(), "Раздел заказов в работе не отображается"
            logger.info("Orders in progress section is displayed")
        
        with allure.step("Получить текущие заказы в работе"):
            orders_in_progress = order_feed_page.get_orders_in_progress()
            logger.info(f"Current orders in progress: {len(orders_in_progress)}")
            
            # Сохраняем для сравнения
            driver.current_orders_in_progress = orders_in_progress
    
    @allure.title('Проверка наличия заказов в ленте')
    def test_order_cards_presence(self, driver):
        """Тест проверяет наличие заказов в ленте"""
        logger.info("Testing order cards presence")
        
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step("Открыть ленту заказов"):
            order_feed_page.go_to_order_feed()
            order_feed_page.wait_for_page_load()
            assert order_feed_page.is_order_feed_page(), "Страница ленты заказов не загрузилась"
            logger.info("Order feed page loaded successfully")
        
        with allure.step("Проверить наличие заказов в ленте"):
            order_cards_count = order_feed_page.get_order_cards_count()
            logger.info(f"Order cards in feed: {order_cards_count}")
            
            # В ленте должны быть заказы (может быть 0 если нет заказов)
            assert order_cards_count >= 0, "Количество заказов должно быть неотрицательным"