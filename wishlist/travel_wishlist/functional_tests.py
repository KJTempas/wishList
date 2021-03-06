#import selenium
#from selenium import webdriver
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver

from django.test import LiveServerTestCase
#do I need this? is it correct?
#driver = webdriver.Chrome('Users/kathryntempas/Desktop/Capstone/django_wishlist/wishlist')
#driver.get('http://www.google.com')

class TitleTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        #self.browser = webdriver.Chrome()
        #self.browser.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
        #self.browser.quit()

    def test_title_show_on_home_page(self):
        self.selenium.get(self.live_server_url)
        self.assertIn('Travel Wishlist', self.selenium.title)
        #self.browser.get(self.live_server_url)
        #self.assertIn(self.browser.title, 'Travel Wishlist')


class AddPlacesTest(LiveServerTestCase):

    fixtures = ['test_places']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        #self.browser = webdriver.Chrome()
        #self.browser.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
        #self.browser.quit()

    def test_add_new_place(self):

        self.selenium.get(self.live_server_url) #loads home page
        input_name = self.selenium.find_element_by_id('id_name') #find input text box. id was generated by Django forms
        input_name.send_keys('Denver')  #enter a place name
        
        add_button = self.selenium.find_element_by_id('add-new-place')  #find the add button
        add_button.click()  #and click it

        #make this test code wait for the server to process the request and for the page to reload
        #wait for the new element to appear on the page
        denver = self.selenium.find_element_by_id('place-name-5') #denver will have id 5
        #assert places from test_places are on page
        self.assertEqual('Denver', denver.text)

        self.assertIn('Tokyo', self.selenium.page_source)
        self.assertIn('New York', self.selenium.page_source)
        #and new place too
        self.assertIn('Denver', self.selenium.page_source)


