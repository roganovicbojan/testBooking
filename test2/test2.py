#!/usr/bin/python
from cfg import *
import requests
import uuid

################################################################################################
# IN
websiteLink = 'https://file-examples.com/'
################################################################################################
################################################################################################
################################################################################################
# logging
fileName = "Report file-examples"
logging.basicConfig(filename=f'{fileName}.log', format='%(asctime)s: %(levelname)s: %(message)s',
                    datefmt='%y/%m/%d', level=logging.INFO, filemode='w')
################################################################################################
browser_get(websiteLink, 'body', 5)
sleep(randint(1, 2))

features = browser.find_element(by=By.CSS_SELECTOR, value="#menu-item-27 > a")
features.click()
logging.info("CLICK TO features")
sleep(randint(1, 2))
documentsURL = browser.find_element(by=By.CSS_SELECTOR,
                                    value="#table-files > tbody > tr:nth-child(4) > td.text-right.file-link > a").get_attribute(
    'href')
browser.get(documentsURL)
logging.info(f"GET documents LINK {documentsURL}")
################################################################################################

downloadRows = browser.find_elements(by=By.CSS_SELECTOR, value='#table-files > tbody > tr')
for row in downloadRows:
    file_size = row.find_element(by=By.CSS_SELECTOR, value='td.file-ext').text
    link = row.find_element(by=By.CSS_SELECTOR, value='td.text-right.file-link > a.btn.btn-orange').get_attribute(
        'href')
    # print(file_size)
    # print(link)

    uuid_number = uuid.uuid1()

    dateAndTime = datetime.now()
    dateAndTimeTimestamp = datetime.timestamp(dateAndTime)
    fileName = f'{dateAndTimeTimestamp}_{uuid_number}_{file_size}.pdf'

    response = requests.get(link)

    # breakpoint()
    with open(f'files/{fileName}', 'wb') as f:
        f.write(response.content)
    logging.info(f"SUCCESSFULLY DOWNLOAD  {fileName}")

browser.quit()

logging.info("CODE FINISH SUCCESSFULLY")
