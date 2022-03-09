#!/usr/bin/python
import logging
from selenium import webdriver

################################################################################################
# IN
websiteLink = 'https://www.httpbin.org/headers'
chromeDriverPath = r'C:\Users\rogan\PycharmProjects\chromedriver.exe'
################################################################################################
################################################################################################
################################################################################################
# logging
fileName = "Report 4"
logging.basicConfig(filename=f'{fileName}.log', format='%(asctime)s: %(levelname)s: %(message)s',
                    datefmt='%y/%m/%d', level=logging.INFO, filemode='w')
################################################################################################
browser = webdriver.Chrome(executable_path=chromeDriverPath)

browser.get(websiteLink)
page_source = browser.page_source
logging.info(f'BEFORE: {"#" * 100}')
logging.info(page_source)
browser.quit()
################################################################################################

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument("--incognito")
# options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("disable-infobars")
browser = webdriver.Chrome(options=options, executable_path=chromeDriverPath)
browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
browser.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

browser.get(websiteLink)
page_source = browser.page_source
logging.info(f'AFTER edit Options: {"#" * 100}')
logging.info("After add_argument, add_experimental_option, execute_script and execute_cdp_cmd")
logging.info(page_source)
browser.quit()
