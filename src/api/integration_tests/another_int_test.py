import unittest
from selenium import webdriver
# from selenium.webdriver.support.select import By
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.support.wait import WebDriverWait as Wait
# from selenium.common.exceptions import ElementNotInteractableException
# from selenium.webdriver.support import expected_conditions as EC
# from cssselect import GenericTranslator
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import os


class TestTest(unittest.TestCase):
    def setUp(self):

        self.driver = webdriver.Chrome()
        # self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        # navigate to the application home page
        self.driver.get("http://127.0.0.1:8000/urban_development/login/")

    def test_search_by_text(self):
        # get the email textbox
        self.email_field = self.driver.find_element_by_id('id_username')
        # enter email address for login
        self.email_field.send_keys('hauptest@hauptest.com')
        # self.driver.save_screenshot("screenshot1.png")
        # get the password textbox
        self.password_field = self.driver.find_element_by_id('id_password')
        # enter password for login
        self.password_field.send_keys('!helloT12345')
        # self.driver.save_screenshot("screenshot2.png")
        self.login_button = self.driver.find_element_by_xpath('//*[@id="content-box"]/form/button')
        self.login_button.click()

        self.map_url = self.driver.current_url
        self.assertEqual(self.map_url, 'http://127.0.0.1:8000/urban_development/map/')
        # self.driver.save_screenshot("screenshot3.png")

    def tearDown(self):
        # close the browser window
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
