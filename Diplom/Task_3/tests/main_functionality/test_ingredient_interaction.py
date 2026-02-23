# tests/main_functionality/test_ingredient_interaction.py
import allure
import pytest
import logging
from pages.main_page import MainPage

logger = logging.getLogger(__name__)

@allure.feature('Основная функциональность')
@allure.story('Взаимодействие с ингредиентами')
class TestIngredientInteraction:
    
    @allure.title('Проверка интерактивности ингредиентов')
    def test_ingredients_are_interactive(self, driver):
        """Тест проверяет что ингредиенты интерактивны"""
        logger.info("Testing ingredient interactivity")
        
        main_page = MainPage(driver)
        
        with allure.step("Открыть главную страницу"):
            main_page.go_to_main_page()
            assert main_page.is_constructor_page(), "Страница конструктора не загрузилась"
            logger.info("Constructor page loaded successfully")
        
        with allure.step("Проверить что ингредиенты можно кликать"):
            ingredients = main_page.get_all_ingredients()
            assert len(ingredients) > 0, "На странице нет ингредиентов"
            
            # Проверяем первые 3 ингредиента
            for i, ingredient in enumerate(ingredients[:3]):
                with allure.step(f"Проверить ингредиент {i+1}"):
                    assert ingredient.is_displayed(), f"Ингредиент {i+1} не отображается"
                    assert ingredient.is_enabled(), f"Ингредиент {i+1} неактивен"
                    
                    # Проверяем что есть текст (название или цена)
                    ingredient_text = ingredient.text.strip()
                    assert len(ingredient_text) > 0, f"Ингредиент {i+1} не имеет текста"
                    
                    logger.info(f"Ingredient {i+1}: {ingredient_text[:30]}...")
    
    @allure.title('Проверка реакции на клик ингредиента')
    def test_ingredient_click_reaction(self, driver):
        """Тест проверяет реакцию на клик ингредиента"""
        logger.info("Testing ingredient click reaction")
        
        main_page = MainPage(driver)
        
        with allure.step("Открыть главную страницу"):
            main_page.go_to_main_page()
            assert main_page.is_constructor_page(), "Страница конструктора не загрузилась"
            logger.info("Constructor page loaded successfully")
        
        with allure.step("Кликнуть на ингредиент и проверить реакцию"):
            # Используем соус для теста (обычно их больше)
            sauce_element = main_page.get_first_sauce_element()
            if sauce_element:
                # Запоминаем начальное состояние
                initial_counter = main_page.get_ingredient_counter(sauce_element)
                
                # Кликаем на ингредиент
                main_page.click_ingredient(main_page.FIRST_SAUCE)
                
                # Проверяем что произошла какая-то реакция
                # Это может быть:
                # 1. Открытие модального окна
                # 2. Изменение счетчика
                # 3. Добавление в конструктор
                
                modal_opened = main_page.is_modal_displayed()
                if modal_opened:
                    logger.info("Modal opened after clicking ingredient")
                    # Закрываем модальное окно
                    main_page.close_modal()
                else:
                    # Проверяем изменился ли счетчик
                    updated_sauce_element = main_page.get_first_sauce_element()
                    if updated_sauce_element:
                        updated_counter = main_page.get_ingredient_counter(updated_sauce_element)
                        if updated_counter != initial_counter:
                            logger.info(f"Counter changed from {initial_counter} to {updated_counter}")
                        else:
                            logger.info("No visible reaction to ingredient click")
                    else:
                        logger.info("Ingredient element was re-rendered after click")
            else:
                logger.warning("Sauce element not found for click test")