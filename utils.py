import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def is_element_exist_by(driver, by, id):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((by, id)))
    except TimeoutException:
        return False
    
def number_to_changes(name):
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

def links_to_changes(user_text):
    text = user_text.get_attribute('innerHTML')
    url_pattern = r'https://[\S]+'
    urls = re.findall(url_pattern, text)

    url = urls[0]
    index=0
    for i in range(len(url)):
        if url[i]=='?': index=i
    if index!=0: result_url=url[:index]
    return result_url