# conftest.py
import pytest
import os
import logging
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", 
                    help="browser to run tests: chrome or firefox")

def get_driver_path(browser_name):
    """Получаем путь к драйверу из переменных окружения"""
    env_var_name = f"{browser_name.upper()}_DRIVER_PATH"
    driver_path = os.getenv(env_var_name)
    
    if driver_path and os.path.exists(driver_path):
        logger.info(f"Using driver from environment variable {env_var_name}: {driver_path}")
        return driver_path
    
    # По умолчанию используем драйвер в папке проекта
    if browser_name == "chrome":
        default_path = os.path.join(os.path.dirname(__file__), "drivers", "chromedriver.exe")
    elif browser_name == "firefox":
        default_path = os.path.join(os.path.dirname(__file__), "drivers", "geckodriver.exe")
    else:
        default_path = None
    
    if default_path and os.path.exists(default_path):
        logger.info(f"Using default driver path: {default_path}")
        return default_path
    
    logger.info("No driver path found, will use webdriver-manager")
    return None

@pytest.fixture
def driver(request):
    browser_name = request.config.getoption("--browser").lower()
    
    logger.info(f"Initializing {browser_name} driver")
    
    driver_instance = None
    
    try:
        if browser_name == "chrome":
            options = ChromeOptions()
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            driver_path = get_driver_path("chrome")
            
            if driver_path:
                logger.info(f"Using ChromeDriver from: {driver_path}")
                service = ChromeService(driver_path)
                driver_instance = webdriver.Chrome(service=service, options=options)
            else:
                from webdriver_manager.chrome import ChromeDriverManager
                service = ChromeService(ChromeDriverManager().install())
                driver_instance = webdriver.Chrome(service=service, options=options)
                logger.info("ChromeDriver initialized via webdriver-manager")
            
        elif browser_name == "firefox":
            options = FirefoxOptions()
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            
            driver_path = get_driver_path("firefox")
            
            if driver_path:
                logger.info(f"Using GeckoDriver from: {driver_path}")
                service = FirefoxService(driver_path)
                driver_instance = webdriver.Firefox(service=service, options=options)
            else:
                from webdriver_manager.firefox import GeckoDriverManager
                service = FirefoxService(GeckoDriverManager().install())
                driver_instance = webdriver.Firefox(service=service, options=options)
                logger.info("GeckoDriver initialized via webdriver-manager")
        
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        # Общие настройки
        driver_instance.implicitly_wait(10)
        driver_instance.set_page_load_timeout(30)
        
        logger.info(f"{browser_name.capitalize()} driver initialized successfully")
        
        yield driver_instance
        
    except Exception as e:
        logger.error(f"Failed to initialize {browser_name} driver: {e}")
        pytest.skip(f"Could not initialize {browser_name} driver: {e}")
    
    finally:
        if driver_instance:
            try:
                driver_instance.quit()
                logger.info("Driver closed successfully")
            except Exception as e:
                logger.warning(f"Error while closing driver: {e}")

@pytest.fixture(autouse=True)
def take_screenshot_on_failure(request, driver):
    """Фикстура для автоматического создания скриншотов при падении тестов"""
    yield
    
    # Создаем скриншот только при падении теста
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        try:
            # Используем метод из BasePage для создания скриншота
            from pages.base_page import BasePage
            base_page = BasePage(driver)
            screenshot = base_page.take_screenshot()
            
            allure.attach(
                screenshot,
                name=f"screenshot_failure_{request.node.name}",
                attachment_type=allure.attachment_type.PNG
            )
            logger.info(f"Screenshot taken for failed test: {request.node.name}")
        except Exception as e:
            logger.warning(f"Could not take screenshot: {e}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для получения статуса выполнения теста"""
    outcome = yield
    rep = outcome.get_result()
    
    # Устанавливаем атрибут rep_call для использования в фикстурах
    setattr(item, "rep_" + rep.when, rep)

def pytest_configure(config):
    """Настройка логирования для pytest"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )