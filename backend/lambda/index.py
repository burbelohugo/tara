from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from env import USER_EMAIL, USER_PASSWORD
PAGE_BASE_URL = "https://esjbooked.umd.edu/Web/index.php?redirect="


def handler(event, context):
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome('/opt/chromedriver',chrome_options=options)

    driver.get(PAGE_BASE_URL)
    body = f"Headless Chrome Initialized, Page title: {driver.title}"

    inputElement = driver.find_element_by_id("email")
    inputElement.send_keys(USER_EMAIL)

    inputElement = driver.find_element_by_id("password")
    inputElement.send_keys(USER_PASSWORD)

    driver.find_element_by_css_selector('#login-box > div:nth-child(5) > button').click()

    body = {
        "result": driver.find_element_by_id("schedule-title").get_attribute('innerHTML')
    }

    driver.close()
    driver.quit()

    response = {
        "statusCode": 200,
        "body": body
    }

    return response

