from fastapi import APIRouter
import os
import yaml

PROJECTS_ALL = []

route = APIRouter()
#--------------------------------------------------------------------
def update_projects_all():
    days_yml = os.listdir('out')
    days_yml = [i for i in days_yml if i != 'history.yml']
    days_yml.sort()
    projects_all = []
    for day_yml in days_yml:
        date = day_yml.split('.')[0]
        with open(f'out/{day_yml}') as f:
            projects_day = yaml.safe_load(f)
            for project_key in projects_day.keys():
                project = projects_day[project_key]
                if project['link'] not in [item['link'] for item in projects_all]:
                    projects_all.append(project)
                    projects_all[-1]['date'] = date
                    projects_all[-1]['dates_file'] = [date]
                    projects_all[-1]['dates_history'] = []
                else:
                    projects_all_key = [projects_all.index(i) for i in projects_all if i['link'] == project['link']][0]
                    projects_all[projects_all_key]['date'] = date
                    projects_all[projects_all_key]['dates_file'].append(date)
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
