from django.test import TestCase
from datetime import date

from django.contrib.auth import get_user_model

from .models import OrderLine, Order, Comment, Product, Category, PotravinyFeatures, CustomUser
from datetime import date

# Create your tests here.

# pip install selenium
# tests.py
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
import time


class MySeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up the WebDriver (make sure the path is correct if needed)
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

        cls.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com'
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # Access the live server URL
        self.selenium.get(f'{self.live_server_url}/accounts/login/')
        time.sleep(2)
        # Find the username and password input fields and fill them
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        time.sleep(2)
        # Submit the form
        self.selenium.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(2)

        # Test that we successfully logged in (check for a successful redirect or message)
        self.assertIn("User logged in: admin - Logout", self.selenium.page_source)
