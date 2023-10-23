from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from insert_users import user_parser
from user_post_parcer import user_post_parser_zher
from sql_table import delete_repeat

from utils import is_element_exist_by, links_to_changes

def main_page_users_parcing():
    DZEN_MAIN_PAGE_URL = 'https://dzen.ru/articles'
    # Создание дравера с опциями (чтобы не спамил ошибками)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    # Открываем веб-сайт
    driver.get(DZEN_MAIN_PAGE_URL)

    current_id = 0
    current_id_txt='zen-row-'+str(current_id)

    while current_id!=5:
        try:
            # Поиск элемента с текущим id
            element = driver.find_element(By.ID, current_id_txt)
            element_text = element.get_attribute('innerHTML')
            if 'card-wrapper _is-desktop _theme_white _with-border' in element_text:
                while is_element_exist_by(driver, By.CLASS_NAME, "zen-ui-channel-info__title-and-veryfied-mark-wrapper") is False:
                    pass
                user_text = links_to_changes(element.find_element(By.CLASS_NAME, "zen-ui-channel-info__title-and-veryfied-mark-wrapper"))
                user_parser(user_text)
                user_post_parser_zher(user_text)

            # Перейдите к следующему id
            current_id = current_id+1
            current_id_txt = 'zen-row-' + str(current_id)

            scroll_count = 0
            while is_element_exist_by(driver,By.ID, current_id_txt) is False and scroll_count < 3:
                scroll_count += 1
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            if is_element_exist_by(driver,By.ID, current_id_txt) is False:
                print("Конец страницы")
                break
        except Exception as e:
            # Если элемент не был найден, завершите цикл
            print("Элемент не найден. Завершение.")
            print(type(e), e)
            break
    driver.quit()


if __name__ == '__main__':
    main_page_users_parcing()
    delete_repeat()
