from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sql_table import insert_user

from utils import is_element_exist_by, number_to_changes

import sys, traceback

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
        n_followers_str=words[1]
        n_followers = number_to_changes(n_followers_str)
        description='\n'.join(words[3:-2])

        #достаю аву
        while is_element_exist_by(driver,By.CLASS_NAME,"desktop-channel-layout__avatar") is False:
            pass
        photo = driver.find_element(By.CLASS_NAME, "desktop-channel-layout__avatar")

        # достаю ссылку
        text = photo.get_attribute('innerHTML')
        url_pattern = r'https://[\S]+'
        urls = re.findall(url_pattern, text)
        if len(urls)>0:
            image = urls[0]
            image = image[:-9]
        else:
            image = 'Нет аватарки' 
            
        insert_user(user_name, url, image, description, n_followers)
        return [user_name,url,image,description,n_followers]

    except Exception:
        exc = sys.exception()
        print("*** print_exception:")
        traceback.print_exception(exc, limit=2, file=sys.stdout)
        print("*** print_exc:")
        traceback.print_exc(limit=2, file=sys.stdout)
    driver.quit()


if __name__ == '__main__':
    test_url = 'https://dzen.ru/user/8c9dcm93t0v8hatujpv4w0rj1r'
    user_parser(test_url)