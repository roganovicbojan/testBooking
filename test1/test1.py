#!/usr/bin/python
"""Navigate through booking.com to extract information"""
from datetime import date
from testBooking.cfg import logging, datetime, sleep, randint, date_range,\
    browser, browser_get, By, find_elem_by_path, \
    find_more_elements_by_path, find_elem_by_path_and_click, \
    find_elem_by_path_and_take_text, find_elem_by_path_and_get_attribute,\
    find_elem_by_css, find_more_elements_by_css,\
    find_elem_by_css_and_click, find_elem_by_css_and_take_text,\
    set_month, set_date, close_map
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#############################################################
# IN
WEBSITE_LINK = "https://www.booking.com/"
CURRENCY = "USD"
PLACE = "Barcelona"
date_check_in = datetime(2022, 3, 15)  # Year,Month,Day
# date_check_out  = "2022-04-10"
DAYS = 40
date_check_out = date_range(
    date_check_in, DAYS)
ADULTS_TRAVEL = 2
KIDS_TRAVEL = 0
AGES_KIDS = [
    5, 2,
]
SORT_IN = "Star rating and price"
PRICE_MAX = 240
PRICE_MIN = 90
FILTER_LIST = [
    "Hotels",
    "Air conditioning",
    "Very Good: 8+",
]
#############################################################
# logging
REPORT_FILE_NAME = "Report booking"
logging.basicConfig(
    filename=f"{REPORT_FILE_NAME}.log",
    format="%(asctime)s: %(levelname)s: %(message)s",
    datefmt="%y/%m/%d",
    level=logging.INFO,
    filemode="w")
#############################################################
# start Browser
browser_get(
    WEBSITE_LINK, "body", 5)
sleep(randint(4, 6))

# CURRENCY
currency_current = find_elem_by_css(
    browser,
    "header > nav.bui-header__bar >"
    " div.bui-group.bui-button-group.bui-group--inline."
    "bui-group--align-end.bui-group--vertical-align-middle >"
    " div:nth-child(1) > button")
if CURRENCY not in currency_current.text:
    currency_current.click()
    sleep(randint(1, 2))
    currency_part = find_elem_by_css(
        browser, "bui-modal__header")
    currency_all = find_more_elements_by_css(
        currency_part, "ul")

    for one_currency in currency_all:
        inner_html = one_currency.get_attribute("inner_html")
        if CURRENCY in inner_html:
            currencyPosition = find_elem_by_css_and_click(
                one_currency, "a")
            sleep(randint(1, 2))
            break
    logging.info("Changing currency - DONE")

# Place
search_where = find_elem_by_path(
    browser, '//*[@id="ss"]')
search_where.send_keys(PLACE)
logging.info(f"SEND Key - {PLACE}")

wait = WebDriverWait(
    browser, 20)

path_to_confirm = f'//span[text()="{PLACE}"]'
select_from_drop_menu = wait.until(
    EC.element_to_be_clickable((By.XPATH, path_to_confirm))
)
select_from_drop_menu.click()
sleep(randint(1, 3))
logging.info("SELECTED: %", PLACE)


# check IN/OUT
todays_date = date.today()
today_month = todays_date.month
avaliable_months = [
    today_month,
    today_month + 1,
]

month_in = date_check_in.month
month_out = date_check_out.month

if month_in not in avaliable_months:
    set_month(
        browser, month_in, today_month, '//div[@data-bui-ref="calendar-next"]')
set_date(browser, date_check_in)

if month_out not in avaliable_months:
    set_month(
        browser, month_out, today_month,
        '//div[@data-bui-ref="calendar-next"]')
set_date(browser, date_check_out)

logging.info("SELECTED - DATEs %s | %s", date_check_in, date_check_out)

# adults
adults = find_elem_by_path_and_click(browser, '//*[@id="xp__guests__toggle"]')
adults_current = find_elem_by_path(
    adults, '//span[@data-bui-ref="input-stepper-value"]')
adults_current_no = int(adults_current.text)

adults_part = find_elem_by_path(
    browser, '//div[@class="sb-group__field sb-group__field-adults"]')
if adults_current_no > ADULTS_TRAVEL:
    for minus in range(adults_current_no - ADULTS_TRAVEL):
        minus_click = find_elem_by_path_and_click(
            adults_part,
            '//button[@data-bui-ref="input-stepper-subtract-button"]')
        logging.info("MINUS Adult")
elif adults_current_no < ADULTS_TRAVEL:
    for plus in range(ADULTS_TRAVEL - adults_current_no):
        plus_lick = find_elem_by_path_and_click(
            adults_part, '//button[@data-bui-ref="input-stepper-add-button"]')
        logging.info("PLUS Adult")

# KIDS
if KIDS_TRAVEL != 0:
    kids_part = find_elem_by_path(
        browser, '//div[@class="sb-group__field sb-group__field-adults"]')
    for kid_age in range(len(KIDS_TRAVEL)):
        addKid = find_elem_by_path_and_click(
            kids_part, '//button[@aria-label="Increase number of Children"]')
        logging.info("ADD KID")
        sleep(randint(0, 1))
    logging.info(f"ADD {KIDS_TRAVEL} kids")

    age_part = find_elem_by_path_and_click(
        browser, '//*[@id="xp__guests__inputs-container"]')

    age_sets = find_more_elements_by_path(
        age_part, "//div/div/div[3]/select")

    KIN_NO = 0
    for one_set in age_sets:
        one_set.click()
        sleep(randint(1, 2))

        AGE = AGES_KIDS[KIN_NO]
        age_list = find_more_elements_by_css(
            one_set, "option")

        for option in age_list[AGE + 1: AGE + 2]:
            option.click()
            logging.info("SELECT - AGE %s", AGE)
            sleep(randint(2, 3))
        KIN_NO += 1

    logging.info("AGES ADDED")

# Search
search = find_elem_by_css_and_click(
    browser, "#frm div.xp__button button")
sleep(randint(5, 8))
logging.info("SEARCH - DONE")

if "Map" in browser.current_url:
    close_map('//*[@id="b2searchresultsPage"]/div[9]/div[2]')

# Sort
try:
    sort_part = find_elem_by_path_and_click(
        browser, '//*[@id="right"]/div[1]/div/div/div/span/button')
    sort_all = find_elem_by_path_and_click(
        browser, '//button[@data-id="class_and_price"]')
except AttributeError:
    try:
        sort_parts = find_more_elements_by_path(
            browser, "//div[1]/div/div/div[2]/ul/li")
        for one_sort in sort_parts:
            inner_html = one_sort.get_attribute("inner_html")
            if str(SORT_IN) in str(inner_html):
                link = find_elem_by_css(
                    one_sort, "a")
                browser.get(link.get_attribute("href"))
                break
    except AttributeError:
        sort_part = find_elem_by_path(
            browser, '//button[@data-testid="sorters-dropdown-trigger"]')
        sort_all = find_elem_by_path_and_click(
            browser, '//a[@data-id="class_and_price"')
        set_price_filter = find_elem_by_path_and_click(
            browser,
            f'//div[@data-testid="filters-group-label-content"]'
            f'[text()="{SORT_IN}"]')
sleep(randint(2, 3))

if "Map" in browser.current_url:
    close_map('//*[@id="b2searchresultsPage"]/div[9]/div[2]')

# Filters
all_filters = find_more_elements_by_path(
    browser, '//div[@data-testid="filters-group-label-content"]')
for one_filter in FILTER_LIST:
    for one_posible_filter in all_filters:
        try:
            filter_text = one_posible_filter.text
        except IndexError:
            continue

        if one_filter in str(filter_text):
            set_filter = find_elem_by_path(
                browser,
                f'//div[@data-testid="filters-group-label-content"]'
                f'[text()="{one_filter}"]',
            )
            set_filter.click()
            logging.info(f"CLICK FILTER {one_filter}")
            sleep(randint(2, 4))
            break

logging.info("SELECTED - Filters")

# Range Price
current_url = browser.current_url
current_url = str(current_url).replace("&sb=1", "")\
    .replace("&src_elem=sb", "").replace("#map_opened", "")
edited_url = f"{current_url}&nflt=price%3DUSD-{PRICE_MIN}-{PRICE_MAX}-1"
browser_get(edited_url, "body", 3)

if "map_opened" in str(edited_url):
    close_map('//*[@id="b2searchresultsPage"]/div[9]/div[2]')
logging.info("PRICE RANGED")

# Products
all_products = find_more_elements_by_path(
    browser, '//div[@data-testid="property-card"]'
)
for one_product in all_products[0:10]:
    name = find_elem_by_path_and_take_text(
        one_product, '//div[@data-testid="title"]'
    )
    price = find_elem_by_path_and_take_text(
        one_product, '//div[@data-testid="price-and-discounted-price"]'
    )
    score_and_reviews = find_elem_by_path(
        one_product, '//div[@data-testid="review-score"]'
    )
    number_of_reviews = find_elem_by_css_and_take_text(
        score_and_reviews, "div:nth-child(1)"
    )
    score = find_elem_by_css_and_take_text(
        score_and_reviews, "div:nth-child(2)"
    )
    location = find_elem_by_path_and_take_text(
        one_product, '//div[@data-testid="location"]'
    )
    image_url = find_elem_by_path_and_get_attribute(
        one_product, '//img[@data-testid="image"]', "src"
    )

    print("Name: %s", name)
    print("Price: %s", price)
    print("NumberOfReviews: %s", number_of_reviews)
    print("Score: %s", score)
    print("Location: %s", location)
    print("ImageURL: %s", image_url)
    logging.info(
        "Name: %s, Price: %s, "
        "NumberOfReviews: %s, Score: %s, "
        "Location: %s, ImageURL: %s",
        name, price, number_of_reviews, score, location, image_url
    )

browser.quit()
logging.info("CODE FINISH SUCCESSFULLY")
