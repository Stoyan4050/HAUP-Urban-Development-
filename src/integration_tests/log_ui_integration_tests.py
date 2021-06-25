"""
log_ui_integration_tests.py
"""

from selenium import webdriver
from selenium.webdriver.support.select import By
from selenium.webdriver.support.wait import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC


def browser():
    """
    Function to open Chrome with driver.
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
    Load page. Takes in Chrome driver and page to open in Chrome.
    """

    driver.get(page)


CHROME = browser()
load_page(CHROME, 'http://127.0.0.1:8000/urban_development/login/')


def selection(selector, number=0):
    """
    Selection to select elements. Takes in css tag selector and, optionally,
    the number of the selector in case of multiple selectors.
    """

    return Wait(CHROME, 5000).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))[number]


EMAIL = selection('#id_username')
EMAIL.send_keys('hauptest@hauptest.com')

PASSWORD = selection('#id_password')
PASSWORD.send_keys('!helloT12345')

MAP_BUTTON = selection('button')
MAP_BUTTON.click()

URL_MAP = CHROME.current_url
if URL_MAP == 'http://127.0.0.1:8000/urban_development/main/':
    print('Correct page')
else:
    print('Incorrect page')

USER_NAME = selection('#user-name').text
if USER_NAME == 'Hello, hauptest@hauptest.com':
    print('Correct user')
else:
    print('Incorrect user')

LOGOUT_BUTTON = selection('#logout-button')
LOGOUT_BUTTON.click()

URL_AFTER_LOGOUT = CHROME.current_url
if URL_AFTER_LOGOUT == 'http://127.0.0.1:8000/urban_development/login/':
    print('Correct page')
else:
    print('Incorrect page')

CHANGE_PASSWORD = selection('a', 0)
CHANGE_PASSWORD.click()

URL_CHANGE_PASSWORD = CHROME.current_url
if URL_CHANGE_PASSWORD == 'http://127.0.0.1:8000/urban_development/change_password/':
    print('Correct page')
else:
    print('Incorrect page')

CHANGE_PASSWORD_EMAIL = selection('#id_email')
CHANGE_PASSWORD_EMAIL.send_keys('hauptest2@hauptest.com')

CHANGE_PASSWORD_BUTTON = selection('button')
CHANGE_PASSWORD_BUTTON.click()

RESEND_CHANGE_PASSWORD_EMAIL = selection('a', 0)
RESEND_CHANGE_PASSWORD_EMAIL.click()

URL_RESEND_CHANGE_PASSWORD_EMAIL = CHROME.current_url
if 'http://127.0.0.1:8000/urban_development/send_change_password_email/' in URL_RESEND_CHANGE_PASSWORD_EMAIL:
    print('Correct page')
else:
    print('Incorrect page')

LOGIN_AFTER_CHANGE_PASSWORD = selection('a', 1)
LOGIN_AFTER_CHANGE_PASSWORD.click()

URL_AFTER_CHANGE_PASSWORD = CHROME.current_url
if URL_AFTER_CHANGE_PASSWORD == 'http://127.0.0.1:8000/urban_development/login/':
    print('Correct page')
else:
    print('Incorrect page')

REGISTER_USER = selection('a', 1)
REGISTER_USER.click()

URL_REGISTER_USER = CHROME.current_url
if URL_REGISTER_USER == 'http://127.0.0.1:8000/urban_development/register/':
    print('Correct page')
else:
    print('Incorrect page')

RETURN_TO_LOGIN = selection('a', 0)
RETURN_TO_LOGIN.click()

URL_LOGIN_AFTER_REGISTER = CHROME.current_url
if URL_LOGIN_AFTER_REGISTER == 'http://127.0.0.1:8000/urban_development/login/':
    print('Correct page')
else:
    print('Incorrect page')

LOGIN_GUEST = selection('a', 2)
LOGIN_GUEST.click()

URL_MAP_GUEST = CHROME.current_url
if URL_MAP_GUEST == 'http://127.0.0.1:8000/urban_development/main/':
    print('Correct page')
else:
    print('Incorrect page')

GUEST_NAME = selection('#user-name').text
if GUEST_NAME == 'Hello, guest':
    print('Correct user')
else:
    print('Incorrect user')

# Check map and data view
MAP_VIEW_BUTTON = selection('button', 0)
DATA_VIEW_BUTTON = selection('button', 1)

if not MAP_VIEW_BUTTON.is_enabled() and DATA_VIEW_BUTTON.is_enabled():
    print('Button enabling correct')
else:
    print('Button enabling incorrect')

DATA_VIEW_BUTTON.click()

if MAP_VIEW_BUTTON.is_enabled() and not DATA_VIEW_BUTTON.is_enabled():
    print('Button enabling correct')
else:
    print('Button enabling incorrect')
