# config/settings.py
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Settings:
    """Настройки проекта из переменных окружения"""
    
    # Пути к драйверам
    CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
    FIREFOX_DRIVER_PATH = os.getenv("FIREFOX_DRIVER_PATH")
    
    # URL приложения
    BASE_URL = "https://stellarburgers.education-services.ru"
    
    # Настройки тестирования
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    
    # Настройки логирования
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Создаем экземпляр настроек
settings = Settings()