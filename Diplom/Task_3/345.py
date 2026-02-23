# Проверяем что нет print в проекте
import subprocess
result = subprocess.run(['grep', '-r', 'print(', 'tests/', 'pages/', 'utils/'], 
                      capture_output=True, text=True)
print("Print statements found:", bool(result.stdout))

# Проверяем что все методы BasePage используются
result = subprocess.run(['grep', '-r', 'driver\\.', 'tests/'], 
                      capture_output=True, text=True)
print("Direct driver calls in tests:", bool(result.stdout))

# Проверяем что нет time.sleep
result = subprocess.run(['grep', '-r', 'time\\.sleep', 'tests/', 'pages/'], 
                      capture_output=True, text=True)
print("Time.sleep found:", bool(result.stdout))