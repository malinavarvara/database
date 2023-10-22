from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sql_table import insert_user

def is_element_exist_by_id(driver, id):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, id)))
    except TimeoutException:
        return False

def is_element_exist_by(driver,by, id):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((by, id)))
    except TimeoutException:
        return False


def user_parser(url):
    # Создание дравера с опциями (чтобы не спамил ошибками)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    # Открываем веб-сайт
    driver.get(url)

    try:
        name = driver.find_element(By.CLASS_NAME, "desktop-channel-layout__header-wrapper").text.strip()
        words=name.split('\n')
        user_name=words[0]
        n_followers=words[1]
        n_followers=n_followers.replace(',', '.')
        n=0
        if 'K' in n_followers: n= float(n_followers[:-1])*1000
        elif 'M' in n_followers: n= float(n_followers[:-1]) * 1000000
        else: n=n_followers
        description=''
        for i in range(len(words)-2):
            if i>2: description=description+words[i]+'\n'

        #достаю аву
        while is_element_exist_by(driver,By.CLASS_NAME,"desktop-channel-layout__avatar") == False:
            print(1)
        photo = driver.find_element(By.CLASS_NAME, "desktop-channel-layout__avatar")

        # достаю ссылку
        text = photo.get_attribute('innerHTML')
        url_pattern = r'https://[\S]+'
        urls = re.findall(url_pattern, text)
        image=urls[0]
        insert_user(user_name, url, image[:-9], description, n)
        return [user_name,url,image[:-9],description,n]

    except Exception as e:
        print("Элемент не найден. Завершение.")
        print(type(e), e)
    driver.quit()


if __name__ == '__main__':
    test_url = 'https://dzen.ru/tastyminute'
    user_parser(test_url)