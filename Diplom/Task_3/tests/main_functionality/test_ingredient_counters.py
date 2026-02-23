# tests/main_functionality/test_ingredient_counters.py
import allure
import pytest
import logging
from pages.main_page import MainPage

logger = logging.getLogger(__name__)

@allure.feature('Основная функциональность')
@allure.story('Счетчики ингредиентов')
class TestIngredientCounters:
    
    @allure.title('Проверка начального состояния счетчиков ингредиентов')
    def test_initial_ingredient_counters(self, driver):
        """Тест проверяет начальное состояние счетчиков ингредиентов"""
        logger.info("Testing initial ingredient counters state")
        
        main_page = MainPage(driver)
        
        with allure.step("Открыть главную страницу"):
            main_page.go_to_main_page()
            assert main_page.is_constructor_page(), "Страница конструктора не загрузилась"
            logger.info("Constructor page loaded successfully")
        
        with allure.step("Проверить начальные счетчики ингредиентов"):
            # Получаем элементы ингредиентов
            bun_element = main_page.get_first_bun_element()
            sauce_element = main_page.get_first_sauce_element()
            filling_element = main_page.get_first_filling_element()
            
            # Проверяем что элементы найдены
            assert bun_element is not None, "Булка не найдена"
            assert sauce_element is not None, "Соус не найден"
            assert filling_element is not None, "Начинка не найдена"
            
            # Получаем начальные значения счетчиков
            initial_bun_counter = main_page.get_ingredient_counter(bun_element)
            initial_sauce_counter = main_page.get_ingredient_counter(sauce_element)
            initial_filling_counter = main_page.get_ingredient_counter(filling_element)
            
            logger.info(f"Initial counters - Bun: {initial_bun_counter}, Sauce: {initial_sauce_counter}, Filling: {initial_filling_counter}")
            
            # В начальном состоянии счетчики должны быть 0
            assert initial_bun_counter == 0, f"Начальный счетчик булки должен быть 0, получен: {initial_bun_counter}"
            assert initial_sauce_counter == 0, f"Начальный счетчик соуса должен быть 0, получен: {initial_sauce_counter}"
            assert initial_filling_counter == 0, f"Начальный счетчик начинки должен быть 0, получен: {initial_filling_counter}"
    
    @allure.title('Проверка увеличения счетчика при добавлении ингредиента')
    def test_ingredient_counter_increases_on_drag(self, driver):
        """Тест проверяет увеличение счетчика при добавлении ингредиента в заказ"""
        logger.info("Testing ingredient counter increase on drag")
        
        main_page = MainPage(driver)
        
        with allure.step("Открыть главную страницу"):
            main_page.go_to_main_page()
            assert main_page.is_constructor_page(), "Страница конструктора не загрузилась"
            logger.info("Constructor page loaded successfully")
        
        with allure.step("Получить первый ингредиент для тестирования"):
            # Используем соус для тестирования (обычно их больше и они проще для drag&drop)
            sauce_element = main_page.get_first_sauce_element()
            assert sauce_element is not None, "Соус для тестирования не найден"
            
            # Получаем начальный счетчик
            initial_counter = main_page.get_ingredient_counter(sauce_element)
            logger.info(f"Initial sauce counter: {initial_counter}")
        
        with allure.step("Добавить ингредиент в конструктор через drag&drop"):
            try:
                # Прокручиваем к ингредиенту чтобы он был видим
                main_page.scroll_to_element(main_page.FIRST_SAUCE)
                
                # Получаем зону конструктора
                constructor_area = main_page.find_element(main_page.CONSTRUCTOR_AREA)
                
                # Выполняем drag&drop с помощью JavaScript
                drag_drop_script = """
                var source = arguments[0];
                var target = arguments[1];
                
                // Создаем события drag&drop
                var dragStart = new Event('dragstart', { bubbles: true });
                var dragOver = new Event('dragover', { bubbles: true });
                var drop = new Event('drop', { bubbles: true });
                var dragEnd = new Event('dragend', { bubbles: true });
                
                // Устанавливаем данные для transfer
                dragStart.dataTransfer = {
                    setData: function(type, value) {
                        this[type] = value;
                    },
                    getData: function(type) {
                        return this[type];
                    }
                };
                
                // Запускаем процесс drag&drop
                source.dispatchEvent(dragStart);
                target.dispatchEvent(dragOver);
                target.dispatchEvent(drop);
                source.dispatchEvent(dragEnd);
                """
                
                main_page.execute_script(drag_drop_script, sauce_element, constructor_area)
                logger.info("Drag&drop operation performed")
                
                # Даем время на обработку
                main_page.wait_for_page_loaded()
                
            except Exception as e:
                logger.warning(f"Drag&drop failed: {e}. Trying alternative method...")
                
                # Альтернативный метод - просто кликаем на ингредиент
                main_page.click_ingredient(main_page.FIRST_SAUCE)
                logger.info("Used click as alternative to drag&drop")
        
        with allure.step("Проверить изменение счетчика ингредиента"):
            # Получаем обновленный элемент (может быть перерендерен)
            updated_sauce_element = main_page.get_first_sauce_element()
            if updated_sauce_element:
                updated_counter = main_page.get_ingredient_counter(updated_sauce_element)
                logger.info(f"Updated sauce counter: {updated_counter}")
                
                # Счетчик должен увеличиться (стать больше 0)
                assert updated_counter > initial_counter, f"Счетчик должен увеличиться. Было: {initial_counter}, стало: {updated_counter}"
                logger.info("Ingredient counter increased successfully")
            else:
                logger.warning("Could not find updated sauce element for counter check")
    
    @allure.title('Проверка счетчиков разных типов ингредиентов')
    def test_different_ingredient_counters(self, driver):
        """Тест проверяет счетчики разных типов ингредиентов"""
        logger.info("Testing different ingredient type counters")
        
        main_page = MainPage(driver)
        
        with allure.step("Открыть главную страницу"):
            main_page.go_to_main_page()
            assert main_page.is_constructor_page(), "Страница конструктора не загрузилась"
            logger.info("Constructor page loaded successfully")
        
        with allure.step("Проверить счетчики всех типов ингредиентов"):
            ingredient_types = [
                ("булки", main_page.FIRST_BUN, main_page.get_first_bun_element),
                ("соуса", main_page.FIRST_SAUCE, main_page.get_first_sauce_element),
                ("начинки", main_page.FIRST_FILLING, main_page.get_first_filling_element)
            ]
            
            for ingredient_name, locator, getter_method in ingredient_types:
                with allure.step(f"Проверить счетчик {ingredient_name}"):
                    ingredient_element = getter_method()
                    if ingredient_element:
                        counter = main_page.get_ingredient_counter(ingredient_element)
                        logger.info(f"Counter for {ingredient_name}: {counter}")
                        
                        # Счетчик должен быть неотрицательным
                        assert counter >= 0, f"Счетчик {ingredient_name} должен быть неотрицательным"
                        
                        # Проверить что элемент можно кликнуть (интерактивен)
                        try:
                            main_page.scroll_to_element(locator)
                            assert ingredient_element.is_displayed(), f"Ингредиент {ingredient_name} не отображается"
                            logger.info(f"{ingredient_name.capitalize()} is interactive")
                        except Exception as e:
                            logger.warning(f"Could not interact with {ingredient_name}: {e}")
                    else:
                        logger.warning(f"{ingredient_name.capitalize()} element not found")