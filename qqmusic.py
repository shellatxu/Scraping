import time
import pymysql
import requests
import re,sys
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json,random
from seleniumwire import webdriver 
from seleniumwire.utils import decode
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

if len(sys.argv) >= 2:
    singer = sys.argv[1]
else:
    sys.exit()

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("disable-extensions")
options.add_argument("--ignore-certificate-errors");

service = Service(executable_path=r'./chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options) 
driver.maximize_window()

url = 'https://y.qq.com/n/ryqq/singer/00220AYa4Ohak5'
driver.get(url)
time.sleep(5)
#
driver.find_element(By.XPATH, "//*[@id=\"app\"]/div/div[1]/div/div[1]/div[1]/input").send_keys(singer)
#driver.find_element(By.XPATH, "//*[@id=\"app\"]/div/div[1]/div/div[1]/div[1]/button").click()
time.sleep(5)
for request in driver.requests:
    if ('smartbox_new' in request.url) :
        singer_search = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
        singer_search_obj = json.loads(singer_search)

try:
    singer_mid = singer_search_obj['data']['singer']['itemlist'][0]['mid']
except:
    singer_mid = 0
if singer_mid == 0 :
    print("not found")
    sys.exit()
    
url = 'https://y.qq.com/n/ryqq/singer/'+singer_mid
session = requests.session()        
res = session.get(url=url, timeout=(30,30))

title = re.findall('<span class="songlist__songname_txt"><a title="([^<]*)" href="([^<]*)">([^<]*)</a></span>',res.text)

if title:
    for item in title:
        item_title = item[0]
        url = 'https://y.qq.com'+item[1]
        driver.get(url)
        time.sleep(5)
        
        song_info = re.findall('<li class="data_info__item_song">流派：<!-- -->([^<]*) </li><li class="data_info__item_song">发行时间：<!-- -->([^<]*) </li>',driver.page_source)
        if song_info:
            genre = song_info[0][0]
            release_date = song_info[0][1]
        else:
            genre = ""
            release_date = ""
        
        for request in driver.requests:
            if ('musics.fcg' in request.url) :
                song_comment = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
        song_comment_obj = json.loads(song_comment)
        try:
            song_comment_count = song_comment_obj['req_2']['data']['response_list'][0]['count']
        except:
            song_comment_count = 0
                   
        song_item = [item_title, singer_mid, title[0][0], release_date,url,genre, song_comment_count]
        print(song_item)

