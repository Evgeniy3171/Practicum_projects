# pages/main_page.py
import allure
import logging
from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class MainPage(BasePage):
    # Навигация - на основе диагностики
    CONSTRUCTOR_BUTTON = (By.XPATH, "//a[contains(@href, '/')] | //p[contains(text(), 'Конструктор')]")
    ORDER_FEED_BUTTON = (By.XPATH, "//a[contains(@href, '/feed')] | //p[contains(text(), 'Лента заказов')]")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//a[contains(@href, '/account')] | //p[contains(text(), 'Личный Кабинет')]")
    
    # Разделы ингредиентов - на основе диагностики
    BUN_SECTION = (By.XPATH, "//h2[text()='Булки'] | //h2[contains(text(), 'Булки')]")
    SAUCE_SECTION = (By.XPATH, "//h2[text()='Соусы'] | //h2[contains(text(), 'Соусы')]")
    FILLING_SECTION = (By.XPATH, "//h2[text()='Начинки'] | //h2[contains(text(), 'Начинки')]")
    
    # Ингредиенты - правильные локаторы из диагностики
    INGREDIENTS_CONTAINER = (By.XPATH, "//section[contains(@class, 'BurgerIngredients')]")
    INGREDIENT_CARDS = (By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient__1TVf6')]")
    FIRST_BUN = (By.XPATH, "(//a[contains(@class, 'BurgerIngredient_ingredient__1TVf6')])[1]")
    FIRST_SAUCE = (By.XPATH, "(//a[contains(@class, 'BurgerIngredient_ingredient__1TVf6')])[3]")  # 3-й элемент обычно первый соус
    FIRST_FILLING = (By.XPATH, "(//a[contains(@class, 'BurgerIngredient_ingredient__1TVf6')])[5]")  # 5-й элемент обычно первая начинка
    
    # Счётчики ингредиентов
    INGREDIENT_COUNTER = (By.XPATH, ".//div[contains(@class, 'counter')] | .//span[contains(@class, 'counter')]")
    
    # Конструктор
    CONSTRUCTOR_AREA = (By.XPATH, "//section[contains(@class, 'BurgerConstructor')]")
    
    # Модальное окно - правильные локаторы из диагностики
    MODAL_CONTENT = (By.XPATH, "//div[contains(@class, 'Modal_modal__')] | //section[contains(@class, 'Modal_modal__')]")
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modalOverlay__')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close_')] | //div[contains(@class, 'Modal_modal__close_')]")
    
    # Кнопка оформления заказа
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    
    @allure.step("Перейти на главную страницу")
    def go_to_main_page(self):
        logger.info("Navigating to main page")
        self.go_to_url(self.urls.MAIN_PAGE)
        self.wait_for_page_load()
    
    @allure.step("Ожидать загрузки главной страницы")
    def wait_for_page_load(self):
        logger.debug("Waiting for main page to load")
        # Ждем контейнер ингредиентов
        try:
            self.wait.until(EC.presence_of_element_located(self.INGREDIENTS_CONTAINER))
        except:
            # Если не нашли, ждем любой ингредиент
            try:
                self.wait.until(EC.presence_of_element_located(self.INGREDIENT_CARDS))
            except:
                logger.warning("Main page elements not found")
    
    @allure.step("Кликнуть на конструктор")
    def click_constructor(self):
        logger.debug("Clicking on constructor")
        self.safe_click(self.CONSTRUCTOR_BUTTON)
        self.wait_for_page_load()
    
    @allure.step("Кликнуть на ленту заказов")
    def click_order_feed(self):
        logger.debug("Clicking on order feed")
        self.safe_click(self.ORDER_FEED_BUTTON)
        self.wait_for_url_contains("feed")
    
    @allure.step("Кликнуть на личный кабинет")
    def click_personal_account(self):
        logger.debug("Clicking on personal account")
        self.safe_click(self.PERSONAL_ACCOUNT_BUTTON)
        # После клика на личный кабинет должна открыться страница логина
        self.wait_for_url_contains("login")
    
    @allure.step("Кликнуть на ингредиент")
    def click_ingredient(self, ingredient_locator):
        logger.debug(f"Clicking on ingredient: {ingredient_locator}")
        # Прокручиваем к ингредиенту чтобы он был видим
        self.scroll_to_element(ingredient_locator)
        self.safe_click(ingredient_locator)
        # Ждем появления модального окна
        try:
            self.wait.until(EC.visibility_of_element_located(self.MODAL_CONTENT))
        except:
            logger.warning("Modal window did not appear after clicking ingredient")
    
    @allure.step("Закрыть модальное окно")
    def close_modal(self):
        logger.debug("Closing modal window")
        if self.is_modal_displayed():
            # Сначала пробуем кликнуть на overlay
            try:
                self.safe_click(self.MODAL_OVERLAY)
            except:
                # Если overlay не сработал, пробуем кнопку закрытия
                try:
                    self.safe_click(self.MODAL_CLOSE_BUTTON)
                except:
                    logger.warning("Could not close modal window")
            self.wait_for_element_to_disappear(self.MODAL_CONTENT)
    
    @allure.step("Проверить отображение модального окна")
    def is_modal_displayed(self):
        is_displayed = self.is_element_visible(self.MODAL_CONTENT)
        logger.debug(f"Modal displayed: {is_displayed}")
        return is_displayed
    
    @allure.step("Получить значение счетчика ингредиента")
    def get_ingredient_counter(self, ingredient_element):
        try:
            counter_elements = ingredient_element.find_elements(*self.INGREDIENT_COUNTER)
            for element in counter_elements:
                counter_text = element.text.strip()
                if counter_text and counter_text.isdigit():
                    counter_value = int(counter_text)
                    logger.debug(f"Ingredient counter value: {counter_value}")
                    return counter_value
            logger.debug("Ingredient counter not found or zero")
            return 0
        except Exception as e:
            logger.warning(f"Error getting ingredient counter: {e}")
            return 0
    
    @allure.step("Проверить возможность оформления заказа")
    def can_make_order(self):
        try:
            can_order = self.is_element_visible(self.ORDER_BUTTON)
            logger.debug(f"Can make order: {can_order}")
            return can_order
        except Exception as e:
            logger.warning(f"Error checking order button: {e}")
            return False
    
    @allure.step("Проверить видимость конструктора")
    def is_constructor_visible(self):
        try:
            is_visible = self.is_element_visible(self.CONSTRUCTOR_AREA)
            logger.debug(f"Constructor visible: {is_visible}")
            return is_visible
        except Exception as e:
            logger.warning(f"Error checking constructor visibility: {e}")
            return False
    
    @allure.step("Проверить что находимся на странице конструктора")
    def is_constructor_page(self):
        try:
            current_url = self.get_current_url()
            is_constructor = current_url == self.urls.MAIN_PAGE
            logger.debug(f"Is constructor page: {is_constructor}")
            return is_constructor
        except Exception as e:
            logger.warning(f"Error checking constructor page: {e}")
            return False
    
    @allure.step("Получить элемент первой булки")
    def get_first_bun_element(self):
        try:
            return self.find_element(self.FIRST_BUN)
        except Exception as e:
            logger.warning(f"Error getting first bun element: {e}")
            return None
    
    @allure.step("Получить элемент первого соуса")
    def get_first_sauce_element(self):
        try:
            return self.find_element(self.FIRST_SAUCE)
        except Exception as e:
            logger.warning(f"Error getting first sauce element: {e}")
            return None
    
    @allure.step("Получить элемент первой начинки")
    def get_first_filling_element(self):
        try:
            return self.find_element(self.FIRST_FILLING)
        except Exception as e:
            logger.warning(f"Error getting first filling element: {e}")
            return None
    
    @allure.step("Проверить отображение раздела булок")
    def is_bun_section_displayed(self):
        try:
            return self.is_element_visible(self.BUN_SECTION)
        except Exception as e:
            logger.warning(f"Error checking bun section: {e}")
            return False
    
    @allure.step("Проверить отображение раздела соусов")
    def is_sauce_section_displayed(self):
        try:
            return self.is_element_visible(self.SAUCE_SECTION)
        except Exception as e:
            logger.warning(f"Error checking sauce section: {e}")
            return False
    
    @allure.step("Проверить отображение раздела начинок")
    def is_filling_section_displayed(self):
        try:
            return self.is_element_visible(self.FILLING_SECTION)
        except Exception as e:
            logger.warning(f"Error checking filling section: {e}")
            return False
    
    @allure.step("Получить все ингредиенты")
    def get_all_ingredients(self):
        """Получить все карточки ингредиентов"""
        try:
            ingredients = self.find_elements(self.INGREDIENT_CARDS)
            logger.debug(f"Found {len(ingredients)} ingredients")
            return ingredients
        except Exception as e:
            logger.warning(f"Error getting ingredients: {e}")
            return []
    
    @allure.step("Проверить отображение кнопки конструктора")
    def is_constructor_button_displayed(self):
        try:
            return self.is_element_visible(self.CONSTRUCTOR_BUTTON)
        except Exception as e:
            logger.warning(f"Error checking constructor button: {e}")
            return False

    @allure.step("Проверить отображение кнопки ленты заказов")
    def is_order_feed_button_displayed(self):
        try:
            return self.is_element_visible(self.ORDER_FEED_BUTTON)
        except Exception as e:
            logger.warning(f"Error checking order feed button: {e}")
            return False

    @allure.step("Проверить отображение кнопки личного кабинета")
    def is_personal_account_button_displayed(self):
        """Проверить отображение кнопки личного кабинета"""
        try:
            return self.is_element_visible(self.PERSONAL_ACCOUNT_BUTTON)
        except Exception as e:
            logger.warning(f"Error checking personal account button: {e}")
            return False

    @allure.step("Получить все ингредиенты")
    def get_all_ingredients(self):
        """Получить все карточки ингредиентов"""
        try:
            ingredients = self.find_elements(self.INGREDIENT_CARDS)
            logger.debug(f"Found {len(ingredients)} ingredients")
            return ingredients
        except Exception as e:
            logger.warning(f"Error getting ingredients: {e}")
            return []

    @allure.step("Проверить наличие ингредиентов на странице")
    def has_ingredients(self):
        """Проверить что на странице есть ингредиенты"""
        ingredients = self.get_all_ingredients()
        return len(ingredients) > 0
    
    @allure.step("Добавить ингредиент в конструктор")
    def add_ingredient_to_constructor(self, ingredient_locator):
        """Добавляет ингредиент в конструктор через drag&drop"""
        logger.debug(f"Adding ingredient to constructor: {ingredient_locator}")
        try:
            # Пробуем drag&drop
            success = self.drag_and_drop(ingredient_locator, self.CONSTRUCTOR_AREA)
            if success:
                logger.info("Ingredient added via drag&drop")
                return True
            else:
                # Fallback - просто кликаем на ингредиент
                logger.info("Using click as fallback for adding ingredient")
                self.click_ingredient(ingredient_locator)
                return True
        except Exception as e:
            logger.error(f"Failed to add ingredient: {e}")
            return False

    @allure.step("Получить счетчик ингредиента по локатору")
    def get_ingredient_counter_by_locator(self, ingredient_locator):
        """Получает счетчик ингредиента по его локатору"""
        try:
            ingredient_element = self.find_element(ingredient_locator)
            return self.get_ingredient_counter(ingredient_element)
        except Exception as e:
            logger.warning(f"Error getting counter by locator: {e}")
            return 0
    
