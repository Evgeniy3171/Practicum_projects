import pytest
import allure
from pages.main_page import MainPage
from pages.order_page import OrderPage


class TestOrder:
    ORDER_DATA = [
        ("Иван", "Петров", "ул. Тверская, 1", "Библиотека им. Ленина", "+79211234567", "01.01.2025", "сутки", "black", "Жду у подъезда"),
        ("Мария", "Сидорова", "Невский пр-т, 100", "Невский проспект", "+79117654321", "02.02.2025", "двое суток", "grey", "Позвонить за час")
    ]

    @pytest.mark.parametrize("name, last_name, address, metro_station, phone, date, period, color, comment", ORDER_DATA)
    @allure.title("Тест заказа через верхнюю кнопку: {name} {last_name}")
    def test_order_via_top_button(self, driver, name, last_name, address, metro_station, phone, date, period, color, comment):
        main_page = MainPage(driver)
        main_page.go_to_site()
        main_page.click_top_order_button()
        
        order_page = OrderPage(driver)
        order_page.fill_order_form_first_step(name, last_name, address, metro_station, phone)
        order_page.fill_order_form_second_step(date, period, color, comment)
        
        assert "Заказ оформлен" in order_page.get_success_message()

    @pytest.mark.parametrize("name, last_name, address, metro_station, phone, date, period, color, comment", ORDER_DATA)
    @allure.title("Тест заказа через нижнюю кнопку: {name} {last_name}")
    def test_order_via_bottom_button(self, driver, name, last_name, address, metro_station, phone, date, period, color, comment):
        main_page = MainPage(driver)
        main_page.go_to_site()
        main_page.click_bottom_order_button()
        
        order_page = OrderPage(driver)
        order_page.fill_order_form_first_step(name, last_name, address, metro_station, phone)
        order_page.fill_order_form_second_step(date, period, color, comment)
        
        assert "Заказ оформлен" in order_page.get_success_message()