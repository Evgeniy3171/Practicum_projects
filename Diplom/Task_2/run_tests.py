#!/usr/bin/env python3
import subprocess
import sys
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def run_tests():
    """Запуск тестов и генерация отчета"""
    
    logger.info("Запуск тестов Stellar Burgers API")
    
    # Шаг 1: Запуск тестов
    logger.info("Выполнение тестов...")
    result = subprocess.run([
        "pytest", 
        "--alluredir=allure-results",
        "-v"
    ], capture_output=True, text=True)
    
    logger.info(result.stdout)
    if result.stderr:
        logger.error("Ошибки: %s", result.stderr)
    
    # Шаг 2: Генерация отчета Allure
    logger.info("Генерация отчета Allure...")
    try:
        # Пытаемся использовать allure serve
        subprocess.run(["allure", "serve", "allure-results"], check=True)
    except subprocess.CalledProcessError:
        logger.error("Allure serve не доступен, пытаемся generate + open...")
        try:
            subprocess.run(["allure", "generate", "allure-results", "-o", "allure-report", "--clean"], check=True)
            logger.info("Отчет сгенерирован: allure-report/index.html")
        except subprocess.CalledProcessError as e:
            logger.error("Ошибка генерации отчета: %s", e)
            logger.info("Установите Allure:")
            logger.info("   Windows: choco install allure")
            logger.info("   Mac: brew install allure") 
            logger.info("   Linux: sudo apt install allure")
    
    # Шаг 3: Статус выполнения
    if result.returncode == 0:
        logger.info("Все тесты прошли успешно!")
    else:
        logger.info("Некоторые тесты не прошли. Код возврата: %s", result.returncode)
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(run_tests())