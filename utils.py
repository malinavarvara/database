import re

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def is_element_exist_by(driver, by, pattern):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((by, pattern)))
    except TimeoutException:
        return False

def number_to_changes(num_str):
    num_str=num_str.replace(',', '.')
    if num_str == '':
        return 0
    if 'K' in num_str: num = float(num_str[:-1])*1000
    elif 'M' in num_str: num = float(num_str[:-1]) * 1000000
    else: num = int(num_str)
    return num
    
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