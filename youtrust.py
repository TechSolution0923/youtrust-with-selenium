from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import csv

def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox") # linux only    
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless=new") # for Chrome >= 109
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")

    service=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://youtrust.jp/sign_in?type=sign_in")

    WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.ID, "react-application"))
    )

    login_youtrust(driver)
    time.sleep(10)

    f = open('user_1.xml','r')
    xml_content = f.readlines()
    for item in xml_content:
        member_urls = re.findall('>(https:\/\/.+)<',item)
        for member_url in member_urls:
            driver.get(member_url)

            results = []
            company = fetch_company(driver)
            company_url = fetch_company_url(driver)
            member_name = fetch_name(driver)
            role = fetch_role(driver)
            article = fetch_article(driver, member_name)

            insert_data = {
                "company": company,
                "company_url": company_url,
                "member_name": member_name,
                "member_url": member_url,
                "role": role,
                "article": article
            }
            results.append(insert_data)
            print(insert_data)

def login_youtrust(driver):
    email_box = driver.find_element(By.NAME, "database_authentication[email]")
    email_box.send_keys("dataops017@gmail.com")

    pass_box = driver.find_element(By.NAME, "database_authentication[password]")
    pass_box.send_keys("Sumasuma0713")

    login_button = driver.find_element(By.CLASS_NAME, "yt-MuiButton-containedPrimary")
    login_button.click()

def fetch_name(driver):
    name = ''
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'enDHzd'))
        )
        name = driver.find_element(By.CLASS_NAME, 'enDHzd').text
    except:
        print("Error: Fetch Failed Name")
    return name

def fetch_role(driver):
    role = ''
    try:
        role = driver.find_element(By.CSS_SELECTOR, '.sc-gKXOVf.cXRWOT p.bVUllJ').text
    except:
        print("Error: Fetch Failed role")
    return role

def fetch_company(driver):
    company = ''
    try:
        company = driver.find_element(By.CSS_SELECTOR, 'p.bVUllJ:nth-of-type(1)').text
    except:
        print("Error: Fetch Failed Company")
    return company

def fetch_company_url(driver):
    company_url = ''
    try:
        company_url = driver.find_element(By.CSS_SELECTOR, 'div.gvsgxA > div.dCyIBY > a').get_attribute('href')
    except:
        print("Error: Fetch Failed Company Url")
    return company_url

def fetch_article(driver, member_name):
    article = []
    try:
        tab_button = driver.find_element(By.CSS_SELECTOR, "button.yt-MuiTab-root:nth-of-type(3)")
        tab_button.click()

        sel = Selector(text = driver.page_source)
        
        for item in sel.xpath("//div[contains(@class, 'iqbWMm')] / div / div[contains(@class, 'cdppzg')] / div[contains(@class, 'sc-bczRLJ')]"):
            article.append({
                'publish_date' : item.css('p.kuJsjV::text').get(),
                'author' : item.css('div.sc-gKXOVf.cdppzg p.jtrTuS::text').get(),
                'url' : "https://youtrust.jp" + item.css('a::attr(href)').get(),
                'title' : member_name + "さんの紹介コメント",
            })
    except:
        print("Error: Fetch Failed Company Url")
    
    return article

if __name__ == '__main__':
    main()