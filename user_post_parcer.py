from selenium import webdriver
from selenium.webdriver.common.by import By

import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Post:
    def __init__(self, user_name, age, txt):
        self.age = age
        self.user_name = user_name
        self.txt=txt

    def get_data(self):
        print(self.user_name+'\n'+self.txt+'\n'+self.age+'\n')

def is_element_exist_by_id(driver,id):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, id)))
    except TimeoutException:
        return False

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
            
            # Обработка  
            # !!! Здесь нужно добавить обработку
            element_text = element.text
            words = element_text.split('\n')
            text_post=''
            for i in range(len(words)):
                if i>1 and i<(len(words)-1):
                    text_post=text_post+words[i]+'\n'
            post1 = Post(words[0],words[len(words)-1],text_post)
            post1.get_data()

            # Перейдите к следующему id
            current_id = 'zen-row-' + str(int(current_id.split('-')[2]) + 1)
            
            scroll_count = 0
            while is_element_exist_by_id(driver,current_id)==False and scroll_count<3:
                scroll_count+=1
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
            if is_element_exist_by_id(driver,current_id)==False: 
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
    user_post_parser(test_url)