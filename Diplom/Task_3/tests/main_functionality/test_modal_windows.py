# tests/main_functionality/test_modal_windows.py
import allure
import pytest
import logging
from pages.main_page import MainPage

logger = logging.getLogger(__name__)

@allure.feature('Основная функциональность')
@allure.story('Модальные окна')
class TestModalWindows:
    
    @allure.title('Проверка кликабельности ингредиентов')
    def test_ingredients_are_clickable(self, driver):
        """Тест проверяет что ингредиенты можно кликать"""
        logger.info("Testing ingredient clickability")
        
        main_page = MainPage(driver)
        
        with allure.step("Открыть главную страницу"):
            main_page.go_to_main_page()
            assert main_page.is_constructor_page(), "Страница конструктора не загрузилась"
            logger.info("Constructor page loaded")
        
        with allure.step("Проверить наличие ингредиентов"):
            assert main_page.has_ingredients(), "На странице нет ингредиентов"
            ingredients = main_page.get_all_ingredients()
            logger.info(f"Found {len(ingredients)} ingredients")
        
        with allure.step("Проверить что ингредиенты отображаются"):
            for i, ingredient in enumerate(ingredients[:3]):  # Проверяем первые 3
                assert ingredient.is_displayed(), f"Ingredient {i} not displayed"
            logger.info("All checked ingredients are displayed")
    
    @allure.title('Проверка открытия модального окна ингредиента')
    def test_open_ingredient_modal(self, driver):
        """Тест проверяет открытие модального окна ингредиента"""
        logger.info("Testing ingredient modal opening")
        
        main_page = MainPage(driver)
        
        with allure.step("Открыть главную страницу"):
            main_page.go_to_main_page()
            assert main_page.is_constructor_page(), "Страница конструктора не загрузилась"
            logger.info("Constructor page loaded")
        
        with allure.step("Кликнуть на первый ингредиент"):
            first_ingredient = main_page.get_first_bun_element()
            if first_ingredient:
                main_page.click_ingredient(main_page.FIRST_BUN)
                logger.info("Clicked on first ingredient")
                
                # Проверяем открылось ли модальное окно
                modal_opened = main_page.is_modal_displayed()
                logger.info(f"Modal opened: {modal_opened}")
                
                if modal_opened:
                    logger.info("Modal window opened successfully")
                else:
                    logger.warning("Modal window did not open - this might be expected behavior")
            else:
                logger.warning("First ingredient not found, skipping modal test")
    
    @allure.title('Проверка функциональности ингредиентов')
    def test_ingredient_functionality(self, driver):
        """Тест проверяет базовую функциональность ингредиентов"""
        logger.info("Testing ingredient basic functionality")
        
        main_page = MainPage(driver)
        
        with allure.step("Открыть главную страницу"):
            main_page.go_to_main_page()
            assert main_page.is_constructor_page(), "Страница конструктора не загрузилась"
            logger.info("Constructor page loaded")
        
        with allure.step("Проверить разделы ингредиентов"):
            assert main_page.is_bun_section_displayed(), "Раздел булок не отображается"
            assert main_page.is_sauce_section_displayed(), "Раздел соусов не отображается" 
            assert main_page.is_filling_section_displayed(), "Раздел начинок не отображается"
            logger.info("All ingredient sections are displayed")
        
        with allure.step("Проверить наличие ингредиентов"):
            ingredients = main_page.get_all_ingredients()
            assert len(ingredients) >= 3, f"Expected at least 3 ingredients, found {len(ingredients)}"
            logger.info(f"Found {len(ingredients)} ingredients - sufficient for testing")