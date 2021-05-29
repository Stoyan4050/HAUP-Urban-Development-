from selenium import webdriver
from selenium.webdriver.support.select import Select, By
from selenium.webdriver.support.wait import time, WebDriverWait as Wait
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
from cssselect import GenericTranslator
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os


def browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    chrome_options.add_argument("window-position=500,0")
    chrome_options.add_argument("window-size=793,1167")

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def load_page(driver, page):
    driver.get(page)


chrome = browser()
load_page(chrome, 'http://127.0.0.1:8000/urban_development/login/')

def S(selector, n=0):
    return Wait(chrome, 5000).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))[n]

email = S('#id_username')
email.send_keys('liselottejongejans@gmail.com')
password = S('#id_password')
password.send_keys('rainsun3110')
button = S('button')
button.click()

url = chrome.current_url

if url == 'http://127.0.0.1:8000/urban_development/map/':
    print('Correct page')
else:
    print('Incorrect page')
