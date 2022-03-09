from cfg import *
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

################################################################################################
# logging
fileName = "Report wmphvacations"
logging.basicConfig(filename=f'{fileName}.log', format='%(asctime)s: %(levelname)s: %(message)s',
                    datefmt='%y/%m/%d', level=logging.INFO, filemode='w')
################################################################################################
# Browser
options = Options()
# browser = webdriver.Chrome(chromeDriverPath, chrome_options=options)
wait = WebDriverWait(browser, 10)
websiteLink = 'https://www.wmphvacations.com/'
# browser.maximize_window()

browser.get(websiteLink)
sleep(randint(10, 15))
currentURL = browser.current_url
logging.info(f"Browser open {websiteLink} "
             f"and redirect to {currentURL}")
allLinks = browser.find_elements(by=By.CSS_SELECTOR, value='#menu-menu-header a')
listURL = [link.get_attribute('href') for link in allLinks]
for URL in listURL:
    browser.get(URL)
    sleep(randint(2, 5))
    logging.info(f"SUCCESSFULLY open {URL}")

    browser.execute_script("window.scrollTo(0, 200)")

    fileName = re.search('arrivia.com.(.*)', URL).group(1).replace('/', '')
    fileName = f'screenShots/{fileName}.png'
    browser.get_screenshot_as_file(fileName)

    logging.info(f"SUCCESSFULLY take a screenshot  {fileName}")

    sleep(randint(1, 2))

browser.quit()

logging.info("CODE FINISH SUCCESSFULLY")
