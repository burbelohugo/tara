from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import datetime
import time
import json

from env import USER_EMAIL, USER_PASSWORD


PAGE_BASE_URL = "https://esjbooked.umd.edu/Web/index.php?redirect="
PAGE_NAV_URL = "https://esjbooked.umd.edu/Web/schedule.php?sd="
AVAILABILTY_SEARCH_URL = "https://esjbooked.umd.edu/Web/search-availability.php"
DAYS_IN_ADVANCE = 10
DEFAULT_MEETING_LENGTH = 60
DESIRED_START_TIME = "9:00 AM -"
DEFAULT_EVENT_TITLE = "CMSC351 Study Group"
DEFAULT_EVENT_DESCRIPTION = "Study for CMSC351"

def handler(event, context):
    print(json.dumps(event))

    # Setup selenium webdriver
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome('/opt/chromedriver',chrome_options=options)

    # Navigate to base page with proper date preset
    driver.get(AVAILABILTY_SEARCH_URL)

    # Enter email
    inputElement = driver.find_element_by_id("email")
    inputElement.send_keys(USER_EMAIL)

    # Enter password
    inputElement = driver.find_element_by_id("password")
    inputElement.send_keys(USER_PASSWORD)

    # Click login button
    driver.find_element_by_css_selector('#login-box > div:nth-child(5) > button').click()

    # Enter desired time
    inputElement = driver.find_element_by_id("minutes")
    inputElement.clear()
    inputElement.send_keys(DEFAULT_MEETING_LENGTH)

    # Select custom date range
    driver.find_element_by_css_selector('#searchForm > div:nth-child(5) > div.btn-group.margin-bottom-15 > label:nth-child(4)').click()

    # Enter desired date range
    inputElement = driver.find_element_by_id("beginDate")
    inputElement.send_keys(calculateDate(DAYS_IN_ADVANCE))

    inputElement = driver.find_element_by_id("endDate")
    inputElement.send_keys(calculateDate(DAYS_IN_ADVANCE + 1))

    # Click submit
    submitButton = driver.find_element_by_css_selector("#searchForm > div:nth-child(8)")
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(submitButton, 100, 0)
    action.click()
    action.perform()

    # Wait a few seconds for results to load
    time.sleep(3)

    availableSlots = driver.find_elements_by_class_name("dates")
    goodSlots = []

    # Click on first ideal slot
    for slot in availableSlots:
        if DESIRED_START_TIME in slot.get_attribute('innerHTML'):
            goodSlots.append(slot.get_attribute('innerHTML'))
            slot.click()
            break

    inputElement = driver.find_element_by_id("reservationTitle")
    inputElement.send_keys(DEFAULT_EVENT_TITLE)

    inputElement = driver.find_element_by_id("description")
    inputElement.send_keys(DEFAULT_EVENT_DESCRIPTION)

    # Submit
    driver.find_element_by_css_selector("#form-reservation > div:nth-child(9) > div > div > button.btn.btn-success.save.create.btnCreate").click()

    body = {
        "result": calculateDate(DAYS_IN_ADVANCE)
    }

    # Cleanup
    driver.close()
    driver.quit()

    response = {
        "statusCode": 200,
        "body": json.dumps({"req": "finished"})
    }

    return response

def calculateDate(offsetDays):
    # Add a certain number of days to the current date
    currentDate = datetime.datetime.now() + datetime.timedelta(days=offsetDays)
    return currentDate.strftime("%m/%d/%Y")
