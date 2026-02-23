# run.py
import subprocess
import sys
import logging
import os

logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def main():
    setup_logging()
    
    logger.info("🚀 Stellar Burgers Test Suite")
    logger.info("=" * 50)
    
    # Проверяем наличие ChromeDriver
    driver_path = os.path.join("drivers", "chromedriver.exe")
    if not os.path.exists(driver_path):
        logger.warning("ChromeDriver not found. Please run: python setup_chromedriver.py")
        return 1
    
    # Запускаем тесты
    logger.info("Starting tests...")
    
    command = [
        "pytest",
        "tests/",
        "--browser=chrome",
        "-v",
        "--tb=short",
        "--alluredir=allure-results",
        "-k", "not firefox"
    ]
    
    try:
        # Используем Popen для лучшего контроля
        process = subprocess.Popen(command)
        process.wait()
        return process.returncode
    except KeyboardInterrupt:
        logger.info("Test execution interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)