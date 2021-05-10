
import json
import sys
import logging
import time
from selenium import webdriver
from navigation.common_navigation import CommonNavigation
from navigation.zillow_navigation import ZillowNavigation

def write_to_file(file_name, content):
    file = open(file_name, "w")
    file.write(content)
    file.close()

def get_json_file_values(file_path):
    try:
        with open(file_path) as json_file:
            json_obj = json.load(json_file)
    except FileNotFoundError:
        sys.exit(f"File ({file_path}) was not found, please correct the path!")
    except Exception as e:
        sys.exit(f"An error with the json file occured. Error: {e}")
    return json_obj

def main():
    PATH = "C:\Driver\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.set_window_size(1600, 900)

    search_file_path = "F:zillow_search_bk.json"
    search_json = get_json_file_values(search_file_path)
    url = search_json["url"]
    driver.get(url)
    zillow_nav = ZillowNavigation(driver)
    common_nav = CommonNavigation(driver)

    zillow_nav.detected_captcha()
    common_nav.scroll_page_bottom()
    time.sleep(1)
    addr_links = zillow_nav.get_all_listing_from_zillow()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(name)s:  %(message)s', level=logging.DEBUG)
    main()
