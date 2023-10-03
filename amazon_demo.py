import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumwire import webdriver 
from seleniumwire.utils import decode
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.keys import Keys

def add_product_to_cart(url, keyword):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("user-data-dir=/home/shell/.config/google-chrome/")
    options.add_argument("profile-directory=Default")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging"]) 
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("disable-extensions")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('–log-level=3')
    #options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    driver.get(url)
    time.sleep(5)

    try:
        driver.find_elements(By.XPATH, '//*[@id="sp-cc-accept"]')[0].click()
    except:
        print('not found accept cookie button')        
        
    try:
        driver.find_elements(By.XPATH, '//*[@id="twotabsearchtextbox"]')[0].send_keys(keyword)
        driver.find_elements(By.XPATH, '//*[@id="twotabsearchtextbox"]')[0].send_keys(Keys.ENTER)
    except:
        print('not found search input')
    try:
        driver.find_elements(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/h2/a')[0].click()
    except:
        print('not found search result')    
    
    try:
        driver.find_elements(By.XPATH, '//*[@id="add-to-cart-button-ubb"]')[0].click()
    except:
        print('not found add to cart button')      


if __name__ == "__main__":
    start_url = 'https://www.amazon.co.uk/'
    keyword = 'iphone'
    add_product_to_cart(start_url, keyword)