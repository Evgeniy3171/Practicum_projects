# tests/order_feed/test_order_counters.py
import allure
import pytest
import logging
from pages.order_feed_page import OrderFeedPage

logger = logging.getLogger(__name__)

@allure.feature('Лента заказов')
@allure.story('Счетчики заказов')
class TestOrderCounters:
    
    @allure.title('Проверка отображения счетчика заказов за все время')
    def test_total_orders_counter_displayed(self, driver):
        """Тест проверяет отображение счетчика заказов за все время"""
        logger.info("Testing total orders counter display")
        
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step("Открыть ленту заказов"):
            order_feed_page.go_to_order_feed()
            order_feed_page.wait_for_page_load()
            assert order_feed_page.is_order_feed_page()
            logger.info("Order feed page loaded successfully")
        
        with allure.step("Проверить отображение счетчика за все время"):
            assert order_feed_page.is_total_orders_displayed()
            logger.info("Total orders counter is displayed")
    
    @allure.title('Проверка отображения счетчика заказов за сегодня')
    def test_today_orders_counter_displayed(self, driver):
        """Тест проверяет отображение счетчика заказов за сегодня"""
        logger.info("Testing today orders counter display")
        
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step("Открыть ленту заказов"):
            order_feed_page.go_to_order_feed()
            order_feed_page.wait_for_page_load()
            assert order_feed_page.is_order_feed_page()
            logger.info("Order feed page loaded successfully")
        
        with allure.step("Проверить отображение счетчика за сегодня"):
            assert order_feed_page.is_today_orders_displayed()
            logger.info("Today orders counter is displayed")
    
    @allure.title('Проверка корректности счетчика заказов за все время')
    def test_total_orders_counter_value(self, driver):
        """Тест проверяет корректность значения счетчика заказов за все время"""
        logger.info("Testing total orders counter value")
        
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step("Открыть ленту заказов"):
            order_feed_page.go_to_order_feed()
            order_feed_page.wait_for_page_load()
            assert order_feed_page.is_order_feed_page()
            logger.info("Order feed page loaded successfully")
        
        with allure.step("Получить значение счетчика за все время"):
            total_orders = order_feed_page.get_total_orders_count()
            logger.info(f"Total orders count: {total_orders}")
            
            # Счетчик должен быть неотрицательным числом
            assert total_orders >= 0
            logger.info("Total orders counter value is valid")
    
    @allure.title('Проверка корректности счетчика заказов за сегодня')
    def test_today_orders_counter_value(self, driver):
        """Тест проверяет корректность значения счетчика заказов за сегодня"""
        logger.info("Testing today orders counter value")
        
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step("Открыть ленту заказов"):
            order_feed_page.go_to_order_feed()
            order_feed_page.wait_for_page_load()
            assert order_feed_page.is_order_feed_page()
            logger.info("Order feed page loaded successfully")
        
        with allure.step("Получить значение счетчика за сегодня"):
            today_orders = order_feed_page.get_today_orders_count()
            logger.info(f"Today orders count: {today_orders}")
            
            # Счетчик должен быть неотрицательным числом
            assert today_orders >= 0
            logger.info("Today orders counter value is valid")