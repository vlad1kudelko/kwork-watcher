from fastapi import APIRouter
import datetime
import os
import re
import yaml

PROJECTS_ALL = []

route = APIRouter()

keywords_black_list = ','.join([
    'на,для,по,нужно,не,есть,или,что,от,за,https,будет,как,из,если,чтобы,через,все,необходимо,мы',
]).split(',')

#--------------------------------------------------------------------
def rm_txt(txt):
    if txt:
        if ': ' in txt:
            return txt.split(': ')[1]
    return txt
#--------------------------------------------------------------------
def test_date(inp_date):
    inp_date = inp_date[:10]
    now = datetime.datetime.now()
    inp = datetime.datetime.strptime(inp_date, '%Y-%m-%d')
    delta = now - inp
    return delta.days
#--------------------------------------------------------------------
def update_projects_all():
    days_yml = os.listdir('out')
    days_yml = [i for i in days_yml if i != 'history.yml']
    days_yml.sort()
    projects_all = []
    with open('out/history.yml') as f:
        history_all = yaml.safe_load(f)
    for day_yml in days_yml:
        date = day_yml.split('.')[0]
        with open(f'out/{day_yml}') as f:
            projects_day = yaml.safe_load(f)
            for project_key in projects_day.keys():
                project = projects_day[project_key]
                project['price_main'] = rm_txt(project['price_main'])
                project['price_sub']  = rm_txt(project['price_sub'])
                if project['link'] not in [item['link'] for item in projects_all]:
                    projects_all.append(project)
                    projects_all[-1]['date'] = history_all[project['link']].split('+')[0] if project['link'] in history_all else date
                    projects_all[-1]['dates_file'] = [date]
                else:
                    projects_all_key = [projects_all.index(i) for i in projects_all if i['link'] == project['link']][0]
                    projects_all[projects_all_key]['date'] = date
                    projects_all[projects_all_key]['dates_file'].append(date)
    projects_all = list(filter(lambda x: test_date(x['date']) <= 2, projects_all))
    return projects_all
#--------------------------------------------------------------------
@route.get('/update')
async def update():
    global PROJECTS_ALL
    PROJECTS_ALL = update_projects_all()
    return PROJECTS_ALL
#--------------------------------------------------------------------
@route.get('/all')
async def all():
    return PROJECTS_ALL
#--------------------------------------------------------------------
@route.get('/keywords')
def keywords():
    days_yml = os.listdir('out')
    days_yml = [i for i in days_yml if i != 'history.yml']
    days_yml.sort()
    keywords_all = {}
    # цикл по дням
    for day_yml in days_yml:
        with open(f'out/{day_yml}') as f:
            projects_day = yaml.safe_load(f)
            # цикл по проектам
            for key_project, item_project in projects_day.items():
                # цикл по словам
                for item_word in re.split(r'[.,!?;:()/\s]+', item_project['text']):
                    if len(item_word) < 2:
                        continue
                    if item_word in keywords_black_list:
                        continue
                    item_word = item_word.lower()
                    if item_word not in keywords_all:
                        keywords_all[item_word] = 0
                    keywords_all[item_word] += 1
    word_index_arr = []
    for item_word in keywords_all.keys():
        if keywords_all[item_word] < 5:
            continue
        word_index_arr.append([ item_word, keywords_all[item_word] ])
    return list(reversed(
        sorted(word_index_arr, key=lambda x: x[1])
    ))
#--------------------------------------------------------------------

PROJECTS_ALL = update_projects_all()
