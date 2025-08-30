from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import os
import yaml
import datetime

dirname = os.path.dirname(__file__)
os.system(f'mkdir -p "{dirname}/out"')

def get_fullname():
    filename = datetime.datetime.now().isoformat()[:10]
    full_path = f'{dirname}/out/{filename}.yml'
    return full_path

def read_yml():
    full_path = get_fullname()
    if os.path.exists(full_path):
        with open(full_path) as f:
            return yaml.safe_load(f)
    return {}

def write_yml(data):
    full_path = get_fullname()
    with open(full_path, 'w') as f:
        yaml.safe_dump(data, f, encoding='utf-8', allow_unicode=True)

def open_page(driver, url):
    ret = []
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element(By.TAG_NAME, 'h1')
    for item in driver.find_elements(By.CLASS_NAME, 'want-card'):
        obj = {}
        obj['link'] = item.find_element(By.CSS_SELECTOR, 'h1 a').get_attribute('href')
        obj['h1']   = item.find_element(By.TAG_NAME, 'h1').text
        # желаемый бюджет
        obj['price_main'] = item.find_element(By.CLASS_NAME, 'wants-card__header-right-block').text
        # допустимый бюджет
        try:
            obj['price_sub'] = item.find_element(By.CLASS_NAME, 'wants-card__description-higher-price').text
        except NoSuchElementException:
            obj['price_sub'] = None
        # основной текст проекта
        try:
            tmp_text = item.find_element(By.CLASS_NAME, 'wants-card__description-text').get_attribute('innerHTML')
            tmp_text_arr = BeautifulSoup(tmp_text, 'html.parser').get_text().split('...\xa0Показать полностью ')
            if len(tmp_text_arr) == 2:
                obj['text'] = tmp_text_arr[1].split('\xa0Скрыть ')[0].split('\n')
            else:
                obj['text'] = tmp_text_arr[0].split('\n')
        except NoSuchElementException:
            obj['text'] = None
        # заказчик
        payer = item.find_element(By.CLASS_NAME, 'want-payer-statistic')
        payer_login = payer.find_element(By.CSS_SELECTOR, 'a.v-align-t')
        obj['payer_link'] = payer_login.get_attribute('href')
        obj['payer_login'] = payer_login.text
        obj['payer_all'] = payer.text.split('\n')
        # сроки и отклики
        obj['informers'] = item.find_element(By.CLASS_NAME, 'want-card__informers-row').text.split('\n')
        # сохраняем
        ret.append(obj)
    next_page = len(driver.find_elements(By.CLASS_NAME, 'pagination__arrow--next')) > 0
    return (ret, next_page)

dict_to_arr = lambda d: [v for k, v in d.items()]
arr_to_dict = lambda a: {'id_' + v['link'].split('/')[-1]: v for v in a}

def main():
    glob_arr = dict_to_arr( read_yml() )
    print('start with ' + str(len(glob_arr)))
    driver = webdriver.Firefox()
    for i in range(1, 100):
        url = f'https://kwork.ru/projects?page={i}'
        local_arr, next_page = open_page(driver, url)
        glob_arr += local_arr
        print(f'page {i} done')
    driver.close()
    write_yml( arr_to_dict(glob_arr) )
    print('end with ' + str(len(glob_arr)))

if __name__ == '__main__':
    main()
