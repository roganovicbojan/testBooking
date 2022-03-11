#!/usr/bin/python
"""Avoid getting blocked by https://www.wmphvacations.com
and take a screenshot of two
different pages of the website"""
import re
from cfg import logging, sleep, randint, browser, find_more_elements_by_css
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# logging
REPORT_FILE_NAME = "Report wmphvacations"
logging.basicConfig(
    filename=f'{REPORT_FILE_NAME}.log',
    format='%(asctime)s: %(levelname)s: %(message)s',
    datefmt='%y/%m/%d', level=logging.INFO, filemode='w')

# Browser
options = Options()
wait = WebDriverWait(browser, 10)
WEBSITE_LINK = 'https://www.wmphvacations.com/'

browser.get(WEBSITE_LINK)
sleep(randint(10, 15))
# currentURL = browser.current_url
logging.info(f"Browser open {WEBSITE_LINK} "
             f"and redirect to {browser.current_url}")
all_links = find_more_elements_by_css(
    browser, '#menu-menu-header a')
list_url = [link.get_attribute('href') for link in all_links]
for url in list_url:
    browser.get(url)
    sleep(randint(2, 5))
    logging.info(f"SUCCESSFULLY open {url}")

    browser.execute_script("window.scrollTo(0, 200)")

    file_name = re.search('arrivia.com.(.*)', url).group(1).replace('/', '')
    file_name = f'screenShots/{file_name}.png'

    browser.get_screenshot_as_file(file_name)

    logging.info(f"SUCCESSFULLY take a screenshot  {file_name}")

    sleep(randint(1, 2))

browser.quit()

logging.info("CODE FINISH SUCCESSFULLY")
