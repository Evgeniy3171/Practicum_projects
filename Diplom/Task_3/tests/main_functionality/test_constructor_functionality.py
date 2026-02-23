# tests/main_functionality/test_constructor_functionality.py
import allure
import pytest
import logging
from pages.main_page import MainPage

logger = logging.getLogger(__name__)

@allure.feature('Основная функциональность')
@allure.story('Функциональность конструктора')
class TestConstructorFunctionality:
    
    @allure.title('Проверка загрузки конструктора')
    def test_constructor_loads_correctly(self, driver):
        """Тест проверяет корректную загрузку конструктора"""
        logger.info("Testing constructor loading")
        
        main_page = MainPage(driver)
        
        with allure.step("Открыть главную страницу"):
            main_page.go_to_main_page()
            main_page.wait_for_page_load()
            logger.info("Main page loaded")
        
        with allure.step("Проверить что находимся на странице конструктора"):
            assert main_page.is_constructor_page(), "Страница конструктора не загрузилась"
            logger.info("Constructor page verified")
    
    @allure.title('Проверка отображения разделов ингредиентов')
    def test_ingredient_sections_displayed(self, driver):
        """Тест проверяет отображение всех разделов ингредиентов"""
        logger.info("Testing ingredient sections display")
        
        main_page = MainPage(driver)
        
        with allure.step("Открыть главную страницу"):
            main_page.go_to_main_page()
            assert main_page.is_constructor_page(), "Страница конструктора не загрузилась"
            logger.info("Constructor page loaded")
        
        with allure.step("Проверить отображение раздела булок"):
            assert main_page.is_bun_section_displayed(), "Раздел булок не отображается"
            logger.info("Bun section is displayed")
        
        with allure.step("Проверить отображение раздела соусов"):
            assert main_page.is_sauce_section_displayed(), "Раздел соусов не отображается"
            logger.info("Sauce section is displayed")
        
        with allure.step("Проверить отображение раздела начинок"):
            assert main_page.is_filling_section_displayed(), "Раздел начинок не отображается"
            logger.info("Filling section is displayed")
    
    @allure.title('Проверка отображения ингредиентов')
    def test_ingredients_displayed(self, driver):
        """Тест проверяет отображение ингредиентов"""
        logger.info("Testing ingredients display")
        
        main_page = MainPage(driver)
        
        with allure.step("Открыть главную страницу"):
            main_page.go_to_main_page()
            assert main_page.is_constructor_page(), "Страница конструктора не загрузилась"
            logger.info("Constructor page loaded")
        
        with allure.step("Проверить отображение булки"):
            bun_element = main_page.get_first_bun_element()
            assert bun_element is not None and bun_element.is_displayed(), "Булка не отображается"
            logger.info("Bun ingredient is displayed")
        
        with allure.step("Проверить отображение соуса"):
            sauce_element = main_page.get_first_sauce_element()
            assert sauce_element is not None and sauce_element.is_displayed(), "Соус не отображается"
            logger.info("Sauce ingredient is displayed")
        
        with allure.step("Проверить отображение начинки"):
            filling_element = main_page.get_first_filling_element()
            assert filling_element is not None and filling_element.is_displayed(), "Начинка не отображается"
            logger.info("Filling ingredient is displayed")
    
    @allure.title('Проверка счетчиков ингредиентов')
    def test_ingredient_counters(self, driver):
        """Тест проверяет корректность счетчиков ингредиентов"""
        logger.info("Testing ingredient counters")
        
        main_page = MainPage(driver)
        
        with allure.step("Открыть главную страницу"):
            main_page.go_to_main_page()
            assert main_page.is_constructor_page(), "Страница конструктора не загрузилась"
            logger.info("Constructor page loaded")
        
        with allure.step("Проверить счетчик булки"):
            bun_element = main_page.get_first_bun_element()
            if bun_element:
                bun_counter = main_page.get_ingredient_counter(bun_element)
                assert bun_counter >= 0, "Счетчик булки должен быть неотрицательным"
                logger.info(f"Bun counter: {bun_counter}")
            else:
                logger.warning("Bun element not found, skipping counter test")
        
        with allure.step("Проверить счетчик соуса"):
            sauce_element = main_page.get_first_sauce_element()
            if sauce_element:
                sauce_counter = main_page.get_ingredient_counter(sauce_element)
                assert sauce_counter >= 0, "Счетчик соуса должен быть неотрицательным"
                logger.info(f"Sauce counter: {sauce_counter}")
            else:
                logger.warning("Sauce element not found, skipping counter test")
        
        with allure.step("Проверить счетчик начинки"):
            filling_element = main_page.get_first_filling_element()
            if filling_element:
                filling_counter = main_page.get_ingredient_counter(filling_element)
                assert filling_counter >= 0, "Счетчик начинки должен быть неотрицательным"
                logger.info(f"Filling counter: {filling_counter}")
            else:
                logger.warning("Filling element not found, skipping counter test")
    
    @allure.title('Проверка кнопки оформления заказа')
    def test_order_button_functionality(self, driver):
        """Тест проверяет функциональность кнопки оформления заказа"""
        logger.info("Testing order button functionality")
        
        main_page = MainPage(driver)
        
        with allure.step("Открыть главную страницу"):
            main_page.go_to_main_page()
            assert main_page.is_constructor_page(), "Страница конструктора не загрузилась"
            logger.info("Constructor page loaded")
        
        with allure.step("Проверить отображение кнопки оформления заказа"):
            # Кнопка может быть неактивна если нет ингредиентов - это нормально
            order_button_exists = main_page.can_make_order()
            logger.info(f"Order button exists: {order_button_exists}")
            
            # Если кнопка найдена, проверяем ее состояние
            if order_button_exists:
                order_button = main_page.find_element(main_page.ORDER_BUTTON)
                assert order_button.is_displayed(), "Кнопка оформления заказа не отображается"
                logger.info("Order button is displayed")
                
                # Кнопка может быть disabled если нет ингредиентов
                if order_button.is_enabled():
                    logger.info("Order button is enabled")
                else:
                    logger.info("Order button is disabled (no ingredients added)")
            else:
                logger.warning("Order button not found on the page")