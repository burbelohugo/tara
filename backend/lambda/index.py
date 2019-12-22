from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from env import USER_EMAIL, USER_PASSWORD
PAGE_BASE_URL = "https://esjbooked.umd.edu/Web/index.php?redirect="
PAGE_NAV_URL = "https://esjbooked.umd.edu/Web/schedule.php?sd=2019-12-30"

def handler(event, context):
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome('/opt/chromedriver',chrome_options=options)

    driver.get(PAGE_NAV_URL)
    body = f"Headless Chrome Initialized, Page title: {driver.title}"

    inputElement = driver.find_element_by_id("email")
    inputElement.send_keys(USER_EMAIL)

    inputElement = driver.find_element_by_id("password")
    inputElement.send_keys(USER_PASSWORD)

    driver.find_element_by_css_selector('#login-box > div:nth-child(5) > button').click()

    # Navigate to the right week
    # driver.get(PAGE_NAV_URL)

    body = {
        "result": driver.find_element_by_css_selector(".schedule-dates").get_attribute('innerHTML')
    }

    driver.close()
    driver.quit()

    response = {
        "statusCode": 200,
        "body": body
    }

    return response

