from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import argparse
import random, string
import configparser

LOGIN_URL = 'https://calmail.berkeley.edu/my/lists/index'

def getRandomString(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

parser = argparse.ArgumentParser(description = 'Create a number of email addresses and store in database')
parser.add_argument("N", help = "number of accounts to create", type = int)
args = parser.parse_args()

config = configparser.ConfigParser()
config.read('config.ini')

driver = webdriver.Chrome()
driver.get(LOGIN_URL)
if ("Login" in driver.title):
    print('calauth')

    elem = driver.find_element_by_id('username')
    elem.send_keys(config['berkeley-login']['user'])
    elem = driver.find_element_by_id('password')
    elem.send_keys(config['berkeley-login']['password'])
    elem = driver.find_element_by_name('submit')
    elem.click()

    driver.switch_to_frame(driver.find_element_by_id('duo_iframe'))
    elem = driver.find_element_by_xpath("//*[text()[contains(., ' Send Me a Push ')]]")
    elem.click()

    try:
        elem = webdriver.support.wait.WebDriverWait(driver, 20).until(EC.title_contains('Manage'))
    finally:
        print('No authentication received within 20 seconds, exiting...')

    elem = driver.find_element_by_xpath(".//button[@value='Create List Dialog']")
    elem.click()
    elem = driver.find_element_by_name("localpart")
    email_name = getRandomString(16)
    print(email_name)
    elem.send_keys(email_name)
