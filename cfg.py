from datetime import datetime, timedelta
from time import sleep
from random import randint
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By

# Browser-Chrome
chrome_driver_path = r'C:\Users\rogan\PycharmProjects\chromedriver.exe'
browser = webdriver.Chrome(executable_path=chrome_driver_path)
browser.maximize_window()


#   Browser
def browser_get(
        url, check,
        max_try):
    for i in range(max_try):
        try:
            browser.get(url)
            sleep(randint(0, 1))
            browser.find_element(by=By.CSS_SELECTOR, value=check)
            logging.info('ChromeDriver was opened successfully')
            return True
        except Exception as e:
            logging.info(f"Retry  {str(i)}  URL: {url}     #{e}")
    logging.error(f"Unable to open URL {url}")
    return False


# Xpath
def find_element_by_path(
        search_element,
        search_path):
    return search_element.find_element(by=By.XPATH, value=search_path)


def find_more_elements_by_path(
        search_element,
        search_path):
    return search_element.find_elements(by=By.XPATH, value=search_path)


def find_element_by_path_and_click(
        search_element,
        search_path):
    element = search_element.find_element(by=By.XPATH, value=search_path)
    element.click()
    return element


def find_element_by_path_and_take_text(
        search_element,
        search_path):
    return search_element.find_element(by=By.XPATH, value=search_path).text


def find_element_by_path_and_get_attribute(
        search_element, search_path,
        attribute):
    return search_element.find_element(by=By.XPATH, value=search_path).get_attribute(attribute)


# Css
def find_element_by_css(
        search_element,
        search_path):
    return search_element.find_element(by=By.CSS_SELECTOR, value=search_path)


def find_more_elements_by_css(
        search_element,
        search_path):
    return search_element.find_elements(by=By.CSS_SELECTOR, value=search_path)


def find_element_by_css_and_click(
        search_element,
        search_path):
    element = search_element.find_element(by=By.CSS_SELECTOR, value=search_path)
    element.click()
    return element


def find_element_by_css_and_take_text(
        search_element,
        search_path):
    return search_element.find_element(by=By.CSS_SELECTOR, value=search_path).text


def find_element_by_css_and_get_attribute(
        search_element, search_path,
        attribute):
    return search_element.find_element(by=By.CSS_SELECTOR, value=search_path).get_attribute(attribute)


# Date
def set_month(
        search_element, month,
        today_month, next_xpath):
    for _ in range(month - today_month):
        search_element.find_element(by=By.XPATH, value=next_xpath).click()
        sleep(randint(1, 2))
        logging.info("CLICK NEXT MONTH")
    return True


def set_date(
        search_element,
        date_check_in):
    date_in = datetime.strftime(date_check_in, '%Y-%m-%d')
    date_xpath = f'//td[@data-date="{date_in}"]'
    find_element_by_path_and_click(
        search_element, date_xpath
    )
    # find_date_check_in.click()
    sleep(randint(1, 2))
    return logging.info(f"CLICK  {date_in}")


def date_range(
        date_check_in,
        days_value):
    return date_check_in + timedelta(days=days_value)


# Map
def close_map(
        map_xpath):
    if not find_element_by_path(
            browser, map_xpath):
        return True
    return find_element_by_path_and_click(browser, map_xpath)
