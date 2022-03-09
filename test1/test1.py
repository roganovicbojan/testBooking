#!/usr/bin/python
from cfg import *
from datetime import date
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

################################################################################################
# IN
websiteLink = 'https://www.booking.com/'
currency = "USD"
Place = "Barcelona"
dateCheckIN = datetime(2022, 3, 10)  # Year,Month,Day
# dateCheckOUT  = "2022-04-10"
daysValue = 40
dateCheckOUT = dateRange(dateCheckIN, daysValue)
adults = 2
kids = 0
agesKids = [5, 2]
sortIN = 'Star rating and price'
priceMax = 240
priceMin = 90
filterList = ["Hotels", "Air conditioning", "Very Good: 8+"]
################################################################################################
################################################################################################
################################################################################################
# logging
fileName = f"Report booking"
logging.basicConfig(filename=f'{fileName}.log', format='%(asctime)s: %(levelname)s: %(message)s',
                    datefmt='%y/%m/%d', level=logging.INFO, filemode='w')
################################################################################################

browser_get(websiteLink, 'body', 5)
sleep(randint(4, 6))
################################################################################################
# currency
currencyCurrent = findElementByCss(browser,
                                   'header > nav.bui-header__bar > div.bui-group.bui-button-group.bui-group--inline.bui-group--align-end.bui-group--vertical-align-middle > div:nth-child(1) > button')
if currency not in currencyCurrent.text:
    currencyCurrent.click()
    sleep(randint(1, 2))
    currencyPart = browser.find_element(by=By.CLASS_NAME, value='bui-modal__header')
    currencyAll = currencyPart.find_elements(by=By.CSS_SELECTOR, value='ul')

    for oneCurrency in currencyAll:
        innerHTML = oneCurrency.get_attribute('innerHTML')
        if currency in innerHTML:
            currencyPosition = oneCurrency.find_element(by=By.CSS_SELECTOR, value='a')
            currencyPosition.click()
            sleep(randint(1, 2))
            break
    logging.info("Changing currency - DONE")
################################################################################################
# Place
searchWhere = findElementByXpath(browser, '//*[@id="ss"]')
searchWhere.send_keys(Place)
logging.info(f"SEND Key - {Place}")

wait = WebDriverWait(browser, 20)

pathToConfirm = f'//span[text()="{Place}"]'
selectFromDropMenu = wait.until(EC.element_to_be_clickable((By.XPATH, pathToConfirm)))
selectFromDropMenu.click()
sleep(randint(1, 3))
logging.info(f'SELECTED - {Place}')

################################################################################################
# check IN/OUT
todaysDate = date.today()
todayMonth = todaysDate.month
avaliableMonths = [todayMonth, todayMonth + 1]

monthIN = dateCheckIN.month
monthOUT = dateCheckOUT.month

if monthIN not in avaliableMonths:
    avaliableMonths = setMonth(browser, monthIN, todayMonth, '//div[@data-bui-ref="calendar-next"]')
setDate(browser, dateCheckIN)

if monthOUT not in avaliableMonths:
    setMonth(browser, monthOUT, todayMonth, '//div[@data-bui-ref="calendar-next"]')
setDate(browser, dateCheckOUT)

logging.info(f"SELECTED - DATEs {dateCheckIN} | {dateCheckOUT} ")
################################################################################################
# Adults
Adults = findElementByXpath(browser, '//*[@id="xp__guests__toggle"]')
Adults.click()
adultsCurrentNO = findElementByXpath(Adults, '//span[@data-bui-ref="input-stepper-value"]')
adultsCurrentNO = int(adultsCurrentNO.text)

adultsPart = browser.find_element(by=By.XPATH, value='//div[@class="sb-group__field sb-group__field-adults"]')
if adultsCurrentNO > adults:
    for minus in range(adultsCurrentNO - adults):
        minusClick = findElementByXpathAndClick(adultsPart, '//button[@data-bui-ref="input-stepper-subtract-button"]')
        logging.info("MINUS Adult")
elif adultsCurrentNO < adults:
    for plus in range(adults - adultsCurrentNO):
        plusClick = findElementByXpathAndClick(adultsPart, '//button[@data-bui-ref="input-stepper-add-button"]')
        logging.info("PLUS Adult")
################################################################################################
# KIDS
if kids != 0:
    kidsPart = findElementByXpath(browser, '//div[@class="sb-group__field sb-group__field-adults"]')
    for kidAge in range(len(agesKids)):
        addKid = findElementByXpathAndClick(kidsPart, '//button[@aria-label="Increase number of Children"]')
        logging.info("ADD KID")
        sleep(randint(0, 1))
    logging.info(f"ADD {kids} kids")

    agePart = findElementByXpath(browser, '//*[@id="xp__guests__inputs-container"]')
    agePart.click()
    ageSets = agePart.find_elements(by=By.XPATH, value='//div/div/div[3]/select')
    kidNO = 0
    for oneSet in ageSets:
        oneSet.click()
        sleep(randint(1, 2))

        age = agesKids[kidNO]
        ageList = oneSet.find_elements(by=By.CSS_SELECTOR, value="option")
        for option in ageList[age + 1:age + 2]:
            option.click()
            logging.info(f"SELECT - AGE {age}")
            sleep(randint(2, 3))

        kidNO += 1

    logging.info("AGES ADDED")
################################################################################################
# Search
search = findElementByCssAndClick(browser, '#frm div.xp__button button')
sleep(randint(5, 8))
logging.info("SEARCH - DONE")
if 'Map' in browser.current_url:
    checkMap()
################################################################################################
# Sort
try:
    sortPart = findElementByXpath(browser, '//*[@id="right"]/div[1]/div/div/div/span/button')
    sortPart.click()
    sortAll = findElementByXpathAndClick(browser, '//button[@data-id="class_and_price"]')
except:
    try:
        sortPart = browser.find_elements(by=By.XPATH, value='//div[1]/div/div/div[2]/ul/li')
        for oneSort in sortPart:
            innerHtml = oneSort.get_attribute('innerHTML')
            if str(sortIN) in str(innerHtml):
                link = oneSort.find_element(by=By.CSS_SELECTOR, value='a')
                browser.get(link.get_attribute('href'))
                sleep(randint(1, 2))
                break
    except:
        sortPart = findElementByXpath(browser, '//button[@data-testid="sorters-dropdown-trigger"]')
        sortAll = findElementByXpathAndClick(browser, '//a[@data-id="class_and_price"')
        setPriceFilter = findElementByXpathAndClick(browser,
                                                    f'//div[@data-testid="filters-group-label-content"][text()="{sortIN}"]')
if "Map" in browser.current_url:
    checkMap()
################################################################################################
# Filters
allFilters = browser.find_elements(by=By.XPATH, value=f'//div[@data-testid="filters-group-label-content"]')
for oneFilter in filterList:
    for onePosibleFilter in allFilters:
        try:
            filterInner = onePosibleFilter.text
        except:
            continue

        if oneFilter in str(filterInner):
            setFilter = findElementByXpath(browser,
                                           f'//div[@data-testid="filters-group-label-content"][text()="{oneFilter}"]')
            setFilter.click()
            logging.info(f'CLICK FILTER {oneFilter}')
            sleep(randint(2, 4))
            break

logging.info('SELECTED - Filters')
################################################################################################
# Range Price
currentURL = browser.current_url
URL = currentURL.replace('&sb=1', '').replace('&src_elem=sb', '').replace('#map_opened', '')
editedURL = f'{currentURL}&nflt=price%3DUSD-{priceMin}-{priceMax}-1'
browser_get(editedURL, 'body', 3)
if 'map_opened' in str(editedURL):
    checkMap()
logging.info("PRICE RANGED")
################################################################################################
# Products
allProducts = browser.find_elements(by=By.XPATH, value='//div[@data-testid="property-card"]')
for oneProduct in allProducts[0:10]:
    Name = oneProduct.find_element(by=By.XPATH, value='//div[@data-testid="title"]').text
    Price = oneProduct.find_element(by=By.XPATH, value='//div[@data-testid="price-and-discounted-price"]').text
    ScoreAndeRevies = oneProduct.find_element(by=By.XPATH, value='//div[@data-testid="review-score"]')
    NumberOfReviews = ScoreAndeRevies.find_element(by=By.CSS_SELECTOR, value='div:nth-child(1)').text
    Score = ScoreAndeRevies.find_element(by=By.CSS_SELECTOR, value='div:nth-child(2)').text
    Location = oneProduct.find_element(by=By.XPATH, value='//div[@data-testid="location"]').text
    ImageURL = oneProduct.find_element(by=By.XPATH, value='//img[@data-testid="image"]').get_attribute('src')
    print(f"Name: {Name}")
    print(f"Price: {Price}")
    print(f"NumberOfReviews: {NumberOfReviews}")
    print(f"Score: {Score}")
    print(f"Location: {Location}")
    print(f"ImageURL: {ImageURL}")
    logging.info(f"Name: {Name}, Price: {Price}, NumberOfReviews: {NumberOfReviews}, Score: {Score}, Location: {Location}, ImageURL: {ImageURL}")

browser.quit()
logging.info("CODE FINISH SUCCESSFULLY")
