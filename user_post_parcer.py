from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sql_table import insert_post


def is_element_exist_by_id(driver, id):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, id)))
    except TimeoutException:
        return False


def number_to_changesz(name):
    name = name[:-7]
    index = 0
    likes = 0
    if name[len(name) - 1].isdigit() or name[len(name) - 2].isdigit():
        for i in reversed(range(0, len(name))):
            if name[i].isdigit() and not (name[i - 1].isdigit()) and not (name[i - 2].isdigit()):
                index = i
                break
        name = name[index:]
        name = name.replace(',', '.')
        if 'K' in name:
            likes = float(name[:-1]) * 1000
        elif 'M' in name:
            likes = float(name[:-1]) * 1000000
        else:
            likes = int(name)
    return likes


def user_post_parser_zher(url):
    # Создание дравера с опциями (чтобы не спамил ошибками)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    # Открываем веб-сайт
    driver.get(url)
    # Здесь можно заменить на int и просто приписывать "zen-row-"
    current_id = 0
    current_id_txt = 'zen-row-' + str(current_id)

    while current_id != 6:
        try:
            # Поиск элемента с текущим id
            element = driver.find_element(By.ID, current_id_txt)
            # ссылка
            text = element.get_attribute('innerHTML')
            url_pattern = r'https://[\S]+'
            urls = re.findall(url_pattern, text)
            if len(urls) != 0:
                likes = 0
                comments = 0
                # likes
                name = element.find_element(By.CLASS_NAME, "zen-ui-button-like__content").get_attribute('innerHTML')
                likes = number_to_changesz(name)
                # comments
                name = element.find_element(By.CLASS_NAME, "zen-ui-button-footer__content").get_attribute('innerHTML')
                comments = number_to_changesz(name)
                if comments > 0:
                    comments_url = element.find_element(By.CLASS_NAME,
                                                        "card-layer-channel-footer-view__social-meta").get_attribute(
                        'innerHTML')
                    url_pattern_com = r'https://[\S]+'
                    urls_com = re.findall(url_pattern_com, comments_url)
                    print(urls_com)

                urls_post = urls[len(urls) - 1]
                insert_post(url, int(likes), int(comments), urls_post[:-1])

            # Перейдите к следующему id
            current_id = current_id + 1
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
    test_url = 'https://dzen.ru/id/652a7df17a8a8e15f847988f'
    user_post_parser_zher(test_url)