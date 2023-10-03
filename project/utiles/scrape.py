import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from datetime import datetime


async def scraper(location, industry, job_title):
    options = webdriver.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(use_subprocess=False, options=options)
    driver.get('https://www.google.com/maps')
    action = ActionChains(driver)
    search_elem = WebDriverWait(driver, 10)\
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, "#searchboxinput")))
    action.move_to_element(search_elem).click().perform()
    search_elem.send_keys(f"{job_title} companies of {industry} industry in {location}")
    action.send_keys(Keys.ENTER).perform()
    result_elem = WebDriverWait(driver, 10)\
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label^='Results']")))
    start_time = datetime.now().timestamp()
    while datetime.now().timestamp() - start_time < 100:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", result_elem)
        try:
            WebDriverWait(driver, 0.1)\
                .until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label^='Results'] > div > div > p > span")))
            break
        except TimeoutException:
            pass
    link_elems = WebDriverWait(driver, 10)\
                .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[aria-label^="Results"] > div > div > a')))
    print(len(link_elems))
    driver.quit()
    return
