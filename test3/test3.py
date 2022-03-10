#!/usr/bin/python
from cfg import *
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

################################################################################################
# logging
report_file_name = "Report wmphvacations"
logging.basicConfig(
    filename=f'{report_file_name}.log', format='%(asctime)s: %(levelname)s: %(message)s',
    datefmt='%y/%m/%d', level=logging.INFO, filemode='w')
################################################################################################
# Browser
options = Options()
wait = WebDriverWait(browser, 10)
website_link = 'https://www.wmphvacations.com/'

browser.get(website_link)
sleep(randint(10, 15))
# currentURL = browser.current_url
logging.info(f"Browser open {website_link} "
             f"and redirect to {browser.current_url}")
allLinks = find_more_elements_by_css(
    browser, '#menu-menu-header a')
listURL = [link.get_attribute('href') for link in allLinks]
for URL in listURL:
    browser.get(URL)
    sleep(randint(2, 5))
    logging.info(f"SUCCESSFULLY open {URL}")

    browser.execute_script("window.scrollTo(0, 200)")

    file_name = re.search('arrivia.com.(.*)', URL).group(1).replace('/', '')
    file_name = f'screenShots/{file_name}.png'

    browser.get_screenshot_as_file(file_name)

    logging.info(f"SUCCESSFULLY take a screenshot  {file_name}")

    sleep(randint(1, 2))

browser.quit()

logging.info("CODE FINISH SUCCESSFULLY")
