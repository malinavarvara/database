from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from insert_users import user_parser


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

def user_post_parser(url):
    # Создание дравера с опциями (чтобы не спамил ошибками)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    # Открываем веб-сайт
    driver.get(url)

    current_id = 0
    current_id_txt='zen-row-'+str(current_id)

    while current_id!=5:
        try:
            # Поиск элемента с текущим id
            print(current_id)
            element = driver.find_element(By.ID, current_id_txt)
            element_text = element.get_attribute('innerHTML')
            if 'card-wrapper _is-desktop _theme_white _with-border' in element_text:
                while is_element_exist_by(driver, By.CLASS_NAME, "zen-ui-channel-info__title-and-veryfied-mark-wrapper") == False:
                    print(1)
                user_text = element.find_element(By.CLASS_NAME, "zen-ui-channel-info__title-and-veryfied-mark-wrapper")
                # достаю ссылку
                text = user_text.get_attribute('innerHTML')
                url_pattern = r'https://[\S]+'
                urls = re.findall(url_pattern, text)
                url=urls[0]
                user_parser(url[:-1])

            # Перейдите к следующему id
            current_id = current_id+1
            current_id_txt = 'zen-row-' + str(current_id)

            scroll_count = 0
            while is_element_exist_by_id(driver, current_id_txt) == False and scroll_count < 3:
                scroll_count += 1
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            if is_element_exist_by_id(driver, current_id_txt) == False:
                print("Конец страницы")
                break
        except Exception as e:
            # Если элемент не был найден, завершите цикл
            print("Элемент не найден. Завершение.")
            print(type(e), e)
            break
    driver.quit()


if __name__ == '__main__':
    test_url = 'https://dzen.ru/articles'
    user_post_parser(test_url)