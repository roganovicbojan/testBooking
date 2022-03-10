#!/usr/bin/python
from cfg import *
from datetime import date
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

################################################################################################
# IN
website_link = 'https://www.booking.com/'
currency = "USD"
Place = "Barcelona"
date_check_in = datetime(2022, 3, 10)  # Year,Month,Day
# date_check_out  = "2022-04-10"
days_value = 40
date_check_out = date_range(
    date_check_in,
    days_value)
adults_travel = 2
kids_travel = 0
ages_kids = [
    5, 2,
]
sort_in = 'Star rating and price'
price_max = 240
price_min = 90
filter_list = [
    "Hotels", "Air conditioning",
    "Very Good: 8+",
]
################################################################################################
################################################################################################
################################################################################################
# logging
report_file_name = "Report booking"
logging.basicConfig(
    filename=f'{report_file_name}.log', format='%(asctime)s: %(levelname)s: %(message)s',
    datefmt='%y/%m/%d', level=logging.INFO, filemode='w')
################################################################################################

browser_get(
    website_link,
    'body', 5)
sleep(randint(4, 6))
################################################################################################
# currency
currency_current = find_element_by_css(
    browser,
    'header > nav.bui-header__bar >'
    ' div.bui-group.bui-button-group.bui-group--inline.bui-group--align-end.bui-group--vertical-align-middle >'
    ' div:nth-child(1) > button')
if currency not in currency_current.text:
    currency_current.click()
    sleep(randint(1, 2))
    currency_part = browser.find_element(by=By.CLASS_NAME, value='bui-modal__header')
    currency_all = find_more_elements_by_css(
        currency_part, 'ul')

    for one_currency in currency_all:
        innerHTML = one_currency.get_attribute('innerHTML')
        if currency in innerHTML:
            currencyPosition = find_element_by_css_and_click(
                one_currency, 'a')
            sleep(randint(1, 2))
            break
    logging.info("Changing currency - DONE")
################################################################################################
# Place
search_where = find_element_by_path(
    browser, '//*[@id="ss"]')
search_where.send_keys(Place)
logging.info(f"SEND Key - {Place}")

wait = WebDriverWait(browser, 20)

path_to_confirm = f'//span[text()="{Place}"]'
select_from_drop_menu = wait.until(EC.element_to_be_clickable((By.XPATH, path_to_confirm)))
select_from_drop_menu.click()
sleep(randint(1, 3))
logging.info(f'SELECTED - {Place}')

################################################################################################
# check IN/OUT
todays_date = date.today()
today_month = todays_date.month
avaliable_months = [
    today_month,
    today_month + 1
]

month_in = date_check_in.month
month_out = date_check_out.month

if month_in not in avaliable_months:
    set_month(
        browser, month_in,
        today_month, '//div[@data-bui-ref="calendar-next"]')
set_date(
    browser, date_check_in)

if month_out not in avaliable_months:
    set_month(
        browser, month_out,
        today_month, '//div[@data-bui-ref="calendar-next"]')
set_date(
    browser, date_check_out)

logging.info(f"SELECTED - DATEs {date_check_in} | {date_check_out} ")
################################################################################################
# adults
adults = find_element_by_path_and_click(
    browser, '//*[@id="xp__guests__toggle"]')
adults_current = find_element_by_path(
    adults, '//span[@data-bui-ref="input-stepper-value"]')
adults_current_no = int(adults_current.text)
# print(adults_current_no, type(adults_current_no))
adults_part = find_element_by_path(
    browser, '//div[@class="sb-group__field sb-group__field-adults"]')
if adults_current_no > adults_travel:
    for minus in range(adults_current_no - adults_travel):
        minus_click = find_element_by_path_and_click(
            adults_part, '//button[@data-bui-ref="input-stepper-subtract-button"]')
        logging.info("MINUS Adult")
elif adults_current_no < adults_travel:
    for plus in range(adults_travel - adults_current_no):
        plus_lick = find_element_by_path_and_click(
            adults_part, '//button[@data-bui-ref="input-stepper-add-button"]')
        logging.info("PLUS Adult")
################################################################################################
# KIDS
if adults_travel != 0:
    kids_part = find_element_by_path(
        browser, '//div[@class="sb-group__field sb-group__field-adults"]')
    for kid_age in range(len(ages_kids)):
        addKid = find_element_by_path_and_click(
            kids_part, '//button[@aria-label="Increase number of Children"]')
        logging.info("ADD KID")
        sleep(randint(0, 1))
    logging.info(f"ADD {adults_travel} kids")

    age_part = find_element_by_path_and_click(
        browser, '//*[@id="xp__guests__inputs-container"]')
    # age_part.click()
    age_sets = find_more_elements_by_path(
        age_part, '//div/div/div[3]/select')
    # age_sets = age_part.find_elements(by=By.XPATH, value='//div/div/div[3]/select')
    kid_no = 0
    for one_set in age_sets:
        one_set.click()
        sleep(randint(1, 2))

        age = ages_kids[kid_no]
        # age_list = one_set.find_elements(by=By.CSS_SELECTOR, value="option")
        age_list = find_more_elements_by_css(
            one_set, 'option')

        for option in age_list[age + 1:age + 2]:
            option.click()
            logging.info(f"SELECT - AGE {age}")
            sleep(randint(2, 3))

        kid_no += 1

    logging.info("AGES ADDED")
################################################################################################
# Search
search = find_element_by_css_and_click(
    browser, '#frm div.xp__button button')
sleep(randint(5, 8))
logging.info("SEARCH - DONE")

if 'Map' in browser.current_url:
    close_map('//*[@id="b2searchresultsPage"]/div[9]/div[2]')
################################################################################################
# Sort
try:
    sortPart = find_element_by_path(
        browser, '//*[@id="right"]/div[1]/div/div/div/span/button')
    sortPart.click()
    print("CLICK")
    sortAll = find_element_by_path_and_click(
        browser, '//button[@data-id="class_and_price"]')
except:
    try:
        sortPart = find_more_elements_by_path(
            browser, '//div[1]/div/div/div[2]/ul/li')
        print(len(sortPart))
        for oneSort in sortPart:
            innerHtml = oneSort.get_attribute('innerHTML')
            if str(sort_in) in str(innerHtml):
                link = find_element_by_css(
                    oneSort, 'a')
                browser.get(link.get_attribute('href'))
                sleep(randint(1, 2))
                break
    except:
        sortPart = find_element_by_path(
            browser, '//button[@data-testid="sorters-dropdown-trigger"]')
        sortAll = find_element_by_path_and_click(
            browser, '//a[@data-id="class_and_price"')
        setPriceFilter = find_element_by_path_and_click(
            browser, f'//div[@data-testid="filters-group-label-content"][text()="{sort_in}"]')
if "Map" in browser.current_url:
    close_map('//*[@id="b2searchresultsPage"]/div[9]/div[2]')
################################################################################################
# Filters
allFilters = find_more_elements_by_path(
    browser, '//div[@data-testid="filters-group-label-content"]')
for oneFilter in filter_list:
    for onePosibleFilter in allFilters:
        try:
            filterInner = onePosibleFilter.text
        except:
            continue

        if oneFilter in str(filterInner):
            setFilter = find_element_by_path(
                browser, f'//div[@data-testid="filters-group-label-content"][text()="{oneFilter}"]')
            setFilter.click()
            logging.info(f'CLICK FILTER {oneFilter}')
            sleep(randint(2, 4))
            break

logging.info('SELECTED - Filters')
################################################################################################
# Range Price
currentURL = browser.current_url
URL = currentURL.replace('&sb=1', '').replace('&src_elem=sb', '').replace('#map_opened', '')
editedURL = f'{currentURL}&nflt=price%3DUSD-{price_min}-{price_max}-1'
browser_get(
    editedURL, 'body', 3)

if 'map_opened' in str(editedURL):
    close_map('//*[@id="b2searchresultsPage"]/div[9]/div[2]')
logging.info("PRICE RANGED")
################################################################################################
# Products
allProducts = find_more_elements_by_path(
    browser, '//div[@data-testid="property-card"]')
for oneProduct in allProducts[0:10]:
    name = find_element_by_path_and_take_text(
        oneProduct, '//div[@data-testid="title"]')
    price = find_element_by_path_and_take_text(
        oneProduct, '//div[@data-testid="price-and-discounted-price"]')
    score_and_reviews = find_element_by_path(
        oneProduct, '//div[@data-testid="review-score"]')
    number_of_reviews = find_element_by_css_and_take_text(
        score_and_reviews, 'div:nth-child(1)')
    score = find_element_by_css_and_take_text(
        score_and_reviews, 'div:nth-child(2)')
    location = find_element_by_path_and_take_text(
        oneProduct, '//div[@data-testid="location"]')
    image_url = find_element_by_path_and_get_attribute(
        oneProduct, '//img[@data-testid="image"]',
        'src')

    print(f"Name: {name}")
    print(f"Price: {price}")
    print(f"NumberOfReviews: {number_of_reviews}")
    print(f"Score: {score}")
    print(f"Location: {location}")
    print(f"ImageURL: {image_url}")
    logging.info(
        f"Name: {name}, Price: {price}, "
        f"NumberOfReviews: {number_of_reviews}, Score: {score}, "
        f"Location: {location}, ImageURL: {image_url}")

browser.quit()
logging.info("CODE FINISH SUCCESSFULLY")
