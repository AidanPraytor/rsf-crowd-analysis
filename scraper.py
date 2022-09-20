#!/usr/bin/env python3
"""Scraping portion of project. Conducts scrape of RSF Crowd Meter website and returns target data."""
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
import re

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 30)

crowdMeter = 'https://safe.density.io/#/displays/dsp_956223069054042646?token' \
             '=shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e '

driver.get(crowdMeter)
wait.until(presence_of_element_located((By.ID, "root")))
root = driver.find_element(By.ID, "root")


def retrieve():  # got rid of 'url' arg
    """
    Scrapes RSF Crowd Meter website, returns target data.

        Using Selenium Chromedriver, opens a headless browser and isolates 'root' element,
    the parent of target span element, by ID. When 'root' has been found, uses 'root' location
    in HTML tree to find target span by XPATH. In both of these steps, WebDriverWait is used
    to allow JS on webpage to load before attempting to locate invisible elements. If either
    element takes longer than 10 seconds to find, timeout message is printed and System exits 1.

    :param url: url of RSF Crowd Meter tool
    :return str: .text attribute of targeted span
    """
    try:

        """        
        driver.get(crowdMeter)
        wait.until(presence_of_element_located((By.ID, "root")))
        root = driver.find_element(By.ID, "root")
        """

        if root is not None:
            print("Root found")
        else:
            print("Root not found. Process timed out.")
            driver.quit()  # may cause problems, not sure yet
            SystemExit(1)

        wait.until(presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[1]/div[2]/div/span')))
        target = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[2]/div/span')

        if target is not None:
            print("Target found: " + target.text)
        else:
            print("Target not found. Process timed out.")
            driver.quit()  # may cause problems, not sure yet
            SystemExit(1)
    except selenium.common.exceptions.TimeoutException:
        print("Process timed out.")
        driver.quit()  # may cause problems, not sure yet
        return "null"

    return re.sub("% Full", "", target.text)
