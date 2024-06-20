from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pickle

# метод для авторизации через куки и получения токена из кода страницы
def login_and_get_token_by_cookie(cookies, proxy):
    # ChromeOptions с указанием прокси
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy}')

    # Инициализация драйвера браузера (в данном случае Chrome)
    driver = webdriver.Chrome(options=chrome_options)

    # Открытие страницы Facebook для установки домена
    driver.get('https://www.facebook.com/')

    # Добавляем куки в драйвер
    for cookie in cookies:
        driver.add_cookie(cookie)

    # Теперь мы можем перейти на страницу, к которой хотим получить доступ
    driver.get('https://www.facebook.com/adsmanager/manage/')

    # Ждем, пока страница полностью загрузится
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Выполнение JavaScript кода для получения значения window.__accessToken
    access_token = driver.execute_script("return window.__accessToken")

    # Выводим access token
    print(f"Access Token: {access_token}")

    # Закрываем драйвер
    driver.quit()

    return access_token
