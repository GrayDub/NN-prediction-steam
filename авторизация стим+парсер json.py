from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Настройка для видимого режима
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# Путь к новому ChromeDriver (укажите здесь обновленный путь)
chrome_driver_path = "C:/Users/User/.cache/selenium/chromedriver/win64/130.0.6723.58/chromedriver.exe"

# Запуск браузера
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Переход на страницу входа
    driver.get("https://store.steampowered.com/login/")

    # Ожидание загрузки страницы и нахождение элементов логина и пароля
    wait = WebDriverWait(driver, 10)
    username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']._2GBWeup5cttgbTw8FM3tfx")))
    password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']._2GBWeup5cttgbTw8FM3tfx")))

    # Ввод логина и пароля
    username_input.send_keys("sulatevandrej07")
    password_input.send_keys("0p9o8i7u6yY")
    
    # Отправка формы
    password_input.send_keys(Keys.RETURN)

    # Ожидание успешного входа
    time.sleep(5)

    # Переход на страницу профиля пользователя
    driver.get("https://steamcommunity.com/profiles/76561199035908600/")

    # Ожидание загрузки страницы и нахождение элемента с именем пользователя
    persona_name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "actual_persona_name")))

    # Получение текста элемента
    persona_name_text = persona_name.text
    print("Persona Name:", persona_name_text)

    # Переход на страницу ценовой истории
    driver.get("https://steamcommunity.com/market/pricehistory/?country=DE&currency=3&appid=440&market_hash_name=Specialized%20Killstreak%20Brass%20Beast")

    # Ожидание загрузки страницы и получения JSON данных
    time.sleep(5)  # Даем время на загрузку данных
    page_source = driver.page_source

    # Парсинг JSON из page_source
    start_index = page_source.find('{')
    end_index = page_source.rfind('}') + 1
    json_data = page_source[start_index:end_index]

    # Преобразование строки JSON в словарь Python
    data = json.loads(json_data)
    
    # Вывод данных в консоль
    print(json.dumps(data, indent=4))

finally:
    # Закрытие браузера
    driver.quit()
