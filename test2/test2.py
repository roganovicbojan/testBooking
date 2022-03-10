#!/usr/bin/python
from cfg import *
import requests
import uuid

################################################################################################
# IN
website_link = 'https://file-examples.com/'
################################################################################################
################################################################################################
################################################################################################
# logging
report_file_name = "Report file-examples"
logging.basicConfig(
    filename=f'{report_file_name}.log', format='%(asctime)s: %(levelname)s: %(message)s',
    datefmt='%y/%m/%d', level=logging.INFO, filemode='w')
################################################################################################
browser_get(
    website_link,
    'body', 5)
sleep(randint(1, 2))

features = find_element_by_css_and_click(
    browser, "#menu-item-27 > a")
logging.info("CLICK TO features")
sleep(randint(1, 2))

documents_url = find_element_by_css_and_get_attribute(
    browser, "#table-files > tbody > tr:nth-child(4) > td.text-right.file-link > a",
    'href')
browser.get(documents_url)
logging.info(f"GET documents LINK {documents_url}")
################################################################################################

download_rows = find_more_elements_by_css(
    browser, '#table-files > tbody > tr')
for row in download_rows:
    file_size = find_element_by_css_and_take_text(
        row, 'td.file-ext')
    link = find_element_by_css_and_get_attribute(
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
