# run_all_tests.py
import subprocess
import sys

def run_tests():
    """Запуск всех тестов для Chrome"""
    print("🚀 Запуск всех тестов для Chrome...")
    
    # Команда для запуска
    command = [
        "pytest",
        "tests/",
        "--browser=chrome",
        "-v",
        "-s",
        "--tb=short",
        "--alluredir=allure-results",
        "-k", "not firefox"  # Исключаем Firefox тесты
    ]
    
    print(f"📋 Команда: {' '.join(command)}")
    
    # Запускаем
    result = subprocess.run(command)
    
    if result.returncode == 0:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    else:
        print("❌ ЕСТЬ НЕУДАЧНЫЕ ТЕСТЫ")
    
    return result.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)