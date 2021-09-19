from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from creds import USERNAME, PASSWORD
from settings import URL, PHRASES, CHROME_BINARY
from logger import Logger
import time

class Scrapper:
    def __init__(self):
        self.logger = Logger()
        self.logger.log("New instance of Scrapper created")
        if not CHROME_BINARY:
            driver = webdriver.Chrome("./chromedriver.exe")
        else:
            options = Options()
            options.binary_location = CHROME_BINARY
            driver = webdriver.Chrome(chrome_options=options, executable_path="./chromedriver.exe")
        driver.get(URL)
        self.browser = driver
        self.login_and_open_table()

    def login_and_open_table(self):
        self.browser.find_element_by_id("Username").clear()
        self.browser.find_element_by_id("Username").send_keys(USERNAME)
        self.browser.find_element_by_id("Password").clear
        self.browser.find_element_by_id("Password").send_keys(PASSWORD)
        self.browser.find_element_by_id("Password").send_keys(Keys.RETURN)
        self.browser.find_element_by_xpath("//a[@href=\"/EmployeeOnlineHealth/GSTTLIVE/Roster/BankShifts\"]").click()
        self.logger.log("Scrapper authenticated on site")

    def find_shifts(self):
        shifts = []
        next_btn = self.browser.find_element_by_id("btnNext")
        is_active = not("disabled" in next_btn.get_attribute("class"))
        while True:
            try:
                rows = WebDriverWait(self.browser, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id=\"grid\"]/tbody/tr")))         
                for row in rows:
                    shift = self.read_row(row)
                    if shift != "n/a":
                        shifts.append(shift)
            except TimeoutException:
                self.logger.log("No rows found on table page")
            if is_active:
                next_btn.click()
                next_btn = self.browser.find_element_by_id("btnNext")
                is_active = not("disabled" in next_btn.get_attribute("class"))
                time.sleep(3)
            else:
                self.logger.log("Reached end of table")
                break
        return shifts


    def read_row(self, row):
        day = row.find_element_by_xpath("./td[2]").text
        grade = row.find_element_by_xpath("./td[11]").text
        if (day in PHRASES) and (grade in PHRASES):
            message = ("Day: " + day + "\n"
                        "Date: " + row.find_element_by_xpath("./td[3]").text + "\n"
                        "Time: " + row.find_element_by_xpath("./td[4]").text + "\n"
                        "Unit: " + row.find_element_by_xpath("./td[7]").text + "\n"
                        "Grade: " + grade + "\n")
            self.logger.log("Shift found:")
            self.logger.log(message)
            return message
        return "n/a"
            # row.find_element_by_xpath("./td[16]").click()
            # try:
            #     confirm_button =  WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ui-button-text")))
            #     print(confirm_button.text)
            # except TimeoutException:
            #     self.logger.log("Error - confirm btn not found")
            

    
    def close(self):
        self.logger.log("Scrapper done, browser closing")
        self.browser.close()