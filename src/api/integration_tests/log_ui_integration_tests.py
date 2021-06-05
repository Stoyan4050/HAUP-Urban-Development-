"""
log_ui_integration_tests.py
"""

from selenium import webdriver
from selenium.webdriver.support.select import By
# from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait as Wait
# from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
# from cssselect import GenericTranslator
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import os


def browser():
    """
        function to open Chrome with driver
    """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    chrome_options.add_argument("window-position=500,0")
    chrome_options.add_argument("window-size=793,1167")

    # create a new Chrome session
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def load_page(driver, page):
    """
        load page. Takes in Chrome driver and page to open in Chrome.
    """

    driver.get(page)


chrome = browser()
load_page(chrome, 'http://127.0.0.1:8000/urban_development/login/')


def selection(selector, n=0):
    """
        selection to select elements. Takes in css tag selector, and optionally the number of the
        selector in case of multiple selectors.
    """

    return Wait(chrome, 5000).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))[n]


email = selection('#id_username')
email.send_keys('hauptest@hauptest.com')
password = selection('#id_password')
password.send_keys('!helloT12345')
map_button = selection('button')
map_button.click()

url_map = chrome.current_url
if url_map == 'http://127.0.0.1:8000/urban_development/map/':
    print('Correct page')
else:
    print('Incorrect page')

user_name = selection('#user-name').text
if user_name == 'Hello, hauptest@hauptest.com':
    print('Correct user')
else:
    print('Incorrect user')

logout_button = selection('#logout-button')
logout_button.click()

url_after_logout = chrome.current_url
if url_after_logout == 'http://127.0.0.1:8000/urban_development/login/':
    print('Correct page')
else:
    print('Incorrect page')

change_password = selection('a', 0)
change_password.click()

url_change_password = chrome.current_url
if url_change_password == 'http://127.0.0.1:8000/urban_development/change_password/':
    print('Correct page')
else:
    print('Incorrect page')

change_pwd_email = selection('#id_email')
change_pwd_email.send_keys('hauptest2@hauptest.com')
change_pwd_button = selection('button')
change_pwd_button.click()

resend_password = selection('a', 0)
resend_password.click()

url_resend_password = chrome.current_url
if 'http://127.0.0.1:8000/urban_development/send_change_password_email/' in url_resend_password:
    print('Correct page')
else:
    print('Incorrect page')

login_after_change_password = selection('a', 1)
login_after_change_password.click()

url_after_change_pwd = chrome.current_url
if url_after_change_pwd == 'http://127.0.0.1:8000/urban_development/login/':
    print('Correct page')
else:
    print('Incorrect page')

register_user = selection('a', 1)
register_user.click()

url_register_user = chrome.current_url
if url_register_user == 'http://127.0.0.1:8000/urban_development/register/':
    print('Correct page')
else:
    print('Incorrect page')

return_to_login = selection('a', 0)
return_to_login.click()

url_login_after_register = chrome.current_url
if url_login_after_register == 'http://127.0.0.1:8000/urban_development/login/':
    print('Correct page')
else:
    print('Incorrect page')

login_guest = selection('a', 2)
login_guest.click()

url_map_guest = chrome.current_url
if url_map_guest == 'http://127.0.0.1:8000/urban_development/map/':
    print('Correct page')
else:
    print('Incorrect page')

guest_name = selection('#user-name').text
if guest_name == 'Hello, guest':
    print('Correct user')
else:
    print('Incorrect user')

# Check map and data view
map_view_button = selection('button', 0)
data_view_button = selection('button', 1)
if not map_view_button.is_enabled():
    print('Button enabling correct')
else:
    print('Button enabling incorrect')
if data_view_button.is_enabled():
    print('Button enabling correct')
else:
    print('Button enabling incorrect')

data_view_button.click()
if map_view_button.is_enabled():
    print('Button enabling correct')
else:
    print('Button enabling incorrect')
if not data_view_button.is_enabled():
    print('Button enabling correct')
else:
    print('Button enabling incorrect')
