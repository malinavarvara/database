import sys, traceback

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from sql_table import insert_post
from utils import number_to_changes, is_element_exist_by
from post_comment_parcer import post_comment_parser

def user_post_parser(url):
    # Создание дравера с опциями (чтобы не спамил ошибками)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    # Открываем веб-сайт
    driver.get(url)
    # Здесь можно заменить на int и просто приписывать "zen-row-"
    current_id = 0
    current_id_txt = f'zen-row-{current_id}'
    while current_id != 20:
        try:
            # Поиск элемента с текущим id
            element = driver.find_element(By.ID, current_id_txt)
            # ссылка
            text = element.get_attribute('innerHTML')
            type_txt=''
            if 'card-brief _platform_desktop' in text:
                type_txt='Пост'
            elif 'Карточка статьи' in text:
                type_txt = 'Статья'
            elif 'Карточка видео' in text:
                type_txt = 'Видео'
            url_pattern = r'https://[\S]+'
            urls = re.findall(url_pattern, text)
            if len(urls) != 0:
                likes = 0
                comments = 0
                NUMERIC_PATTERN = re.compile(r'.*[кнопке\"|/svg]>(.*)</span>')
                # likes
                likes_str = element.find_element(By.CLASS_NAME, "zen-ui-button-like__content").get_attribute('innerHTML')
                likes_str = re.sub(NUMERIC_PATTERN,r'\1',likes_str)
                likes = number_to_changes(likes_str)
                # comments
                comments_str = element.find_element(By.CLASS_NAME, "zen-ui-button-footer__content").get_attribute('innerHTML')
                comments_str = re.sub(NUMERIC_PATTERN,r'\1',comments_str)
                comments = number_to_changes(comments_str)
                urls_post = urls[len(urls) - 1]
                insert_post(url, likes, comments, urls_post[:-1], type_txt)
                if(comments>0):
                    post_comment_parser(urls_post[:-1])
            # Перейдите к следующему id
            current_id = current_id + 1
            current_id_txt = 'zen-row-' + str(current_id)
            scroll_count = 0
            while is_element_exist_by(driver, By.ID, current_id_txt) is False and scroll_count < 3:
                scroll_count += 1
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if is_element_exist_by(driver, By.ID, current_id_txt) is False:
                #print("Конец страницы")
                break
        except NoSuchElementException:
            break
        except Exception:
            exc = sys.exception()
            print("*** print_exception:")
            traceback.print_exception(exc, limit=2, file=sys.stdout)
            print("*** print_exc:")
            traceback.print_exc(limit=2, file=sys.stdout)
            break
    driver.quit()

if __name__ == '__main__':
    test_url = 'https://dzen.ru/id/622efc792366414af12ed1f3'
    user_post_parser(test_url)