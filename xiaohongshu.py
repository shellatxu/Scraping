import time
import pymysql
import requests
import re
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json,random
from seleniumwire import webdriver 
from seleniumwire.utils import decode
import csv

def scrape_xhs_fashion():
    url = 'https://www.xiaohongshu.com/explore?channel_id=homefeed.fashion_v3'
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("disable-extensions")

    driver = webdriver.Chrome('./chromedriver.exe',options=options)  

    driver.maximize_window()
    driver.get(url)
    homefeed_body = ''
    time.sleep(5)
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('Scrolling %s'%time.ctime())
        time.sleep(random.randrange(5,10))  
        try:
            for request in driver.requests:
                if ('homefeed' in request.url):
                    homefeed_body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))

            obj = json.loads(homefeed_body)    
            if obj['success'] is True:
                for item in obj['data']['items']:
                    with open('xhs_fashion.csv', 'a', newline='',encoding='utf-8') as csvfile:
                        fieldnames = ['poster_id', 'post_id','post_title','poster_nickname','liked_count']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow({'poster_id': item['note_card']['user']['user_id'], 'post_id': item['id'],'post_title':item['note_card']['display_title'],'poster_nickname':item['note_card']['user']['nickname'],'liked_count':item['note_card']['interact_info']['liked_count']})
        except:
            pass
            
            
if __name__ == "__main__": 
    scrape_xhs_fashion()
            
            
            
            
