#!/usr/bin/python
"""Download pdf files from https://file-examples.com"""
import uuid
import requests
from testBooking.cfg import logging, datetime, sleep, randint, \
    browser, browser_get, find_more_elements_by_css, \
    find_elem_by_css_and_click, find_elem_by_css_and_take_text, \
    find_elem_by_css_and_get_attribute

# IN
WEBSITE_LINK = 'https://file-examples.com/'

# logging
REPORT_FILE_NAME = "Report file-examples"
logging.basicConfig(
    filename=f'{REPORT_FILE_NAME}.log',
    format='%(asctime)s: %(levelname)s: %(message)s',
    datefmt='%y/%m/%d', level=logging.INFO, filemode='w')

browser_get(
    WEBSITE_LINK,
    'body', 5)
sleep(randint(1, 2))

features = find_elem_by_css_and_click(
    browser, "#menu-item-27 > a")
logging.info("CLICK TO features")
sleep(randint(1, 2))

documents_url = find_elem_by_css_and_get_attribute(
    browser,
    "#table-files > tbody > tr:nth-child(4) > td.text-right.file-link > a",
    'href')
browser.get(documents_url)
logging.info(f"GET documents LINK {documents_url}")

download_rows = find_more_elements_by_css(
    browser, '#table-files > tbody > tr')
for row in download_rows:
    file_size = find_elem_by_css_and_take_text(
        row, 'td.file-ext')
    link = find_elem_by_css_and_get_attribute(
        row, 'td.text-right.file-link > a.btn.btn-orange',
        'href')
    # print(file_size)
    # print(link)

    uuid_number = uuid.uuid1()

    date_amd_time = datetime.now().timestamp()
    file_name = f'{date_amd_time}_{uuid_number}_{file_size}.pdf'

    response = requests.get(link)

    with open(f'files/{file_name}', 'wb') as f:
        f.write(response.content)
    logging.info(f"SUCCESSFULLY DOWNLOAD  {file_name}")

browser.quit()

logging.info("CODE FINISH SUCCESSFULLY")
