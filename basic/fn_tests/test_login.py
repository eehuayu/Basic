from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import TestCase

import time
import unittest
from unittest import skip

from .base import Base

class Login(Base):

    def test_login_with_incorrect_pwd(self):
        self.browser.get("http://localhost:8080/attendence/")
        time.sleep(3)    

        user_name = self.browser.find_element_by_name('user_name')
        user_name.send_keys('admin')
        time.sleep(3)

        pwd = self.browser.find_element_by_name('pwd')
        pwd.send_keys('adminX')
        pwd.send_keys('\n')
        
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Username or password is incorrect', page_text)

            
