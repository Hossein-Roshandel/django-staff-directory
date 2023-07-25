from django.test import LiveServerTestCase
from selenium import webdriver
from django.urls import reverse

class PollsIndexTest(LiveServerTestCase):
    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("-headless") 
        self.browser = webdriver.Firefox(options=options)
        # self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()
    
    def test_can_see_no_polls_available(self):
        self.browser.get(self.live_server_url + reverse('polls:index'))
        self.assertIn('No polls are available.', self.browser.page_source)
