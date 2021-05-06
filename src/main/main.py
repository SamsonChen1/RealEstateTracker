import requests
import json
import sys
import logging
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def write_to_file(file_name, content):
    file = open(file_name, "w")
    file.write(content)
    file.close()

def extract_value(conf_filename, key):
    try:
        with open(conf_filename) as f:
            content = f.read()
        attr_list = content.split("\n")
        for line in attr_list:
            attr = line.strip().split("=", maxsplit=1)
            if key.lower() == attr[0]:
                return attr[1].strip()
    except FileNotFoundError:
        sys.exit(f"File ({conf_filename}) was not found, please correct the path!")
    print(f"Unable to find the key specified (\"{key}\") within the config file!")
    return None

def get_json_file_values(file_path):
    try:
        with open(file_path) as json_file:
            json_obj = json.load(json_file)
    except FileNotFoundError:
        sys.exit(f"File ({file_path}) was not found, please correct the path!")
    except Exception as e:
        sys.exit(f"An error with the json file occured. Error: {e}")
    return json_obj

def get_page_soup(driver):
    return BeautifulSoup(driver.page_source, "lxml")

def get_zillow_page_listings(driver: webdriver):
    addr_links = []
    result_soup = get_page_soup(driver)
    listings = result_soup.find("ul", class_="photo-cards").find_all("article", class_="list-card")
    for listing in listings:
        post = listing.find("a", class_="list-card-link")
        addr_links.append((post.string, post["href"]))
        print(f"{post.string} - {post['href']} ")
    return addr_links

def click_zillow_next_page(driver):
    result_soup = get_page_soup(driver)
    pagination = result_soup.find(id="grid-search-results").find("nav", {"class": re.compile("^StyledPagination.*")})
    next_button = pagination.find("a", rel="next")
    has_next = False
    if next_button and "tabindex" not in list(next_button.attrs.keys()):
        has_next = True
        driver.find_element_by_xpath("//a[(@rel = 'next') and (@title = 'Next page')]").click()
        time.sleep(3)
    else:
        logging.info("No next page button as the results only have a single page")
        return has_next
    pages = pagination.find_all("li", {"class": re.compile("^PaginationNumberItem")})
    curr_page = pagination.find("li", attrs={"aria-current": "page"}).string
    last_page = pages[-1].string
    logging.info(f"On page {curr_page} of {last_page}")
    return has_next

def scroll_page_bottom(driver):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

def detected_captcha(driver):
    if get_page_soup(driver).find("div", {"class": "captcha-container"}):
        # TODO: Implement a way to bypass the captcha
        input("Done solving the captcha?")


def main():
    PATH = "C:\Driver\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.set_window_size(1600, 900)

    search_file_path = "F:zillow_search_bk.json"
    search_json = get_json_file_values(search_file_path)
    url = search_json["url"]
    headers = search_json["header"]
    params = search_json["params"]
    key = extract_value("F:zillow_key.txt", "key")

    if not key:
        sys.exit("Unable to proceed without an valid Zillow API Key")

    # result = requests.get(url, headers=headers, params=params)
    driver.get(url)
    detected_captcha(driver)
    scroll_page_bottom(driver)
    time.sleep(1)
    addr_links = get_zillow_page_listings(driver)
    while click_zillow_next_page(driver):
        addr_links += get_zillow_page_listings(driver)

    print(f"number of listings {len(addr_links)}")



if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(name)s:  %(message)s', level=logging.DEBUG)
    main()
