# tests/order_feed/test_orders_in_progress.py
import allure
import pytest
import logging
from pages.order_feed_page import OrderFeedPage

logger = logging.getLogger(__name__)

@allure.feature('Лента заказов')
@allure.story('Заказы в работе')
class TestOrdersInProgress:
    
    @allure.title('Проверка отображения раздела заказов в работе')
    def test_orders_in_progress_section_displayed(self, driver):
        """Тест проверяет отображение раздела заказов в работе"""
        logger.info("Testing orders in progress section display")
        
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step("Открыть ленту заказов"):
            order_feed_page.go_to_order_feed()
            order_feed_page.wait_for_page_load()
            assert order_feed_page.is_order_feed_page()
            logger.info("Order feed page loaded successfully")
        
        with allure.step("Проверить отображение раздела заказов в работе"):
            assert order_feed_page.is_orders_in_progress_displayed()
            logger.info("Orders in progress section is displayed")
    
    @allure.title('Проверка получения списка заказов в работе')
    def test_get_orders_in_progress_list(self, driver):
        """Тест проверяет получение списка заказов в работе"""
        logger.info("Testing orders in progress list retrieval")
        
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step("Открыть ленту заказов"):
            order_feed_page.go_to_order_feed()
            order_feed_page.wait_for_page_load()
            assert order_feed_page.is_order_feed_page()
            logger.info("Order feed page loaded successfully")
        
        with allure.step("Получить список заказов в работе"):
            orders_in_progress = order_feed_page.get_orders_in_progress()
            logger.info(f"Found {len(orders_in_progress)} orders in progress")
            
            # Проверяем что метод возвращает список (может быть пустым)
            assert isinstance(orders_in_progress, list)
            logger.info("Orders in progress list retrieved successfully")