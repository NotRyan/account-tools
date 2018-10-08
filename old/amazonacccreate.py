import mechanicalsoup
import requests
import shutil
import re

SIGN_UP_URL = "https://www.amazon.com/ap/register?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dnav_newcust"
SIGN_UP_URL_2 = "https://www.amazon.com/ap/register?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_ya_signin&prevRID=WCT7H5EZTR8W5NNXBTA8&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&prepopulatedLoginId=&failedSignInCount=0&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=usflex&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"


captcha_regex = 'https.*(?=" data-refresh)'

name = ''
email = ''
password = ''

browser = mechanicalsoup.StatefulBrowser()
browser.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36")
browser.open(SIGN_UP_URL_2)


#print(browser.get_current_page().text.encode("utf-8"))
signuppage = browser.get_current_page().text#.encode("utf-8")
#f = open("amznpage.html", "a")
#f.write(signuppage)

#print(signuppage.encode("utf-8"))

match = re.search(captcha_regex, signuppage)
if match:
    print(match.group(0))
else:
    print("No captcha found")
browser.select_form('#ap_register_form')
browser["customerName"] = name
browser["email"] = email
browser["password"] = password
browser["passwordCheck"] = password
page = browser.submit_selected()

signuppage = browser.get_current_page().text
#print(signuppage.encode("utf-8"))

match = re.search(captcha_regex, signuppage)
if match:
    print(match.group(0))
else:
    print("No captcha found")
#print(page.text.encode("utf-8"))
