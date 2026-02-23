# setup_geckodriver.py
import os
import requests
import zipfile
import platform
import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def download_geckodriver():
    """Скачивает и устанавливает GeckoDriver для Firefox"""
    logger.info("Downloading GeckoDriver...")
    
    # Определяем версию для Windows
    url = "https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-win64.zip"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Сохраняем архив
            zip_path = "geckodriver.zip"
            with open(zip_path, "wb") as f:
                f.write(response.content)
            logger.info("GeckoDriver downloaded successfully")
            
            # Создаем папку drivers если её нет
            if not os.path.exists("drivers"):
                os.makedirs("drivers")
            
            # Распаковываем
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall("drivers")
            
            # Переименовываем если нужно
            geckodriver_path = os.path.join("drivers", "geckodriver.exe")
            temp_path = os.path.join("drivers", "geckodriver")
            
            if os.path.exists(temp_path):
                os.rename(temp_path, geckodriver_path)
            
            logger.info(f"GeckoDriver installed to: {geckodriver_path}")
            
            # Проверяем что файл валидный
            if os.path.exists(geckodriver_path):
                file_size = os.path.getsize(geckodriver_path)
                logger.info(f"GeckoDriver file size: {file_size} bytes")
                
                # Очистка временных файлов
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                
                return True
            else:
                logger.error("geckodriver.exe not found after extraction")
                return False
        else:
            logger.error(f"Download failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"Error downloading GeckoDriver: {e}")
        return False

def test_geckodriver():
    """Тестирует установленный GeckoDriver"""
    driver_path = os.path.join("drivers", "geckodriver.exe")
    
    if not os.path.exists(driver_path):
        logger.error("GeckoDriver not found")
        return False
    
    try:
        logger.info("Testing GeckoDriver...")
        options = Options()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        service = Service(driver_path)
        driver = webdriver.Firefox(service=service, options=options)
        
        # Тестируем на правильном сайте
        driver.get("https://stellarburgers.education-services.ru/")
        
        logger.info(f"Page loaded successfully: {driver.title}")
        logger.info(f"Current URL: {driver.current_url}")
        
        driver.quit()
        logger.info("GeckoDriver test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"GeckoDriver test failed: {e}")
        return False

def main():
    setup_logging()
    logger.info("Starting GeckoDriver setup...")
    
    # Проверяем, не установлен ли уже GeckoDriver
    driver_path = os.path.join("drivers", "geckodriver.exe")
    if os.path.exists(driver_path):
        logger.info("GeckoDriver already exists, testing...")
        if test_geckodriver():
            logger.info("GeckoDriver is working correctly")
            return
        else:
            logger.warning("Existing GeckoDriver is not working, reinstalling...")
    
    # Устанавливаем GeckoDriver
    if download_geckodriver():
        if test_geckodriver():
            logger.info("✅ GeckoDriver setup completed successfully!")
        else:
            logger.error("❌ GeckoDriver test failed after installation")
    else:
        logger.error("❌ GeckoDriver installation failed")

if __name__ == "__main__":
    main()