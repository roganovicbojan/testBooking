#!/usr/bin/python
"""This is configuration file"""
import sys
from datetime import datetime, timedelta
from time import sleep
from random import randint
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
sys.path.append(".")

# Browser-Chrome
CHROME_DRIVER = r"C:\Users\rogan\PycharmProjects\chromedriver.exe"
browser = webdriver.Chrome(executable_path=CHROME_DRIVER)
browser.maximize_window()


# Browser
def browser_get(
        url, check, max_try):
    """This def open Browser."""
    for i in range(max_try):
        try:
            browser.get(url)
            sleep(randint(0, 1))
            browser.find_element(by=By.CSS_SELECTOR, value=check)
            logging.info("ChromeDriver was opened successfully")
            return True
        except UserWarning:
            logging.warning("Retry: %s" " URL: %s", i, url)

            # logging.info(f"Retry  {str(i)}  URL: {url} %s")
    logging.error("Unable to open URL: %s ", url)
    return False


# Xpath
def find_elem_by_path(
        search_elem, search_path):
    """Find single element by Xpath"""
    return search_elem.find_element(by=By.XPATH, value=search_path)


def find_more_elements_by_path(
        search_elem, search_path):
    """Find More elements by Xpath"""
    return search_elem.find_elements(by=By.XPATH, value=search_path)


def find_elem_by_path_and_click(
        search_elem, search_path):
    """Find element by Xpath and Click"""
    result = search_elem.find_element(by=By.XPATH, value=search_path)
    result.click()
    return result


def find_elem_by_path_and_take_text(
        search_elem, search_path):
    """Find element by Xpath and take text"""
    return search_elem.find_element(by=By.XPATH, value=search_path).text


def find_elem_by_path_and_get_attribute(
        search_elem, search_path, attribute):
    """Find element by Xpath and get attribute"""
    return search_elem.find_element(by=By.XPATH, value=search_path)\
        .get_attribute(attribute)


# Css Selector
def find_elem_by_css(
        search_elem, search_path):
    """Find single element by css selector"""
    return search_elem.find_element(by=By.CSS_SELECTOR, value=search_path)


def find_more_elements_by_css(
        search_elem, search_path):
    """Find More elements by css selector"""
    return search_elem.find_elements(by=By.CSS_SELECTOR, value=search_path)


def find_elem_by_css_and_click(
        search_elem, search_path):
    """Find element by css selector and Click"""
    result = search_elem.find_element(by=By.CSS_SELECTOR, value=search_path)
    result.click()
    return result


def find_elem_by_css_and_take_text(
        search_elem, search_path):
    """Find element by css selector and take text"""
    return search_elem.find_element(by=By.CSS_SELECTOR, value=search_path).text


def find_elem_by_css_and_get_attribute(
        search_elem, search_path, attribute):
    """Find element by css selector and get attribute"""
    return search_elem.find_element(
        by=By.CSS_SELECTOR, value=search_path
    ).get_attribute(attribute)


# Date
def set_month(
        search_elem, month, today_month, next_xpath):
    """In the calendar, the code changes the month"""
    for _ in range(month - today_month):
        search_elem.find_element(by=By.XPATH, value=next_xpath).click()
        sleep(randint(1, 2))
        logging.info("CLICK NEXT MONTH")
    return True


def set_date(
        search_elem, date_check_in):
    """Finds date and selects"""
    date_in = datetime.strftime(date_check_in, "%Y-%m-%d")
    date_xpath = f'//td[@data-date="{date_in}"]'
    find_elem_by_path_and_click(search_elem, date_xpath)
    sleep(randint(1, 2))
    return logging.info("CLICK  %s", date_in)


def date_range(
        date_check_in, days_value):
    """Counting the number of days"""
    return date_check_in + timedelta(days=days_value)


def close_map(
        map_xpath):
    """Turn off the map"""
    if not find_elem_by_path(browser, map_xpath):
        return True
    return find_elem_by_path_and_click(browser, map_xpath)
