from bs4 import BeautifulSoup

class CommonNavigation:
    def __init__(self, driver):
        self.driver = driver

    def get_page_soup(self):
        return BeautifulSoup(self.driver.page_source, "lxml")

    def scroll_page_bottom(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

