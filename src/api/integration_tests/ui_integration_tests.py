import unittest
from selenium import webdriver


class UIIntegrationTest(unittest.TestCase):
    def setUp(self):

        self.driver = webdriver.Chrome()
        # self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        # navigate to the application home page
        self.driver.get("http://127.0.0.1:8000/urban_development/login/")

    def test_login_user(self):
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

        self.user_name = self.driver.find_element_by_id('user-name')
        self.assertEqual(self.user_name.text, 'Hello, hauptest@hauptest.com')
        self.driver.quit()

    def test_login_guest(self):
        self.guest_login_button = self.driver.find_element_by_xpath('//*[@id="hyperlinks-container"]/a[3]')
        self.guest_login_button.click()

        self.guest_login_url = self.driver.current_url
        self.assertEqual(self.guest_login_url, 'http://127.0.0.1:8000/urban_development/map/')
        # self.driver.save_screenshot("screenshot4.png")

        self.guest_name = self.driver.find_element_by_id('user-name')
        self.assertEqual(self.guest_name.text, 'Hello, guest')
        self.driver.quit()

    def test_logout_user(self):
        self.email_field = self.driver.find_element_by_id('id_username')
        self.email_field.send_keys('hauptest@hauptest.com')
        self.password_field = self.driver.find_element_by_id('id_password')
        self.password_field.send_keys('!helloT12345')
        self.login_button = self.driver.find_element_by_xpath('//*[@id="content-box"]/form/button')
        self.login_button.click()
        self.logout_button = self.driver.find_element_by_xpath('//*[@id="email-cell"]/div/a')
        self.logout_button.click()
        # self.driver.save_screenshot("screenshot5.png")
        self.after_logout_url = self.driver.current_url
        self.assertEqual(self.after_logout_url, 'http://127.0.0.1:8000/urban_development/login/')
        # self.driver.save_screenshot("screenshot6.png")
        self.driver.quit()

    def test_change_password(self):
        self.to_change_password_button = self.driver.find_element_by_xpath('//*[@id="hyperlinks-container"]/a[1]')
        self.to_change_password_button.click()

        self.change_password_url = self.driver.current_url
        self.assertEqual(self.change_password_url, 'http://127.0.0.1:8000/urban_development/change_password/')
        # self.driver.save_screenshot("screenshot7.png")

        self.change_password_email = self.driver.find_element_by_id('id_email')
        self.change_password_email.send_keys('hauptest2@hauptest.com')
        self.change_password_button = self.driver.find_element_by_xpath('//*[@id="content-box"]/form/button')
        self.change_password_button.click()
        # self.driver.save_screenshot("screenshot8.png")

        self.after_change_password_url = self.driver.current_url
        self.assertIn('http://127.0.0.1:8000/urban_development/send_change_password_email/',
                      self.after_change_password_url)
        # self.driver.save_screenshot("screenshot9.png")

        self.resend_password_button = self.driver.find_element_by_xpath('//*[@id="hyperlinks-container"]/a[1]')
        self.resend_password_button.click()

        self.resend_password_url = self.driver.current_url
        self.assertIn('http://127.0.0.1:8000/urban_development/send_change_password_email/',
                      self.after_change_password_url)
        # self.driver.save_screenshot("screenshot10.png")

        self.back_to_login_after_change = self.driver.find_element_by_xpath('//*[@id="hyperlinks-container"]/a[2]')
        self.back_to_login_after_change.click()
        # self.driver.save_screenshot("screenshot11.png")

        self.login_after_change_password_url = self.driver.current_url
        self.assertEqual(self.login_after_change_password_url, 'http://127.0.0.1:8000/urban_development/login/')
        self.driver.quit()

    def test_register_user(self):
        self.register_user_button = self.driver.find_element_by_xpath('//*[@id="hyperlinks-container"]/a[2]')
        self.register_user_button.click()

        self.register_user_url = self.driver.current_url
        self.assertEqual(self.register_user_url, 'http://127.0.0.1:8000/urban_development/register/')
        # self.driver.save_screenshot("screenshot12.png")

        self.return_to_login_button = self.driver.find_element_by_xpath('//*[@id="hyperlinks-container"]/a')
        self.return_to_login_button.click()
        # self.driver.save_screenshot("screenshot13.png")

        self.login_after_registration_url = self.driver.current_url
        self.assertEqual(self.login_after_registration_url, 'http://127.0.0.1:8000/urban_development/login/')
        self.driver.quit()

    # def test_check_map_data_view(self):
    #     self.email_field = self.driver.find_element_by_id('id_username')
    #     self.email_field.send_keys('hauptest@hauptest.com')
    #     self.password_field = self.driver.find_element_by_id('id_password')
    #     self.password_field.send_keys('!helloT12345')
    #     self.login_button = self.driver.find_element_by_xpath('//*[@id="content-box"]/form/button')
    #     self.login_button.click()
    #     # self.driver.save_screenshot("screenshot14.png")
    #
    #     self.map_view_button = self.driver.find_element_by_xpath('//*[@id="map-view-button"]')
    #     self.data_view_button = self.driver.find_element_by_xpath('//*[@id="data-view-button"]')
    #     self.assertFalse(self.map_view_button.is_enabled())
    #     self.assertTrue(self.data_view_button.is_enabled())
    #
    #     self.data_view_button.click()
    #     self.assertTrue(self.map_view_button.is_enabled())
    #     self.assertFalse(self.data_view_button.is_enabled())
    #     self.driver.quit()

    def test_how_to_use_page(self):
        self.email_field = self.driver.find_element_by_id('id_username')
        self.email_field.send_keys('hauptest@hauptest.com')
        self.password_field = self.driver.find_element_by_id('id_password')
        self.password_field.send_keys('!helloT12345')
        self.login_button = self.driver.find_element_by_xpath('//*[@id="content-box"]/form/button')
        self.login_button.click()
        self.how_to_use_button = self.driver.find_element_by_xpath('//*[@id="how-to-view-button"]/a')
        self.how_to_use_button.click()

        # self.driver.save_screenshot("screenshot13.png")
        self.how_to_use_url = self.driver.current_url
        self.assertEqual(self.how_to_use_url, 'http://127.0.0.1:8000/urban_development/how_to_use/')

    # def tearDown(self):
    #     # close the browser window
    #     self.driver.quit()


if __name__ == '__main__':
    unittest.main()
