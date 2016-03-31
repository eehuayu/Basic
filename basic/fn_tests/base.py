from selenium import webdriver
from django.test import TestCase

import unittest

class Base(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        
    def tearDown(self):
        self.browser.quit()
