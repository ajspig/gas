import json
import io
import boto3
import pandas as pd
from tempfile import mkdtemp
from datetime import datetime
from io import StringIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def handler(event, context):
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = '/opt/chrome/chrome'
    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(options=options, service=service)
    driver.get("https://gasprices.aaa.com/?state=NY")

    #get all county elements
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fm-map-container > svg > g > g > g")))
    counties = driver.find_elements(By.CSS_SELECTOR, ".fm-map-container > svg > g > g > g > path")

    #get each county's name and price
    ret = None
    for el in counties:
        hover = ActionChains(driver).move_to_element(el)
        hover.perform()
        county = driver.find_element(By.CSS_SELECTOR, ".fm-tooltip-name")
        price = driver.find_element(By.CSS_SELECTOR, ".fm-tooltip-comment")
        if county.text.lower() == "new york":
            ret = {county.text: price.text}
            break
    
    if ret != None:
        #update data in s3
        s3 = boto3.resource('s3')
        date = datetime.today().strftime('%Y-%m-%d')

        data = pd.read_csv("https://452-data.s3.us-west-1.amazonaws.com/nyc_gas_price.csv")
        data = pd.concat([pd.DataFrame([[date, price]], columns=data.columns), data], ignore_index=True)

        csv_buffer = StringIO()
        data.to_csv(csv_buffer, index = False)
        s3.Object('452-data', 'nyc_gas_price.csv').put(Body=csv_buffer.getvalue())

        return {
            'statusCode': 200,
            'body': json.dumps(ret)
        }
    
    else:
        return {
            'statusCode': 501
        }
