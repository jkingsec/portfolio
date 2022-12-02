import csv, json
import os, sys
import requests
import math
from time import sleep, strftime # use datetime instead
from datetime import datetime, timedelta
from random import randint, choice

# parameterize strings
# sys args, verbose flag

#  Auth dictionary
auth_dict = {
    'admin': 'admin_auth.txt',
    'jking': 'jking_auth.txt',
    'test': 'test_auth.txt'
}


#  Functions
def info():
    print('Gophish API script v0.1')


#  Initialize folders
def folders_init():
    print('Checking folders...')
    if not os.path.exists('auth'):
        os.makedirs('auth')
    if not os.path.exists('backups'):
        os.makedirs('backups')
    if not os.path.exists('sets'):
        os.makedirs('sets')


#  Make new set folders
def new_set(set_name):
    example_json = {
        'name': set_name,
        'date': strftime("%Y%m%d-%H%M%S"),
        'generic': {
            'category': {
                'generic_example': {
                    'warning': {
                        'template': '',
                        'smtp': '',
                        'page': '',
                        'url':''
                    },
                    'level_1': {
                        'template': '',
                        'smtp': '',
                        'page': '',
                        'url':''
                    },
                    'level_2': {
                        'template': '',
                        'smtp': '',
                        'page': '',
                        'url':''
                    },
                    'level_3': {
                        'template': '',
                        'smtp': '',
                        'page': '',
                        'url':''
                    }
                }
            }
        },
        'clone': {
            'category': {
                'clone_example': {
                    'warning': {
                        'template': '',
                        'smtp': '',
                        'page': '',
                        'url':''
                    },
                    'level_1': {
                        'template': '',
                        'smtp': '',
                        'page': '',
                        'url':''
                    },
                    'level_2': {
                        'template': '',
                        'smtp': '',
                        'page': '',
                        'url':''
                    },
                    'level_3': {
                        'template': '',
                        'smtp': '',
                        'page': '',
                        'url':''
                    }
                }
            }
        }
    }
    print('Creating '+set_name+'...')
    set_path = 'sets/'+set_name
    if not os.path.exists(set_path):
        os.makedirs(set_path)
        os.makedirs(set_path+'/templates')
        os.makedirs(set_path+'/pages')
        os.makedirs(set_path+'/smtp')
        os.makedirs(set_path+'/groups')
        os.makedirs(set_path+'/groups/csv')
        os.makedirs(set_path+'/groups/json')
        with open(set_path+'/'+set_name+'.json', 'w') as set_file:
            json.dump(example_json, set_file)
            set_file.close()
    else:
        print(set_name+' already exists!') #  Exception?


#  Make new backup folders
def new_backup_folders(backup_name):
    print('Creating folders for '+backup_name+'...')
    #
    backup_path = 'backups/'+backup_name
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
        os.makedirs(backup_path+'/templates')
        os.makedirs(backup_path+'/pages')
        os.makedirs(backup_path+'/smtp')
        os.makedirs(backup_path+'/groups')
        os.makedirs(backup_path+'/groups/csv')
        os.makedirs(backup_path+'/groups/json')
        return True
    else:
        print(set_name+' already exists!')
        return False


#  Load API auth
def load_auth(user_name):
    auth_path = 'auth/'+auth_dict[user_name]
    if os.path.exists(auth_path):
        auth = [line.rstrip() for line in open(auth_path, 'r').readlines()][0]
    return auth


#  Use API w/ auth
def api_get(user_name, endpoint):
    headers = {
        'Accept': 'application/json',
        'Authorization': load_auth(user_name)
    }
    results = requests.get(
        'https://phish.example.com:3333/api/'+endpoint,
        headers=headers
    ).json()
    return results


def api_post(user_name, endpoint, body):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': load_auth(user_name)
    }
    send = requests.post(
        'https://phish.example.com:3333/api/'+endpoint,
        headers=headers,
        json=body
    )
    return send.status_code


#  Backup entire user account # campaign data
def backup(user_name):
    if user_name in auth_dict:
        backup_name = "backup_"+user_name+"_"+strftime("%Y%m%d-%H%M%S")
        print("Creating "+backup_name+" for user "+user_name+"...")
        if new_backup_folders(backup_name):
            # temps
            print('Collecting templates...')
            templates = api_get(user_name, 'templates/')
            for w in templates:
                id = str(w['id'])
                with open('backups/'+backup_name+'/templates/'+w['name']+'_'+id+'.json', 'w') as template_file:
                    json.dump(w, template_file)
                    template_file.close()
            # pages
            print('Collecting pages...')
            pages = api_get(user_name, 'pages/')
            for x in pages:
                id = str(x['id'])
                with open('backups/'+backup_name+'/pages/'+x['name']+'_'+id+'.json', 'w') as page_file:
                    json.dump(x, page_file)
                    page_file.close()
            # profiles
            print('Collecting sending profiles...')
            profiles = api_get(user_name, 'smtp/')
            for y in profiles:
                id = str(y['id'])
                with open('backups/'+backup_name+'/smtp/'+y['name']+'_'+id+'.json', 'w') as profile_file:
                    json.dump(y, profile_file)
                    profile_file.close()
            # groups
            print('Collecting groups...')
            groups = api_get(user_name, 'groups/')
            for v in groups:
                id = str(v['id'])
                with open('backups/'+backup_name+'/group/json/'+v['name']+'_'+id+'.json', 'w') as group_file:
                    json.dump(v, group_file)
                    group_file.close()
            for z in groups:
                id = str(z['id'])
                with open('backups/'+backup_name+'/groups/csv/'+z['name']+'_'+id+'.csv', 'w') as group_file:
                    group_writer = csv.writer(group_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    group_writer.writerow(['First Name', 'Last Name', 'Position', 'Email'])
                    for target in z['targets']:
                        group_writer.writerow([target['first_name'], target['last_name'], target['position'], target['email']])
                    group_file.close()
            # campaigns


#  Import set to user account
def import_set(user_name, set_name):
    print("Uploading "+set_name+" to user "+user_name+"...")
    set_path = 'sets/'+set_name
    if os.path.exists(set_path):
        #temps
        print('Uploading templates...')
        for x in os.listdir(set_path+'/templates/'):
            template_path = set_path+'/templates/'+x
            template = json.load(open(template_path, 'r'))
            api_post(user_name, 'templates/', template)
        #pages
        print('Uploading pages...')
        for y in os.listdir(set_path+'/pages/'):
            page_path = set_path+'/pages/'+y
            page = json.load(open(page_path, 'r'))
            api_post(user_name, 'pages/', page)
        #profiles
        print('Uploading sending profiles...')
        for z in os.listdir(set_path+'/smtp/'):
            profile_path = set_path+'/smtp/'+z
            profile = json.load(open(profile_path, 'r'))
            api_post(user_name, 'smtp/', profile)
    else:
        print(set_name+" doesn't exist!")


#  Create a meta campaign for a user using a set json
def meta_campaign(user_name, set_name, group_name, total_weeks, start_date):
    #  Default rate: 1 email per week
    #  Or: 1 warning + 1 phish per week?
    type_weight = 55
    level_weights_list = [
        {'warning':50,'level_1':25,'level_2':25,'level_3':0},
        {'warning':25,'level_1':25,'level_2':50,'level_3':0},
        {'warning':25,'level_1':25,'level_2':25,'level_3':25},
        {'warning':25,'level_1':0,'level_2':50,'level_3':25}
        ] # redo
    set_json_path = 'sets/'+set_name+'/'+set_name+'.json'
    quarter_point = total_weeks // 4
    quarter_marks = [0, quarter_point, quarter_point*2, quarter_point*3]
    #date = YYYY-MM-DD
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    except datetime.exceptions.ValueError:
        print('Error in date format (YYYY-MM-DD)')
    #date_list = [(start_date, start_date + week),...] # date_list[n]
    date_list = [(start_date + timedelta(hours=9), start_date + timedelta(days=4, hours=17))]
    for x in range(1, total_weeks):
        date_list.append((date_list[x-1][0] + timedelta(days=7), date_list[x-1][1] + timedelta(days=7)))

    if os.path.exists(set_json_path):
        print('Creating meta campaign for '+group_name+' ('+user_name+') using '+set_name+' set...') # warning that it works best with fresh user
        set_json = json.load(open(set_json_path, 'r'))
        #  here's the blah part
        for n in range(0,total_weeks):
            if randint(0,100) <= type_weight:
                type = 'generic'
            else:
                type = 'clone'
            category = choice(list(set_json[type])) #
            name = choice(list(set_json[type][category]))
            # picking the level is tricky
            if n in range(quarter_marks[0],quarter_marks[1]):
                level_weights = level_weights_list[0]
            elif n in range(quarter_marks[1],quarter_marks[2]):
                level_weights = level_weights_list[1]
            elif n in range(quarter_marks[2],quarter_marks[3]):
                level_weights = level_weights_list[2]
            elif n >= quarter_marks[3]:
                level_weights = level_weights_list[3]
            # more blah
            temp_list = []
            for x in level_weights: # need to redo level weights
                i = 0
                while i in range(0,level_weights[x]):
                    temp_list.append(x)
                    i += 1
                    # increment level weights here
            level = choice(temp_list)
            camp_name = "["+type+"]["+category+"]["+level+"]"+" "+str(n)
            # put it all together for the api call
            api_body = {
                "name": camp_name,
                "launch_date": date_list[n][0].isoformat()+'Z',
                "send_by_date": date_list[n][1].isoformat()+'Z',
                "template": {"name": set_json[type][category][name][level]["template"]},
                "page": {"name": set_json[type][category][name][level]["page"]},
                "groups": [{"name": group_name}],
                "smtp": {"name": set_json[type][category][name][level]["smtp"]},
                "url": set_json[type][category][name][level]["url"]
            }
            print(api_body)
            api_post(user_name, 'campaigns/', api_body)
    else:
        print('Set JSON file not found!')


info()
folders_init()
