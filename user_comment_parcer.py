from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ordered_set import OrderedSet
from bs4 import BeautifulSoup


def highlight(driver, element):
    """Highlights (blinks) a Selenium Webdriver element"""

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)

    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 2px solid red;")
    time.sleep(.3)
    apply_style(original_style)


def is_element_exist_by_id(driver, id):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, id)))
    except TimeoutException:
        return False


def is_element_exist_by(driver, by, id):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((by, id)))
    except TimeoutException:
        return False


def post_comment_parser_test(url):
    # Создание дравера с опциями (чтобы не спамил ошибками)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    # Открываем веб-сайт
    driver.get(url)
    time.sleep(5)

    elements_classes = driver.find_elements(By.CSS_SELECTOR, "[class]")

    comm_pattern = r"comment__commentContent-.*"
    elements_comms = OrderedSet(
        [element for element in elements_classes if re.search(comm_pattern, element.get_attribute("class"))])

    Bad_counter = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        new_elements_classes = driver.find_elements(By.CSS_SELECTOR, "[class]")
        try:
            new_elements_comms = OrderedSet([element for element in new_elements_classes if
                                             re.search(comm_pattern, element.get_attribute("class"))])
            new_elements_comms |= elements_comms
            # more_comment_str = "коммент"
            if len(elements_comms) == len(new_elements_comms):
                Bad_counter += 1
                # button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//div[@class="more-comments-button__block-3z more-comments-button__text-1C"]')))
                # print(button.text)
                # driver.execute_script("arguments[0].style.transform='scale(1)';", driver.find_element(By.TAG_NAME,"body"))
                # highlight(driver, button)
                # driver.execute_script("arguments[0].click();", button)
            # else:
            #    Bad_counter = 0
            elements_comms |= new_elements_comms
        except:
            Bad_counter += 1
        if (Bad_counter >= 3):
            break

    for el in elements_comms:
        el_soup = BeautifulSoup(el.get_attribute('innerHTML'), 'html.parser')

        link_pattern = re.compile(r"Link Link_theme_normal Link_view_default comment-header__nameLink.*")
        links = el_soup.find_all(class_=link_pattern)
        if links is not None:
            for link in links:
                user_url_part = 'https://dzen.ru'+link.get("href")
                print(user_url_part)

        content_pattern = re.compile(r"ui-lib-rich-text__text _color_primary.*")
        content_txt = el_soup.find_all(class_=content_pattern)
        if content_txt is not None:
            for cont in content_txt:
                content=cont.get_text()
                content=content.replace('<span class="ui-lib-rich-text__text _color_primary">','')
                content = content.replace('</span>', '')
                print(content)

        content_pattern = re.compile(r"ui-lib-rich-text__text _color_primary.*")
        content_txt = el_soup.find_all(class_=content_pattern)
        if content_txt is not None:
            for cont in content_txt:
                content = cont.get_text()
                content = content.replace('<span class="ui-lib-rich-text__text _color_primary">', '')
                content = content.replace('</span>', '')
                print(content)
    driver.quit()


if __name__ == '__main__':
    test_url = 'https://dzen.ru/b/ZTP3gQJ23RI2zQz-?referrer_clid=1400&'
    post_comment_parser_test(test_url)
