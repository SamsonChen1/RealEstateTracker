import requests
import json
import sys
import logging
from bs4 import BeautifulSoup

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


def main():
    search_file_path = "F:zillow_search_bk.json"
    search_json = get_json_file_values(search_file_path)
    url = search_json["url"]
    headers = search_json["header"]
    params = search_json["params"]

    key = extract_value("F:zillow_key.txt", "key")

    if not key:
        sys.exit("Unable to proceed without an valid Zillow API Key")

    result = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(result.text, "lxml")
    listings = soup.find("ul", class_="photo-cards").find_all("article", class_="list-card")
    for listing in listings:
        post = listing.find("a", class_="list-card-link")
        print(post.string)
        print(post["href"])


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(name)s:  %(message)s', level=logging.WARNING)
    main()
