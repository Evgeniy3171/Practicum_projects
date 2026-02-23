# setup_chromedriver.py
import os
import requests
import zipfile
import subprocess
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def download_chromedriver():
    """Скачивает и устанавливает ChromeDriver"""
    logger.info("Downloading ChromeDriver...")
    
    # Используем стабильную версию
    version = "122.0.6261.69"
    url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/win64/chromedriver-win64.zip"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Сохраняем архив
            zip_path = "chromedriver.zip"
            with open(zip_path, "wb") as f:
                f.write(response.content)
            logger.info("ChromeDriver downloaded successfully")
            
            # Создаем папку drivers если её нет
            if not os.path.exists("drivers"):
                os.makedirs("drivers")
            
            # Распаковываем
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall("drivers_temp")
            
            # Находим chromedriver.exe
            chromedriver_path = None
            for root, dirs, files in os.walk("drivers_temp"):
                for file in files:
                    if file == "chromedriver.exe":
                        chromedriver_path = os.path.join(root, file)
                        break
            
            if chromedriver_path:
                # Копируем в папку drivers
                final_path = os.path.join("drivers", "chromedriver.exe")
                with open(chromedriver_path, "rb") as src, open(final_path, "wb") as dst:
                    dst.write(src.read())
                
                logger.info(f"ChromeDriver installed to: {final_path}")
                
                # Проверяем что файл валидный
                file_size = os.path.getsize(final_path)
                logger.info(f"ChromeDriver file size: {file_size} bytes")
                
                # Очистка временных файлов
                import shutil
                if os.path.exists("drivers_temp"):
                    shutil.rmtree("drivers_temp")
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                
                return True
            else:
                logger.error("chromedriver.exe not found in archive")
                return False
        else:
            logger.error(f"Download failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"Error downloading ChromeDriver: {e}")
        return False

def test_chromedriver():
    """Тестирует установленный ChromeDriver"""
    driver_path = os.path.join("drivers", "chromedriver.exe")
    
    if not os.path.exists(driver_path):
        logger.error("ChromeDriver not found")
        return False
    
    try:
        logger.info("Testing ChromeDriver...")
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        # Тестируем на правильном сайте
        driver.get("https://stellarburgers.education-services.ru/")
        
        logger.info(f"Page loaded successfully: {driver.title}")
        logger.info(f"Current URL: {driver.current_url}")
        
        # Проверяем ключевые элементы
        page_text = driver.page_source
        if "Конструктор" in page_text or "бургер" in page_text.lower():
            logger.info("Key page elements found")
        else:
            logger.warning("Key page elements not found")
        
        driver.quit()
        logger.info("ChromeDriver test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"ChromeDriver test failed: {e}")
        return False

def main():
    setup_logging()
    logger.info("Starting ChromeDriver setup...")
    
    # Проверяем, не установлен ли уже ChromeDriver
    driver_path = os.path.join("drivers", "chromedriver.exe")
    if os.path.exists(driver_path):
        logger.info("ChromeDriver already exists, testing...")
        if test_chromedriver():
            logger.info("ChromeDriver is working correctly")
            return
        else:
            logger.warning("Existing ChromeDriver is not working, reinstalling...")
    
    # Устанавливаем ChromeDriver
    if download_chromedriver():
        if test_chromedriver():
            logger.info("✅ ChromeDriver setup completed successfully!")
        else:
            logger.error("❌ ChromeDriver test failed after installation")
    else:
        logger.error("❌ ChromeDriver installation failed")

if __name__ == "__main__":
    main()