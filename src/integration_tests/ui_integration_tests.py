"""
ui_integration_tests.py
"""

import unittest
from selenium import webdriver


class UIIntegrationTests(unittest.TestCase):
    """
    class UIIntegrationTests(unittest.TestCase)
    """

    register_user_button = None
    register_user_url = None
    return_to_login_button = None
    login_after_registration_url = None
    guest_login_button = None
    guest_login_url = None
    guest_name = None
    email_field = None
    password_field = None
    login_button = None
    map_url = None
    user_name = None
    logout_button = None
    after_logout_url = None
    to_change_password_button = None
    change_password_url = None
    change_password_email = None
    change_password_button = None
    after_change_password_url = None
    resend_password_button = None
    resend_password_url = None
    back_to_login_after_change = None
    login_after_change_password_url = None
    how_to_use_button = None
    how_to_use_url = None

    def setUp(self):
        """
        def setUp(self)
        """

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        # navigate to the application home page
        self.driver.get("http://127.0.0.1:8000/urban_development/login/")

    def test_register_user(self):
        """
        def test_register_user(self)
        """

        self.register_user_button = self.driver.find_element_by_xpath('//*[@id="hyperlinks-container"]/a[2]')
        self.register_user_button.click()

        self.register_user_url = self.driver.current_url
        self.assertEqual(self.register_user_url, 'http://127.0.0.1:8000/urban_development/register/')

        self.return_to_login_button = self.driver.find_element_by_xpath('//*[@id="hyperlinks-container"]/a')
        self.return_to_login_button.click()

        self.login_after_registration_url = self.driver.current_url
        self.assertEqual(self.login_after_registration_url, 'http://127.0.0.1:8000/urban_development/login/')

        self.driver.quit()

    def test_login_guest(self):
        """
        def test_login_guest(self)
        """

        self.guest_login_button = self.driver.find_element_by_xpath('//*[@id="hyperlinks-container"]/a[3]')
        self.guest_login_button.click()

        self.guest_login_url = self.driver.current_url
        self.assertEqual(self.guest_login_url, 'http://127.0.0.1:8000/urban_development/main/')

        self.guest_name = self.driver.find_element_by_id('user-name')
        self.assertEqual(self.guest_name.text, 'Hello, guest')

        self.driver.quit()

    def test_login_user(self):
        """
        def test_login_user(self)
        """

        # get the email textbox
        self.email_field = self.driver.find_element_by_id('id_username')

        # enter email address for login
        self.email_field.send_keys('hauptest@hauptest.com')

        # get the password textbox
        self.password_field = self.driver.find_element_by_id('id_password')

        # enter password for login
        self.password_field.send_keys('!helloT12345')

        self.login_button = self.driver.find_element_by_xpath('//*[@id="content-box"]/form/button')
        self.login_button.click()

        self.map_url = self.driver.current_url
        self.assertEqual(self.map_url, 'http://127.0.0.1:8000/urban_development/main/')

        self.user_name = self.driver.find_element_by_id('user-name')
        self.assertEqual(self.user_name.text, 'Hello, hauptest@hauptest.com')

        self.driver.quit()

    def test_logout_user(self):
        """
        def test_logout_user(self)
        """

        # get the email textbox
        self.email_field = self.driver.find_element_by_id('id_username')

        # enter email address for login
        self.email_field.send_keys('hauptest@hauptest.com')

        # get the password textbox
        self.password_field = self.driver.find_element_by_id('id_password')

        # enter password for login
        self.password_field.send_keys('!helloT12345')

        self.login_button = self.driver.find_element_by_xpath('//*[@id="content-box"]/form/button')
        self.login_button.click()

        self.logout_button = self.driver.find_element_by_xpath('//*[@id="email-cell"]/div/a')
        self.logout_button.click()

        self.after_logout_url = self.driver.current_url
        self.assertEqual(self.after_logout_url, 'http://127.0.0.1:8000/urban_development/login/')

        self.driver.quit()

    def test_change_password(self):
        """
        def test_change_password(self)
        """

        self.to_change_password_button = self.driver.find_element_by_xpath('//*[@id="hyperlinks-container"]/a[1]')
        self.to_change_password_button.click()

        self.change_password_url = self.driver.current_url
        self.assertEqual(self.change_password_url, 'http://127.0.0.1:8000/urban_development/change_password/')

        self.change_password_email = self.driver.find_element_by_id('id_email')
        self.change_password_email.send_keys('hauptest2@hauptest.com')
        self.change_password_button = self.driver.find_element_by_xpath('//*[@id="content-box"]/form/button')
        self.change_password_button.click()

        self.after_change_password_url = self.driver.current_url
        self.assertIn('http://127.0.0.1:8000/urban_development/send_change_password_email/',
                      self.after_change_password_url)

        self.resend_password_button = self.driver.find_element_by_xpath('//*[@id="hyperlinks-container"]/a[1]')
        self.resend_password_button.click()

        self.resend_password_url = self.driver.current_url
        self.assertIn('http://127.0.0.1:8000/urban_development/send_change_password_email/',
                      self.after_change_password_url)

        self.back_to_login_after_change = self.driver.find_element_by_xpath('//*[@id="hyperlinks-container"]/a[2]')
        self.back_to_login_after_change.click()

        self.login_after_change_password_url = self.driver.current_url
        self.assertEqual(self.login_after_change_password_url, 'http://127.0.0.1:8000/urban_development/login/')

        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
