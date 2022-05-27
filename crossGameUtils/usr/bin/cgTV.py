#/bin/python3

#apt install chromium-chromedriver

from selenium import webdriver
from tv.rtveTV import rtveTV

if __name__ == "__main__":
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--kiosk")
    chrome_options.add_argument("--window-position=0,0")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(chrome_options=chrome_options)
    a = rtveTV(driver)
    a.setChannel("https://www.rtve.es/play/videos/directo/la-1/")