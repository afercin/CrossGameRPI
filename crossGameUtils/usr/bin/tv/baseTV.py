from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


class tv:
    COOKIES = ""
    READY = ""

    def __init__(self, driver):
        self.driver = driver
        self.firstTime = True

    def findElement(self, xpath, count=1):
        print(f"[INFO] Trying to find element: {xpath}")
        if self.isElementVisible(xpath):
            print(f"[ OK ] Find element: {xpath}")
            return self.driver.find_element(By.XPATH, xpath)
        elif count < 5:
            count += 1
            self.findElement(xpath, count)

        print(f"[WARN] Can not find element: {xpath}")
        return None

    def isElementVisible(self, xpath):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except:
            return False

        return True

    def clickElement(self, xpath):
        element = self.findElement(xpath)
        if element != None:
            time.sleep(0.25)
            print(f"[ OK ] Click element: {xpath}")
            element.click()

    def setChannel(self, url):
        done = False
        times = 0
        while times < 3 and not done:
            print(f"[INFO] Setting url: {url}")
            try:
                self.driver.get(url)
                if self.COOKIES and self.firstTime:
                    while not self.isElementVisible(self.COOKIES):
                        pass

                    time.sleep(0.5)
                    self.clickElement(self.COOKIES)
                    self.firstTime = False

                if self.READY:
                    while not self.isElementVisible(self.READY):
                        pass
                done = True
            except:
                times += 1
                time.sleep(0.5)
