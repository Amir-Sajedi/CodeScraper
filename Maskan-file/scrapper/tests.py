import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RawData:
    def __init__(self,url):
        self.driver = webdriver.Chrome()
        self.url = url
        self.html = None
    def get_data(self):
        self.driver.get(self.url)
        time.sleep(3)
        # WebDriverWait(self.driver,3)
    def parse_html(self):
        self.html = bs(self.driver.page_source, 'html.parser')
        return self.html
    def get_parsed(self):
        return self.html


class MaskanData(RawData):
    def __init__(self, url):
        super().__init__(url)
        self.houses = []
    def get_all_houses(self):
        for house in self.html.select_one("#Div_Grv").find_all('div',recursive=False):
            # .find() is there to go one level deeper, First div is useless
            self.houses.append(house.find())
        return self.houses

    def show_more_btn(self):
        more_btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, "lnkmore"))
        )
        more_btn.click()
        time.sleep(3)

    # /////////////////// CAUTION ///////////////////////////
    def old_detector(self,x):
        for i in range(x):
            self.show_more_btn()

class MaskanHouse:
    def __init__(self,div):
        self.div = div
        self.html = None
        self.url = 'NO_LINK'
        self.name = "عنوان"
        self.address = "آدرس"
        self.price = "قیمت"
        self.area  = "متراژ"
        self.rooms_count  = "تعداد اتاق"
        self.year  = "سال ساخت"
        self.feats  = "امکانات"
        self.images  = "تصاویر"

    def complete_parse(self):
        self.get_ad_link()
        self.parse_html()
        self.get_name()

    def get_ad_link(self):
        links = self.div.find_all('div', onclick=lambda link: link is not None and link.startswith("window.open("))
        # Getting the link, no regex needed ;)
        self.url = links[0].get('onclick').split('(')[1][1:-2]

    def parse_html(self):
        url = self.url
        url_data = RawData(url)
        url_data.get_data()
        self.html = url_data.parse_html()

    def get_name(self):
        self.name = self.html.find('h4', class_='adds').get_text()



maskan_file_data = MaskanData("https://maskan-file.ir/Site/Default.aspx")
maskan_file_data.get_data()
# maskan_file_data.old_detector(10)
maskan_file_data.parse_html()
maskan_houses = []

for house in maskan_file_data.get_all_houses():
    # Make each house an object
    if(house.parent.get('id')):
        # Take the ads out
        maskan_houses.append(MaskanHouse(house))

test_house = maskan_houses[0]
test_house_next_page = maskan_houses[-1]
test_house.complete_parse()
test_house_next_page.complete_parse()
print(test_house.name)
print(test_house_next_page.name)