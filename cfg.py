from datetime import datetime, timedelta
from time import sleep
from random import randint
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By

################################################################################################
# Browser-Chrome
chromeDriverPath = r'C:\Users\rogan\PycharmProjects\chromedriver.exe'
browser = webdriver.Chrome(executable_path=chromeDriverPath)
browser.maximize_window()


################################################################################################
#   Browser
def browser_get(url, check, max_try):
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


def findElementByXpath(searchElement, searchByPath):
    return searchElement.find_element(by=By.XPATH, value=searchByPath)


def findElementByXpathAndClick(searchElement, searchByPath):
    element = searchElement.find_element(by=By.XPATH, value=searchByPath)
    element.click()
    return element


def findElementByCss(searchElement, searchByPath):
    return searchElement.find_element(by=By.CSS_SELECTOR, value=searchByPath)


def findElementByCssAndClick(searchElement, searchByPath):
    element = searchElement.find_element(by=By.CSS_SELECTOR, value=searchByPath)
    element.click()
    return element


def setMonth(searchElement, month, todayMonth, nextXpath):
    for _ in range(month - todayMonth):
        searchElement.find_element(by=By.XPATH, value=nextXpath).click()
        sleep(randint(1, 2))
    logging.info("CLICK NEXT MONTH")
    return True


def setDate(searchElement, dateCheckIN):
    dateIN = datetime.strftime(dateCheckIN, '%Y-%m-%d')
    datXpath = f'//td[@data-date="{dateIN}"]'
    findDateCheckIn = searchElement.find_element(by=By.XPATH, value=datXpath)
    findDateCheckIn.click()
    sleep(randint(1, 2))
    return logging.info(f"CLICK  {dateIN}")


def checkMap():
    if not findElementByXpath(
            browser, '//*[@id="b2searchresultsPage"]/div[9]/div[2]'
    ):
        return True
    return findElementByXpathAndClick(browser, '//*[@id="b2searchresultsPage"]/div[9]/div[2]')


def dateRange(dateCheckIN, daysValue):
    return dateCheckIN + timedelta(days=daysValue)
