from bs4 import BeautifulSoup as Bs
import requests
import csv
from time import sleep, strftime
from random import randint
import sys

#  Made for use with www.nonprofitlist.org, 2021


def make_url_list(var, var2):
    if str(var)[-1] == "/":
        urls = [str(var)[:-1]]
    else:
        urls = [str(var)]
    for i in range(2, var2+1):
        urls.append(urls[0]+"/"+str(i))
    return urls


def get_website(var):
    results = Bs(requests.get(var, timeout = 5.0).content, "html.parser").find(id="content")
    page_elements = results.find_all("div", class_="entry")
    if page_elements[0].find("a") is None:
        link = "N/A"
    else:
        link = page_elements[0].find("a")["href"].replace("https://", "")
    return link


def scrape(var):
    with open('nonprofs'+strftime("%Y%m%d-%H%M%S")+'.csv', mode='w') as nonprof_file:
        nonprof_writer = csv.writer(nonprof_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for URL in var:
            results = Bs(requests.get(URL).content, "html.parser").find(id="middle")
            page_elements = results.find_all("div", class_="portfolio_inner")
            for page_element in page_elements:
                title = page_element.find("h5", class_="entry-title").text.strip()
                if page_element.find("a") is None:
                    break
                page_link = page_element.find("a")["href"]
                contact = page_element.find("div", class_="entry-content")
                contact_list = contact.text.strip().replace(" ", "").replace("\r", "").split("\n")
                locale = contact_list[0]
                website = get_website(page_link)
                if len(contact_list) == 2:
                    phone = contact_list[1]
                else:
                    phone = "N/A"
                if "www.nonprofitlist.org" in website:
                    print(f"{title} has no website")
                elif "." not in website:
                    print(f"{title} has invalid website URL")
                else:
                    try:
                        requests.get(website)
                        nonprof_writer.writerow([title, phone, locale, website])
                        print(title + " added!")
                    except requests.exceptions.ConnectionError:
                        print(f"{title} not reachable")
                #sleep(randint(4, 7))


if len(sys.argv) != 3:
    print("""Invalid number of arguments 
Example usage: python3 scraper.py https://www.nonprofitlist.org/AZ/Phoenix.html 3""")
elif "www.nonprofitlist.org" not in sys.argv[1]:
    print("""Only for use with www.nonprofitlist.org 
Example usage: python3 scraper.py https://www.nonprofitlist.org/AZ/Phoenix.html 3""")
else:
    scrape(make_url_list(str(sys.argv[1]), int(sys.argv[2])))
