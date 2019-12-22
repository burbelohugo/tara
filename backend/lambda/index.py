from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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

    driver.close();
    driver.quit();

    response = {
        "statusCode": 200,
        "body": body
    }

    return response

