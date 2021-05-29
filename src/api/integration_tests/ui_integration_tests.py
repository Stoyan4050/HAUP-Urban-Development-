"""
ui_integration_tests.py
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
email.send_keys('testtest@test.com')
password = selection('#id_password')
password.send_keys('!helloT12345')
map_button = selection('button')
map_button.click()

url_map = chrome.current_url

if url_map == 'http://127.0.0.1:8000/urban_development/map/':
    print('Correct page')
else:
    print('Incorrect page')


logout_button = selection('#logout-button')
logout_button.click()

url_after_logout = chrome.current_url

if url_after_logout == 'http://127.0.0.1:8000/urban_development/login/':
    print('Correct page')
else:
    print('Incorrect page')

assert url_after_logout == 'http://127.0.0.1:8000/urban_development/login/'

# map_view_enabled = selection('#map_view_button')
# print(map_view_enabled.is_enabled())

# data_view_button = selection('#data_view_button')
# data_view_button.click()
