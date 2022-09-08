from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://safe.density.io/#/displays/dsp_956223069054042646?token=shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e'

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)


def retrieve():
    driver.get(url)
    wait.until(presence_of_element_located((By.ID, "root")))
    root = driver.find_element(By.ID, "root")

    if root is not None:
        print("Root found")
    else:
        print("Root not found. Process timed out.")

    wait.until(presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[1]/div[2]/div/span')))
    target = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[2]/div/span')

    if target is not None:
        print("Target found: " + target.text)
    else:
        print("Target not found. Process timed out.")

    # driver.quit()
    return target.text
