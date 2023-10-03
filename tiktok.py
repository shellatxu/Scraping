import time,datetime
import requests
import re,os 
from selenium import webdriver
from selenium.webdriver.common.by import By
import json,random,sys
from seleniumwire import webdriver 
from seleniumwire.utils import decode
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin


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

        
filename = "xhs_demo.csv"
output_file = open(filename, "a" ,encoding='utf-8')
if os.path.exists(filename) is not True :
    output_file.write("nickname, max_id, poster_id, following ,followers,bio,poster_posts, total_followers_screen,videos_this_week\n")    

url = 'https://www.tiktok.com/foryou'
driver.get(url)
time.sleep(5)

item = driver.find_elements(By.XPATH, '//*[@data-e2e="modal-close-inner-button"]')
item[0].click()

homefeed_body = ''
comment_body = ''
while True:

    del driver.requests
    driver.execute_script("window.scrollTo(0, -100);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('Scrolling %s'%time.ctime())   
    time.sleep(5) 
            
    for request in driver.requests:
        if ('api/recommend' in request.url) :
            homefeed_body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
        
    homefeed_obj = json.loads(homefeed_body)
    for post_item in homefeed_obj['itemList']:
        author = post_item['author']
        author_stats = post_item['authorStats']
        author_data = {}
        author_data['nickname'] = author['nickname']
        author_data['max_id'] = '0'
        author_data['poster_id'] = str(author['id'])
        author_data['following'] = str(author_stats['followingCount'])
        author_data['followers'] = str(author_stats['followerCount'])
        author_data['bio'] = str(author_stats['heart'])
        author_data['poster_posts'] = str(author_stats['videoCount'])
        author_data['diggCount'] = str(author_stats['diggCount'])
        print(author_data)
        line = ','.join(list(author_data.values()))+"\n"
        output_file.write(line)
