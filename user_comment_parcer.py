import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from ordered_set import OrderedSet
from bs4 import BeautifulSoup

from user_parser import user_parser
from sql_table import insert_comments

from utils import number_to_changes

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

    bad_counter = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        new_elements_classes = driver.find_elements(By.CSS_SELECTOR, "[class]")
        try:
            new_elements_comms = OrderedSet([element for element in new_elements_classes if
                                             re.search(comm_pattern, element.get_attribute("class"))])
            new_elements_comms |= elements_comms
            if len(elements_comms) == len(new_elements_comms):
                bad_counter += 1
            elements_comms |= new_elements_comms
        except NoSuchElementException:
            break            
        except:
            bad_counter += 1
        if (bad_counter >= 3):
            break

    for el in elements_comms:
        el_soup = BeautifulSoup(el.get_attribute('innerHTML'), 'html.parser')

        link_pattern = re.compile(r"Link Link_theme_normal Link_view_default comment-header__nameLink.*")
        links = el_soup.find_all(class_=link_pattern)
        user_url_part=''
        if links is not None:
            for link in links:
                user_url_part = f'https://dzen.ru{link.get("href")}'
                user_parser(user_url_part)

        content_pattern = re.compile(r"ui-lib-rich-text__text _color_primary.*")
        content_txt = el_soup.find_all(class_=content_pattern)
        content=''
        if content_txt is not None:
            for cont in content_txt:
                content=cont.get_text()
                content=content.replace('<span class="ui-lib-rich-text__text _color_primary">','')
                content = content.replace('</span>', '')

        likes_pattern = re.compile(r"Text Text_typography_text-14-18 comment-footer__feedbackCount-2E.*")
        likes_txt = el_soup.find_all(class_=likes_pattern)
        like_n=''
        if likes_txt is not None:
            for likes in likes_txt:
                like_n=likes.get_text()
                like_n=like_n.replace('<div class="Text Text_typography_text-14-18 comment-footer__feedbackCount-2E" title="Количество лайков">','')
                like_n = like_n.replace('<div class="Text Text_typography_text-14-18 comment-footer__feedbackCount-2E comment-footer__empty-3u" title="Количество лайков">','')
                like_n = like_n.replace('</div>','')
        insert_comments(url, user_url_part, content, number_to_changes(like_n))
    driver.quit()

if __name__ == '__main__':
    test_url = 'https://dzen.ru/b/ZTP3gQJ23RI2zQz-?from=channel&amp'
    post_comment_parser_test(test_url)
