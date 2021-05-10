
import logging
import time
import re
from common_navigation import CommonNavigation

class ZillowNavigation:
    def __init__(self, driver):
        self.driver = driver
        self.com_nav = CommonNavigation(driver)

    def get_zillow_page_listings(self):
        addr_links = []
        result_soup = self.com_nav.get_page_soup()
        listings = result_soup.find("ul", class_="photo-cards").find_all("article", class_="list-card")
        for listing in listings:
            post = listing.find("a", class_="list-card-link")
            addr_links.append((post.string, post["href"]))
            print(f"{post.string} - {post['href']} ")
        return addr_links

    def click_zillow_next_page(self):
        result_soup = self.com_nav.get_page_soup()
        pagination = result_soup.find(id="grid-search-results").find("nav", {"class": re.compile("^StyledPagination.*")})
        next_button = pagination.find("a", rel="next")
        has_next = False
        if next_button and "tabindex" not in list(next_button.attrs.keys()):
            has_next = True
            self.driver.find_element_by_xpath("//a[(@rel = 'next') and (@title = 'Next page')]").click()
            time.sleep(5)
        else:
            logging.info("It's current at the last page.")
            return has_next
        pages = pagination.find_all("li", {"class": re.compile("^PaginationNumberItem")})
        curr_page = pagination.find("li", attrs={"aria-current": "page"}).string
        last_page = pages[-1].string
        logging.info(f"On page {curr_page} of {last_page}")
        return has_next

    def detected_captcha(self):
        if self.com_nav.get_page_soup().find("div", {"class": "captcha-container"}):
            # TODO: Implement a way to bypass the captcha
            input("Done solving the captcha?")

    def get_all_listing_from_zillow(self):
        addr_links = self.get_zillow_page_listings()
        while self.click_zillow_next_page():
            addr_links += self.get_zillow_page_listings()
        logging.info(f"Found {len(addr_links)} listings")
        return addr_links

