#!/bin/python3

from bs4 import BeautifulSoup as Bs
import csv
import os, sys
import requests, html, json
from time import sleep, strftime
from random import randint

sources = {
    "bugcrowd": "Bugcrowd",
    "hackerone": "HackerOne",
    "hackenproof": "HackenProof",
    "immunefi": "Immunefi",
    "intigriti": "Intigriti",
    "federacy": "Federacy",
    "yeswehack": "Yes We Hack"
}
if os.path.exists('ho_auth.txt'):
    ho_auth = [line.rstrip() for line in open('ho_auth.txt', 'r').readlines()]


def info():
    print(
"""______  _     _  ______ _______ _______  ______ _______  _____  _______  ______
|_____] |     | |  ____ |______ |       |_____/ |_____| |_____] |______ |_____/
|_____] |_____| |_____| ______| |_____  |    \_ |     | |       |______ |    \_
By Uboa Security
Version 1.0

Available Commands: bugcrowd, hackerone, hackenproof, immunefi, intigriti, federacy, yeswehack, all

Example: python3 bugscraper.py bugcrowd
"""
    )


def load_csv():
    if os.path.exists("./bugbounty.csv"):
        with open('bugbounty.csv', mode='r') as bugbounty_file:
            reader = csv.reader(bugbounty_file)
            data = list(reader)
            data_dict = {}
            for x in data:
                data_dict[x[0]] = x[1:]
            bugbounty_file.close()
            return data_dict
    else:
        with open('bugbounty.csv', mode='w+') as bugbounty_file:
            bugbounty_writer = csv.writer(bugbounty_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            bugbounty_writer.writerow(['Program Name', 'Handle', 'URL', 'Bounty Site', 'Paid', 'Open'])
            bugbounty_file.close()
            return {}


def check_init_paths():
    path = "./programs"
    if not os.path.exists(path):
        print("Creating Project Folder...")
        os.makedirs(path)
    else:
        pass
    print("Initialization Complete!")
    if not os.path.exists('ho_auth.txt'):
        print("WARNING: NO HACKERONE AUTH FILE DETECTED!")
    print('\n')


def create_project_folder(name, handle):
    print("Creating Folder for", name+"...")
    path = "./programs/" + handle
    if not os.path.exists(path):
        os.makedirs(path)
        open(path + "/scope.txt", "w")
        open(path + "/oos.txt", "w")
        open(path + "/scope_wildcards.txt", "w")
        open(path + "/oos_wildcards.txt", "w")
        open(path + "/apis.txt", "w")
        print("Folder for", name, "Has Been Created!")
    else:
        pass


def scrape(program_name):
    bugbounty_data = load_csv()  # format: {page_name : [url, program_name, vdp, program_open]}
    print("Starting", program_name, "Scrape...")
    print("Creating CSV Entries...")
    with open('bugbounty.csv', mode='a', newline="") as bugbounty_file:
        bugbounty_writer = csv.writer(bugbounty_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if program_name == "Bugcrowd":
            scrape_bugcrowd(bugbounty_data, bugbounty_writer)
        elif program_name == "HackerOne":
            if os.path.exists('ho_auth.txt'):
                scrape_hackerone(bugbounty_data, bugbounty_writer)
            else:
                print('No HackerOne Auth File!')
        elif program_name == "HackenProof":
            scrape_hackenproof(bugbounty_data, bugbounty_writer)
        elif program_name == "Immunefi":
            scrape_immunefi(bugbounty_data, bugbounty_writer)
        elif program_name == "Intigriti":
            scrape_intigriti(bugbounty_data, bugbounty_writer)
        elif program_name == "Federacy":
            scrape_federacy(bugbounty_data, bugbounty_writer)
        elif program_name == "Yes We Hack":
            scrape_yeswehack(bugbounty_data, bugbounty_writer)
        else:
            print("Error in Bug Bounty Name!")
        bugbounty_file.close()
    print("Starting", program_name, "Scrape Complete!")


def scrape_bugcrowd(bugbounty_data, bugbounty_writer): #switch to API
    programs = []
    n = 0
    print('Grabbing Bugcrowd Programs...')
    print('NOTE: ACQUIRING SCOPE REQUIRES SCRAPING PAGES')
    results = requests.get('https://bugcrowd.com/programs.json?offset[]='+str(n)).json()['programs']
    while results:
        for item in results: # issue with the upper bound?
            programs.append(item)
        n += 25
        print('Total Programs Grabbed:', str(n))
        results = requests.get('https://bugcrowd.com/programs.json?offset[]=' + str(n)).json()['programs']

    for item in programs:
        if item['ongoing?'] is True and item['participation'] == 'public' and item['name'] not in bugbounty_data:
            name = item['name']
            handle = item['program_url'][1:]
            url = 'https://bugcrowd.com'+item['program_url']
            if item['reward_range_summary'] == '' and item['reward_program_max'] == '':
                paid = False
            else:
                paid = True
            bugbounty_writer.writerow([name, handle, url, 'Bugcrowd', paid, True])
            print(name, "added!")
            bugcrowd_scope(url, name, handle)


def bugcrowd_scope(url, name, handle):
    print('Getting Scope for', name+'...')
    results = Bs(requests.get(url).content, "html.parser")
    scopes = json.loads(
        html.unescape(
            results.find_all(
                'div',
                class_="react-component react-component-researcher-target-groups"
            )[0]['data-react-props']
        )
    )
    create_project_folder(name, handle)

    print('Appending Scope to Files...')
    path = './programs/'+handle+'/'
    scopef = open(path+'scope.txt', 'a')
    oosf = open(path+'oos.txt', 'a')
    scopewf = open(path+'scope_wildcards.txt', 'a')
    ooswf = open(path+'oos_wildcards.txt', 'a')
    apisf = open(path+'apis.txt', 'a')
    for item in scopes['groups']:
        if item['name'] == 'In scope':
            for x in item['targets']:
                if '.' in x['name']:
                    if x['category'] == 'website':
                        if '*' in x['name']:
                            scopewf.write(x['name']+'\n')
                        else:
                            scopef.write(x['name']+'\n')
                        print(x['name'], ' added!')
                    elif x['category'] == 'api':
                        apisf.write(x['name']+'\n')
                        scopef.write(x['name'] + '\n')
                        print(x['name'], 'added!')
        else:
            for x in item['targets']:
                if '.' in x['name']:
                    if '*' in x['name']:
                        ooswf.write(x['name']+'\n')
                    else:
                        oosf.write(x['name']+'\n')
                    print(x['name'] + ' is Out of Scope!')
    scopef.close()
    scopewf.close()
    oosf.close()
    ooswf.close()
    apisf.close()
    print('Scope is Complete!')


def scrape_hackerone(bugbounty_data, bugbounty_writer):
    # requires API authentication
    headers = {
        'Accept': 'application/json'
    }
    programs = []
    print('Grabbing HackerOne Programs...')
    print('NOTE: ACQUIRING SCOPE REQUIRES SEPARATE API REQUESTS')
    results = requests.get(
        'https://api.hackerone.com/v1/hackers/programs?page[size]=100&page[number]=1',
        auth=(ho_auth[0], ho_auth[1]),
        headers=headers
    ).json()
    while 'next' in results['links']:
        next_link = results['links']['next']
        for item in results['data']:
            programs.append(item)
        print('Total Programs Grabbed:', str(len(programs)))
        results = requests.get(
            next_link,
            auth=(ho_auth[0], ho_auth[1]),
            headers=headers
        ).json()
    else:
        for item in results['data']:
            programs.append(item)
        print('Total Programs Grabbed:', str(len(programs)))

    for item in programs:
        if item['attributes']['submission_state'] != 'paused' and item['attributes']['name'] not in bugbounty_data:
            name = item['attributes']['name']
            handle = item['attributes']['handle']
            url = 'https://hackerone.com/'+item['attributes']['handle']
            if item['attributes']['offers_bounties'] is True:
                paid = True
            else:
                paid = False
            bugbounty_writer.writerow([name, handle, url, 'HackerOne', paid, True])
            print(name, "added!")
            hackerone_scope(name, handle)


def hackerone_scope(name, handle):
    print('Getting Scope for', name+'...')
    headers = {
        'Accept': 'application/json'
    }
    results = requests.get(
        'https://api.hackerone.com/v1/hackers/programs/'+handle,
        auth=(ho_auth[0], ho_auth[1]),
        headers=headers
    ).json()

    create_project_folder(name, handle)

    print('Appending Scope to Files...')
    path = './programs/' + handle + '/'
    scopef = open(path + 'scope.txt', 'a')
    oosf = open(path + 'oos.txt', 'a')
    scopewf = open(path + 'scope_wildcards.txt', 'a')
    ooswf = open(path + 'oos_wildcards.txt', 'a')
    apisf = open(path + 'apis.txt', 'a')
    for item in results['relationships']['structured_scopes']['data']:
        scope_url = item['attributes']['asset_identifier']
        if item['attributes']['eligible_for_submission'] is True:
            if item['attributes']['asset_type'] == 'URL':
                if '*' in scope_url:
                    scopewf.write(scope_url + '\n')
                elif 'api' in scope_url:
                    apisf.write(scope_url+ '\n')
                    scopef.write(scope_url + '\n')
                else:
                    scopef.write(scope_url + '\n')
                print(scope_url, ' added!')

        else:
            if '*' in scope_url:
                ooswf.write(scope_url + '\n')
            else:
                oosf.write(scope_url + '\n')
            print(scope_url + ' is Out of Scope!')
    scopef.close()
    scopewf.close()
    oosf.close()
    ooswf.close()
    apisf.close()
    print('Scope is Complete!')


def scrape_hackenproof(bugbounty_data, bugbounty_writer): #broken
    print('Grabbing HackenProof Programs...')
    print('NOTE: ACQUIRING SCOPE REQUIRES SCRAPING PAGES')
    print('WARNING: CHECK HACKENPROOF SCOPES CAREFULLY')
    results = Bs(
        requests.get(
            'https://hackenproof.com/programs?skills=web'
        ).content, "html.parser"
    ).find_all(
        'div',
        class_="bounty-programs-list--item flex-sm justify-between"
    )
    print('Total Programs Grabbed:', str(len(results)))
    for item in results:
        if item.find('h2').a.text.strip() not in bugbounty_data:
            name = item.find('h2').a.text.strip()
            url = 'https://hackenproof.com'+item.div.div.a['href']
            handle = url.split('/')[-1]
            bugbounty_writer.writerow([name, handle, url, 'HackenProof', True, True])
            print(name, 'added!')
            hackenproof_scope(name, url, handle)
        else:
            pass


def hackenproof_scope(name, url, handle):
    print('Getting Scope for', name+'...')
    results = requests.get(url).content
    scope = Bs(
        results,
        'html.parser'
    ).find_all('tr', class_="in-scope")
    oos = Bs(
        results,
        'html.parser'
    ).find_all('tr', class_='tr-out')

    create_project_folder(name, handle)

    print('Appending Scope to Files...')
    path = './programs/' + handle + '/'
    scopef = open(path + 'scope.txt', 'a')
    oosf = open(path + 'oos.txt', 'a')
    scopewf = open(path + 'scope_wildcards.txt', 'a')
    ooswf = open(path + 'oos_wildcards.txt', 'a')
    apisf = open(path + 'apis.txt', 'a')
    for item in scope:
        if item.p is None and '.' in item.h5.text:
            scope_url = item.h5.text
        elif item.p.a is None:
            scope_url = ''
        else:  # kinda broken around here
            scope_url = item.p.a['href'].replace('https://hackenproof.com/redirect?url=', '')
        if not any(x in scope_url for x in ["apps.apple.com", "play.google.com", "chrome.google.com"]):
            if '*' in scope_url:
                scopewf.write(scope_url + '\n')
            elif 'api' in scope_url:
                scopef.write(scope_url + '\n')
                apisf.write(scope_url + '\n')
            else:
                scopef.write(scope_url + '\n')
            print(scope_url,'added!')

    if oos:
        for item in oos:
            if '*' in item.h5.text:
                ooswf.write(item.h5.text + '\n')
            else:
                oosf.write(item.h5.text + '\n')
            print(item.h5.text, 'is Out of Scope!')

    scopef.close()
    scopewf.close()
    oosf.close()
    ooswf.close()
    apisf.close()
    print('Scope is Complete!')


def scrape_immunefi(bugbounty_data, bugbounty_writer): #broken
    print('Grabbing Immunefi Programs...')
    print('NOTE: IGNORING SMART CONTRACTS!')
    print('WARNING: NO OUT-OF-SCOPE OR WILDCARDS!')
    programs = json.loads(Bs(
        requests.get(
            'https://immunefi.com/explore/'
        ).content, "html.parser"
    ).find('script', id="__NEXT_DATA__").text)['props']['pageProps']['bounties']
    print('Total Programs Grabbed:', str(len([x for x in programs if not x['is_external']])))

    for item in programs:
        if not item['is_external'] and item['id'] not in bugbounty_data:
            if 'Web' in item['technologies']:
                name = item['project']
                handle = item['id']
                url = 'https://immunefi.com/bounty/'+handle+'/'

                bugbounty_writer.writerow([name, handle, url, 'Immunefi', True, True])
                print(name, "added!")
                immunefi_scope(item, name, handle)


def immunefi_scope(item, name, handle):
    print('Getting Scope for', name+'...')
    create_project_folder(name, handle)

    print('Appending Scope to Files...')
    path = './programs/' + handle + '/'
    scopef = open(path + 'scope.txt', 'a')
    apisf = open(path + 'apis.txt', 'a')
    if 'assets_in_scope' in item:
        for target in item['assets_in_scope']:
            if 'Web' in target['type']:
                scopef.write(target['target'] + '\n')
                print(target['target'], ' added!')

            elif 'API' in target['type']:
                scopef.write(target['target'] + '\n')
                apisf.write(target['target'] + '\n')
                print(target['target'], ' added!')

    else:
        print('No available scope for '+name+'!')


def scrape_intigriti(bugbounty_data, bugbounty_writer):
    print('Grabbing Integriti Programs...')
    print('NOTE: ACQUIRING SCOPE REQUIRES SEPARATE API REQUESTS')
    print('WARNING: INTEGRITI SCOPES PRONE TO FORMATTING ERRORS')
    print('WARNING: CANNOT RELIABLY GET OUT-OF-SCOPE FOR INTIGRITI')
    results = requests.get('https://api.intigriti.com/core/program').json()
    print('Total Programs Grabbed:', str(len(results)))
    for item in results:
        if item['confidentialityLevel'] != 2 and item['name'] not in bugbounty_data:
            name = item['name']
            handle = item['handle']
            prog_id = item['programId']
            url = 'https://app.intigriti.com/programs/'+item['companyHandle']+'/'+item['handle']+'/detail'
            if item['minBounty'] == 0 and item['maxBounty'] == 0:
                paid = False
            else:
                paid = True
            bugbounty_writer.writerow([name, handle, url, 'Intigriti', paid, True])
            print(name, 'added!')
            intigriti_scope(name, prog_id, handle)
        else:
            pass


def intigriti_scope(name, prog_id, handle):
    print('Getting Scope for', name+'...')

    api_url = 'https://api.intigriti.com/core/program/'+prog_id
    results = requests.get(api_url).json()
    scope = set()
    for z in results:
        if 'domains' in z:
            for x in results['domains']:
                for y in x['content']:
                    scope.add(y['endpoint'])

    create_project_folder(name, handle)

    print('Appending Scope to Files...')
    path = './programs/' + handle + '/'
    scopef = open(path + 'scope.txt', 'a')
    scopewf = open(path + 'scope_wildcards.txt', 'a')
    apisf = open(path + 'apis.txt', 'a')
    for x in scope:
        if '.' in x:
            if '*' in x:
                scopewf.write(x + '\n')
            elif 'api' in x:
                scopef.write(x + '\n')
                apisf.write(x + '\n')
            else:
                scopef.write(x + '\n')
            print(x, ' added!')
    scopef.close()
    scopewf.close()
    apisf.close()
    print('Scope is Complete!')


def scrape_federacy(bugbounty_data, bugbounty_writer):
    print('Grabbing Federacy Programs...')
    print('NOTE: ACQUIRING SCOPE REQUIRES SEPARATE API REQUESTS')
    results = requests.get('https://www.federacy.com/api/public_programs').json()
    print('Total Programs Grabbed:', str(len(results)))
    for item in results:
        if item['public'] is True and item['program_name'] not in bugbounty_data:
            name = item['program_name']
            handle = item['slug']
            prog_id = item['id']
            url = "https://federacy.com/" + item['slug'] + '?tab=Scopes'
            if item['offers_awards'] is True:
                paid = True
            else:
                paid = False
            bugbounty_writer.writerow([name, handle, url, 'Federacy', paid, True])
            print(name, "added!")
            federacy_scope(name, handle, prog_id)
        else:
            pass


def federacy_scope(name, handle, prog_id):
    print('Getting Scope for', name+'...')
    results = requests.get(
        'https://www.federacy.com/api/public_programs/'+prog_id+'/program_scopes'
    ).json()

    create_project_folder(name, handle)

    print('Appending Scope to Files...')
    path = './programs/' + handle + '/'
    scopef = open(path + 'scope.txt', 'a')
    oosf = open(path + 'oos.txt', 'a')
    scopewf = open(path + 'scope_wildcards.txt', 'a')
    ooswf = open(path + 'oos_wildcards.txt', 'a')
    apisf = open(path + 'apis.txt', 'a')

    for item in results:
        if any(x in item['scope_type'] for x in ['website', 'api']):
            if item['in_scope']:
                if '*' in item['identifier']:
                    scopewf.write(item['identifier'] + '\n')
                elif item['scope_type'] == 'api':
                    scopef.write(item['identifier'] + '\n')
                    apisf.write(item['identifier'] + '\n')
                else:
                    scopef.write(item['identifier'] + '\n')
                print(item['identifier'], 'added!')
            else:
                if '*' in item['identifier']:
                    ooswf.write(item['identifier'] + '\n')
                else:
                    oosf.write(item['identifier'] + '\n')
                print(item['identifier'], 'is Out of Scope!')

    scopef.close()
    scopewf.close()
    oosf.close()
    ooswf.close()
    apisf.close()
    print('Scope is Complete!')


def scrape_yeswehack(bugbounty_data, bugbounty_writer):
    programs = []
    n = 1
    print('Grabbing Yes We Hack Programs...')
    print('NOTE: ACQUIRING SCOPE REQUIRES SCRAPING PAGES')
    print('WARNING: OUT-OF-SCOPE PRONE TO FORMATTING ERRORS')
    results = requests.get('https://api.yeswehack.com/programs?page=' + str(n)).json()['items']
    while results:
        for item in results:
            programs.append(item)
        n += 1
        print('Total Programs Grabbed:', str(len(results)))
        results = requests.get('https://api.yeswehack.com/programs?page=' + str(n)).json()['items']

    for item in programs:
        if item['disabled'] is False and item['public'] is True and item['title'] not in bugbounty_data:
            name = item['title']
            handle = item['slug']
            url = 'https://yeswehack.com/programs/'+item['slug']
            if item['bounty'] is True:
                paid = True
            else:
                paid = False
            bugbounty_writer.writerow([name, handle, url, 'Yes We Hack', paid, True])
            print(name, "added!")
            yeswehack_scope(name, handle)
        else:
            pass


def yeswehack_scope(name, handle):
    print('Getting Scope for', name + '...')
    results = requests.get(
        'https://api.yeswehack.com/programs/' + handle
    ).json()
    scope = results['scopes']
    oos = results['out_of_scope']

    create_project_folder(name, handle)

    print('Appending Scope to Files...')
    path = './programs/' + handle + '/'
    scopef = open(path + 'scope.txt', 'a')
    oosf = open(path + 'oos.txt', 'a')
    scopewf = open(path + 'scope_wildcards.txt', 'a')
    ooswf = open(path + 'oos_wildcards.txt', 'a')
    apisf = open(path + 'apis.txt', 'a')

    for item in scope:
        if '.' in item['scope'] and not any(x in item['scope'] for x in [
            "apps.apple.com", "play.google.com", "chrome.google.com"
            ]
        ):
            if '*' in item['scope']:
                scopewf.write(item['scope'] + '\n')
            else:
                if item['scope_type'] == 'web-application':
                    scopef.write(item['scope'] + '\n')
                elif item['scope_type'] == 'api':
                    scopef.write(item['scope'] + '\n')
                    apisf.write(item['scope'] + '\n')
                print(item['scope'], 'added!')

    for item in oos:
        if '.' in item:
            if '*' in item:
                ooswf.write(item + '\n')
            else:
                oosf.write(item + '\n')
            print(item + ' is Out of Scope!')

    scopef.close()
    scopewf.close()
    oosf.close()
    ooswf.close()
    apisf.close()
    print('Scope is Complete!')


def scrape_all():
    for program in sources:
        scrape(sources[program])


# Main Loop
info()
check_init_paths()
if len(sys.argv) == 1:
    print("No Arguments Given!")
elif len(sys.argv) == 2:
    if sys.argv[1] in sources:
        scrape(sources[sys.argv[1]])
    elif sys.argv[1] == "all":
        scrape_all()
    else:
        print("Argument Not Recognized! See Available Commands!")
else:
    print("Too Many Arguments Given!")
