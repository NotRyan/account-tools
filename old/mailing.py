#DO NOT POST THIS FILE ONLINE - SENSITIVE DATA
import requests
import lxml
from lxml import html
import json
import random, string
import argparse
from datetime import datetime
import pymysql
import configparser

def getRandomString(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

parser = argparse.ArgumentParser(description = 'Create a number of email addresses and store in database')
parser.add_argument("N", help = "number of accounts to create", type = int)
args = parser.parse_args()

config = configparser.ConfigParser()
config.read('config.ini')
print(config.sections())

LOGIN_URL = 'https://calmail.berkeley.edu/my/lists/index'
CALMAIL_AUTH_URL = 'https://auth.berkeley.edu/cas/login?renew=true&service=https%3A%2F%2Fcalmail.berkeley.edu%2Flogin%3Fnext%3D%252Fmy%252Flists%252Findex'
CALMAIL_LIST_URL = 'https://calmail.berkeley.edu/my/lists/create_group'
#why is the json so weird? No idea, but this is the only way I could get the site to accept it
# Fill in your details here to be posted to the login form.
payload = {
    '_eventId': 'submit',
    'geolocation': '',
    'submit': 'Sign In'
}
payload['username'] = config['berkeley-login']['user']
payload['password'] = config['berkeley-login']['password']


connection = pymysql.connect(host=config['sql']['host'],
                             user=config['sql']['user'],
                             password=config['sql']['password'],
                             db=config['sql']['db'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

for i in range(args.N):
    email_name = getRandomString(16)
    s = requests.session()
    login = s.get(CALMAIL_AUTH_URL, headers = {'DNT':'1','Referer': CALMAIL_AUTH_URL},verify = False)
    tree = html.fromstring(login.text)
    payload['execution'] = tree.find(".//input[@name='execution']").get('value')

    s.post(CALMAIL_AUTH_URL, data = payload, cookies = s.cookies, verify = False)

    list_headers = {
        "Referer": LOGIN_URL,
        #'X-CSRFToken': s.cookies['csrftoken'],
        'Origin': 'https://calmail.berkeley.edu'
        }

    s.get(CALMAIL_LIST_URL, cookies = s.cookies, headers = {'Referer': LOGIN_URL}, verify = False)

    group_json = json.dumps({"group_name":email_name,"group_domain":"lists.berkeley.edu","who_can_post":"ANYONE_CAN_POST"}).encode("utf-8")
    result = s.post(CALMAIL_LIST_URL, data = group_json, cookies = s.cookies, headers = list_headers, verify = False)

    if result.status_code != 200:
        break
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sql = """INSERT INTO `accounts_db`.`accounts` (`email`, `email_creation_date`) VALUES ('""" + email_name + """@lists.berkeley.edu', '""" + timestamp + """')"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()
connection.close()
