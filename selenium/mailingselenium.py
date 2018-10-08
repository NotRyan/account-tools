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


    elem = driver.find_element_by_id("id_localpart")
    print("class: " + elem.get_attribute("class"))
    print("displayed: " + str(elem.is_displayed()))
    print("enabled: " + str(elem.is_enabled()))
    print("selected: " + str(elem.is_selected()))

    elem = driver.find_element_by_xpath(".//button[@value='Create List Dialog']")
    elem.click()
    driver.switch_to_active_element()
    #print(elem)
    #print(elem.get_attribute("class"))

    #driver.switch_to_alert()
    #driver.switch_to_frame(driver.find_element_by_id('add_list_dialog'))
    #elem = driver.find_element_by_name("localpart")
    #elem = driver.find_element_by_class_name("mdl-textfield__input requiredfield")
    list_dialog = driver.find_element_by_id('add_list_dialog')
    #elem = list_dialog.find_element_by_id("id_localpart")
    elem_list = driver.find_elements_by_id("id_localpart")
    print(elem_list)

    elem = driver.find_element_by_id("id_localpart")
    print("class: " + elem_list[0].get_attribute("class"))
    print("displayed: " + str(elem.is_displayed()))
    print("enabled: " + str(elem.is_enabled()))
    print("selected: " + str(elem.is_selected()))
    elem.send_keys("aaaaaaaaaaa")



    #email_name = getRandomString(16)
    #print(email_name)
    #elem.send_keys(email_name)
