import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import os

class Scraper:

    dictionary = {
        'en': {
            'result': 'Results',
            'information': 'Information',
        },
        'ru': {
            'result': 'Результаты',
            'information': 'Информация',
        }
    }

    def __init__(self, driver = None, language = 'en', wait = 10):
        self.driver = driver
        self.language = language
        self.result_data = []
        self.history_data = {}
        self.filter_text = ''
        self.element_wait_timeout = wait
    
    def create_driver(self, headless = False, profile_num = 0):
        if self.driver is not None:
            self.del_driver()
        options = webdriver.ChromeOptions()
        options.headless = headless
        if headless:
            options.add_argument('--headless')
        if profile_num:
            if os.name == 'nt':
                user_data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
            else:
                user_data_dir = os.path.join(os.path.expanduser('~'), '.config', 'google-chrome')
            options.add_argument(f'--user-data-dir={user_data_dir}')
            if not os.path.exists(os.path.join(user_data_dir, "Profile ", str(profile_num))):
                options.add_argument(f'--profile=Profile {str(profile_num)})')    
            else:
                options.add_argument(f'--profile=Default')
        self.driver = uc.Chrome(use_subprocess=False, options=options)
        self.driver.maximize_window()

    def check_lang_location(self, test_url = 'https://www.google.com/maps'):
        if self.driver is None:
            print("Driver is not created")
            return
        self.driver.get(test_url)
        site_language = self.driver.execute_script("return document.documentElement.getAttribute('lang');")
        if 'en' in site_language:
            self.language = 'en'
        elif 'ru' in site_language:
            self.language = 'ru'
        else:
            self.language = 'en'

    def get_language(self):
        return self.language

    def del_driver(self):
        if self.driver is not None:
            self.driver.quit()

    def start_scraping(self, location, industry, job_title, limit=None):
        self.filter_text = f"{location}-{industry}-{job_title}"
        if self.driver is None:
            print("Driver is not created")
            return 500 # Driver is not created
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get('https://www.google.com/maps')
        action = ActionChains(self.driver)
        try:
            search_elem = WebDriverWait(self.driver, self.element_wait_timeout) \
                .until(EC.presence_of_element_located((By.CSS_SELECTOR, "#searchboxinput")))
        except:
            print("Bad network connection")
            return 400 # Bad network connection
        action.move_to_element(search_elem).click().perform()
        search_elem.send_keys(f"{job_title} companies of {industry} industry in {location}")
        action.send_keys(Keys.ENTER).perform()
        try:
            search_elem = WebDriverWait(self.driver, self.element_wait_timeout) \
                .until(EC.presence_of_element_located((By.CSS_SELECTOR, "#searchbox-searchbutton")))
            search_elem.click()
        except:
            print("Bad network connection")
            return 400 # Bad network connection
        try:
            result_elem = WebDriverWait(self.driver, self.element_wait_timeout) \
                .until(EC.presence_of_element_located((By.CSS_SELECTOR, f"div[aria-label^='{self.dictionary[self.language]['result']}']")))
        except: 
            print("Result not found")
            return 404 # Result not found
        start_t = datetime.now().second
        link_elems = []
        while datetime.now().second - start_t < 60:
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", result_elem)
            link_elems = WebDriverWait(self.driver, self.element_wait_timeout) \
                    .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'div[aria-label^="{self.dictionary[self.language]["result"]}"] > div > div > a')))
            if limit and len(link_elems) >= limit:
                break
            try:
                WebDriverWait(self.driver, self.element_wait_timeout) \
                    .until(EC.presence_of_element_located((By.CSS_SELECTOR, f"div[aria-label^='{self.dictionary[self.language]['result']}'] > div > div > p > span")))
                break
            except TimeoutException:
                pass
        
        print(f"Found {len(link_elems)} results")
        urls = []
        for link_elem in link_elems:
            urls.append(link_elem.get_attribute('href'))
            if limit and len(urls) >= limit:
                break

        for url in urls:
            self.driver.get(url)
            action = ActionChains(self.driver)
            try:
                WebDriverWait(self.driver, self.element_wait_timeout) \
                    .until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='main']")))
            except:
                print("Bad network connection")
                return 400 # Bad network connection
            try:
                elem = WebDriverWait(self.driver, self.element_wait_timeout) \
                    .until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="main"] > div:nth-child(2) h1')))
                company_name = elem.text.strip()
            except:
                company_name = "Not Found"
            if company_name != "Not Found" and company_name in self.history_data.get(self.filter_text, []):
                continue
            try:
                elem = WebDriverWait(self.driver, self.element_wait_timeout) \
                    .until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="main"] > div:nth-child(2) button')))
                company_category = elem.text.strip()
            except:
                company_category = "Not Found"
            elems = WebDriverWait(self.driver, self.element_wait_timeout) \
                .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'div[role="main"] > div[aria-label^="{self.dictionary[self.language]["information"]}"] > div > button')))
            company_address = "Not Found"
            company_country = "Not Found"
            company_zip = "Not Found"
            company_phone = "Not Found"
            company_state = "Not Found"
            company_city = "Not Found"
            for elem in elems:
                try:
                    img = elem.find_element(By.CSS_SELECTOR, 'img')
                    if img.get_attribute('src').find("place") >= 0: 
                        company_location = elem.text.strip()
                        company_loc_info = company_location.split(",")
                        company_address = company_loc_info[0].strip()
                        company_country = company_loc_info[-1].strip()
                        company_zip_info = company_loc_info[-2].strip().split(" ", 1)
                        if len(company_zip_info) == 2:
                            company_zip = company_zip_info[1]
                    elif img.get_attribute('src').find("phone") >= 0: 
                        company_phone = elem.text.strip()
                    elif img.get_attribute('src').find("ic_plus") >= 0: 
                        company_state_info = elem.text.strip().split(" ", 1)
                        if len(company_state_info) == 2:
                            company_city = company_state_info[1].split(", ")[0]
                            company_state = company_state_info[1].split(", ")[1]
                except:
                    pass
            try:
                elem = WebDriverWait(self.driver, self.element_wait_timeout) \
                    .until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[role="main"] > div[aria-label^="{self.dictionary[self.language]["information"]}"] > div > a')))
                company_website = elem.text.strip()
            except:
                company_website = "Not Found"
            self.result_data.append({
                "company": company_name,
                "website": company_website,
                "linkedin_comp": "Not Found",
                "phone": company_phone,
                "address": company_address,
                "state": company_state,
                "city": company_city,
                "category": company_category,
                "code": company_zip,
                "country": company_country,
                "fname": "Not Found",
                "lname": "Not Found",
                "title": "Not Found",
                "email": "Not Found",
                "linkedin_pers": "Not Found",
            })
        for i in range(len(self.result_data)):
            self.driver.get('https://dashboard.lusha.com/dashboard')
            action = ActionChains(self.driver)
            data = self.result_data[i]
            try:
                search_elem = WebDriverWait(self.driver, self.element_wait_timeout) \
                    .until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-test-id="search-input-field"]')))
            except:
                print("Maybe Not Logged in Lusha")
                break
                # return 201 
            action.move_to_element(search_elem).click().perform()
            search_elem.clear()
            search_elem.send_keys(f"{data['website']}")
            # action.send_keys(Keys.ENTER).perform()
            try:
                search_elem = WebDriverWait(self.driver, self.element_wait_timeout) \
                    .until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="search-item-company-0"] span[class*="DescriptionContainer"] div[class*="StyledEllipsisTextContainer"]')))
                if data['website'] in search_elem.text:
                    search_elem.click()
                else:
                    raise Exception("Company Website not found")
            except:
                print("Company Website not found")
                continue
            try:
                WebDriverWait(self.driver, self.element_wait_timeout) \
                    .until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="decision-makers"] div[data-test-id*="contact-0"] > div')))
                elems = WebDriverWait(self.driver, self.element_wait_timeout) \
                    .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-test-id="decision-makers"] div[data-test-id*="contact-0"] > div')))
                if len(elems) == 0:
                    raise Exception("Director not found")
                else:
                    try:
                        full_elem = elems[0].find_element(By.CSS_SELECTOR, 'div[class*="StyledContactInfoFullName"]')
                        fullname = full_elem.text.strip().split(" ")
                        self.result_data[i]["fname"] = fullname[0].strip()
                        self.result_data[i]["lname"] = fullname[-1].strip()
                    except:
                        print("Full name not found")
                    try:
                        title_elem = elems[0].find_element(By.CSS_SELECTOR, 'div[data-for*="job-title"]')
                        self.result_data[i]["title"] = title_elem.text.strip()
                    except:
                        print("Title not found")
                    try:
                        email_elem = elems[1].find_element(By.CSS_SELECTOR, 'div[data-for*="email"]')
                        self.result_data[i]["email"] = email_elem.get_attribute('data-for').split("-", 1)[1].strip()
                    except:
                        print("Email not found")
            except:
                print("Director not found")
            try:
                linkedin_elem = WebDriverWait(self.driver, self.element_wait_timeout) \
                    .until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="StyledDomainAndLinkedin-company-page"] div[class*="StyledLinkedinIcon-company-page"]')))
                linkedin_elem.click()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                if 'linkedin.com' in self.driver.current_url:
                    self.result_data[i]["linkedin_comp"] = self.driver.current_url
                    self.driver.close() 
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                print("Company Linkedin Link not found")
            try:
                linkedin_elem = WebDriverWait(self.driver, self.element_wait_timeout) \
                    .until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="decision-makers"] div[data-test-id*="contact-0"] > div div[class*="StyledContactInfoLinkedinLink"]')))
                linkedin_elem.click()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                if 'linkedin.com' in self.driver.current_url:
                    self.result_data[i]["linkedin_pers"] = self.driver.current_url
                    self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                print("Director Linkedin Link not found")
        
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return 200

    def add_to_history(self, company_name):
        if self.filter_text not in self.history_data:
            self.history_data[self.filter_text] = []
        self.history_data[self.filter_text].append(company_name)

    def open_new_window(self, url=""):
        if self.driver:
            self.driver.execute_script("window.open('{0}');", url)
            self.driver.switch_to.window(self.driver.window_handles[-1])

    def get_result_data(self):
        return self.result_data
    
    def get_history(self):
        return self.history_data

    def is_driver_quitted(self):
        if self.driver.service.process is None:
            return True
        else:
            return False
    
    def quit_driver_process(self):
        if self.driver.service.process is not None:
            try:
                self.driver.service.process.terminate()
                return True
            except:
                return False
        else:
            return True

    def remove_all_chrome_process(self):
        try:
            os.system("taskkill /f /im chrome.exe")
            return True
        except:
            return False

    def clear_result_data(self):
        self.result_data = []
    
    def clear_history(self):
        self.history_data.clear()

scraper = Scraper(wait=10)
