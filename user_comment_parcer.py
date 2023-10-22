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

def is_element_exist_by(driver,by, id):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((by, id)))
    except TimeoutException:
        return False

def parsing(prev_comment, driver):
    post = driver.find_element(By.CLASS_NAME, "card-image-compact-view__content")
    post_text = post.text

    if post_text != prev_comment:
        href = post.find_element(By.CLASS_NAME, "zen-ui-card-title-clamp")
        description = post.find_element(By.CLASS_NAME, "card-layer-snippet-view").text.strip()
        hrefUrl = href.get_attribute("href")
        href_title = href.text.strip()

        info_description = (description[:100] + '...') if len(description) > 100 else description
        return f"{href_title}\n\n{info_description}\n\n{hrefUrl}", post_text
    else:
        return None, post_text

def user_post_parser(url):
    # Создание дравера с опциями (чтобы не спамил ошибками)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    # Открываем веб-сайт
    driver.get(url)
    while True:
        try:
            scroll_count = 0
            prev_comment = None
            while is_element_exist_by(driver, current_id) == False and scroll_count < 3:
                scroll_count += 1
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            post_return = parsing(prev_comment, driver)
            prev_comment = post_return[1]

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