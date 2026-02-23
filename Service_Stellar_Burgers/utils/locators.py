from selenium.webdriver.common.by import By

class MainPageLocators:
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//p[text()='Личный Кабинет']")
    CONSTRUCTOR_BUTTON = (By.XPATH, "//a[contains(@href, '/') and contains(@class, 'AppHeader_header__link')]")
    LOGO = (By.XPATH, "//div[contains(@class, 'AppHeader_header__logo')]")
    BUNS_SECTION = (By.XPATH, "//span[text()='Булки']/ancestor::div[contains(@class, 'tab_tab__1SPyG')]")
    SAUCES_SECTION = (By.XPATH, "//span[text()='Соусы']/ancestor::div[contains(@class, 'tab_tab__1SPyG')]")
    TOPPINGS_SECTION = (By.XPATH, "//span[text()='Начинки']/ancestor::div[contains(@class, 'tab_tab__1SPyG')]")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")

class LoginPageLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    REGISTER_LINK = (By.XPATH, "//a[text()='Зарегистрироваться']")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[text()='Восстановить пароль']")
    LOGIN_LINK = (By.XPATH, "//a[text()='Войти']")

class RegistrationPageLocators:
    NAME_INPUT = (By.XPATH, "//label[text()='Имя']/following-sibling::input")
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    PASSWORD_INPUT = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")
    REGISTER_BUTTON = (By.XPATH, "//button[text()='Зарегистрироваться']")
    LOGIN_LINK = (By.XPATH, "//a[text()='Войти']")
    ERROR_MESSAGE = (By.XPATH, "//p[contains(@class, 'input__error')]")

class PersonalAccountLocators:
    PROFILE_LINK = (By.XPATH, "//a[text()='Профиль']")
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")
    CONSTRUCTOR_LINK = (By.XPATH, "//a[text()='Конструктор']")