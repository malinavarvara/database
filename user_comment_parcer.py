from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def is_element_exist_by_id(driver, id):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, id)))
    except TimeoutException:
        return False


# Переписать как user_post_parser(url,func)
# Типо
# def func(element):
#    print(element.text)
def user_post_parser(url):
    # Создание дравера с опциями (чтобы не спамил ошибками)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    # Открываем веб-сайт
    driver.get(url)
    # Здесь можно заменить на int и просто приписывать "zen-row-"
    current_id = 'zen-row-0'

    while True:
        try:
            # Поиск элемента с текущим id
            element = driver.find_element(By.ID, current_id)
            text = element.get_attribute('innerHTML')
            url_pattern = r'https://[\S]+'
            urls = re.findall(url_pattern, text)
            print(urls, current_id)
            # Обработка
            # !!! Здесь нужно добавить обработку

            element_text = element.text
            print(element_text)

            # Перейдите к следующему id
            current_id = 'zen-row-' + str(int(current_id.split('-')[2]) + 1)

            scroll_count = 0
            while is_element_exist_by_id(driver, current_id) == False and scroll_count < 3:
                scroll_count += 1
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            if is_element_exist_by_id(driver, current_id) == False:
                print("Конец страницы")
                break
        except Exception as e:
            # Если элемент не был найден, завершите цикл
            print("Элемент не найден. Завершение.")
            print(type(e), e)
            break
    driver.quit()


if __name__ == '__main__':
    test_url = 'https://dzen.ru/video/watch/653433f74098ea1f27696a76?rid=2965756932.249.1697974558130.78267&amp;comment-request=1&amp;referrer_clid=1400&amp;#comments_data=p_root'
    user_post_parser(test_url)