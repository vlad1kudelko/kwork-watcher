from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from zoneinfo import ZoneInfo
import datetime
import os
import time
import yaml

SELENIUM_URL = os.environ['SELENIUM_URL']

# структура данных
# id_[id проекта]:
#   link:           str
#   h1:             str
#   price_main:     str
#   price_sub:      str
#   text:           str
#   payer_link:     str
#   payer_login:    str
#   payer_all:      arr(str)
#   stay:           str
#   reaction:       str

dirname = os.path.dirname(__file__)
os.system(f'mkdir -p "{dirname}/out"')

def dt():
    return datetime.datetime.now(ZoneInfo('Asia/Irkutsk')).isoformat()

def get_fullname(name=''):
    if name == '':
        filename = dt()[:10]
    else:
        filename = name
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

def test_history(test_link):
    full_path = get_fullname('history')
    history_arr = {}
    if os.path.exists(full_path):
        with open(full_path) as f:
            history_arr = yaml.safe_load(f)
    if test_link not in history_arr:
        history_arr[test_link] = dt()
        with open(full_path, 'w') as f:
            yaml.safe_dump(history_arr, f, encoding='utf-8', allow_unicode=True)
            return True
    return False

def parser_info_stay(inp_arr):
    for item in inp_arr:
        if not item.startswith('Осталось: '):
            continue
        txt = item.split('Осталось: ')[1].split('.')
        ret = { 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0 }
        for tok in txt:
            if tok.endswith(' д'):
                ret['days'] += int(tok[:-2])
            if tok.endswith(' ч'):
                ret['hours'] += int(tok[:-2])
            if tok.endswith(' мин'):
                ret['minutes'] += int(tok[:-4])
            if tok.endswith(' сек'):
                ret['seconds'] += int(tok[:-4])
        f = lambda x: str(x).rjust(2, '0')
        return f'{ret['days']} {f(ret['hours'])}:{f(ret['minutes'])}:{f(ret['seconds'])}'

def parser_info_reaction(inp_arr):
    for item in inp_arr:
        if not item.startswith('Предложений: '):
            continue
        return item.split('Предложений: ')[1]

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
            obj['text'] = ' '.join(obj['text'])
        except NoSuchElementException:
            obj['text'] = None
        # заказчик
        payer = item.find_element(By.CLASS_NAME, 'want-payer-statistic')
        payer_login = payer.find_element(By.CSS_SELECTOR, 'a.v-align-t')
        obj['payer_link'] = payer_login.get_attribute('href')
        obj['payer_login'] = payer_login.text
        obj['payer_all'] = payer.text.split('\n')
        # сроки и отклики
        informers = item.find_element(By.CLASS_NAME, 'want-card__informers-row').text.split('\n')
        obj['stay'] = parser_info_stay(informers)
        obj['reaction'] = parser_info_reaction(informers)
        # сохраняем
        ret.append(obj)
        test_history(obj['link'])
    next_page = len(driver.find_elements(By.CLASS_NAME, 'pagination__arrow--next')) > 0
    return (ret, next_page)

get_key     = lambda x: 'id_' + x['link'].split('/')[-1]
dict_to_arr = lambda d: [v for k, v in d.items()]
arr_to_dict = lambda a: {get_key(v): v for v in a}

def main():
    try:
        glob_arr = dict_to_arr( read_yml() )  # все спаршенные проекты (ниже по коду могут быть повторы)
        old_count = len(glob_arr)             # количество спаршенных проектов c прошлого раза
        print(f'start with {old_count}')
        driver = webdriver.Remote(
            command_executor=SELENIUM_URL,
            options=webdriver.FirefoxOptions())
        for i in range(1, 100):
            url = f'https://kwork.ru/projects?page={i}'
            local_arr, next_page = open_page(driver, url)  # массив со спаршенными проектами и признаком наличия следующей страницы
            glob_arr += local_arr                          # добавляем спаршенные проекты (повторы могут появиться здесь)
            new_dict = arr_to_dict(glob_arr)               # преобразуем в словарь для сохранения (тут повторы сворачиваются)
            new_count = len(new_dict.keys())               # суммарное количество проектов без повторов
            write_yml( new_dict )
            print(' '.join([
                'page:',
                str(i).rjust(2, ' '),
                '-',
                str(new_count).rjust(4, ' '),
                f'(+{new_count - old_count})',
            ]))
            old_count = new_count
            if next_page == False:
                break
        print(f'end with {old_count}')
    finally:
        driver.quit()

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            #  print(e)
            print('ERROR неожиданная ошибка')
        time.sleep(5)
