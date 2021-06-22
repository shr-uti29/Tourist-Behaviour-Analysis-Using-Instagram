from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
import requests
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
#"goaadventuretogether","goadiary2018","goadiaries🌴🌊🏖️","goadiaries2018🌴","goa2020❤️","goadiary2020","goa2020🌊☀️","goa2020🏖️","goadiaries2019🌴🌊","goadiaries😎"
#,"goa2018😎","goadiary2018❤️","goavacation🌴","goadiary😍","goa2019🏝","goa2019🌴","goa2019❤️","goadiaries🌴❤️","goadiaries🏖️"
hashtags=["goa2018❤️"]
j=0
result=pd.DataFrame(columns = ['Time','Date','User_id','Full_Name','User_Name','Location_Id','Location_Name','Latitude','Longitude'])
for hashtag in hashtags:
    browser = webdriver.Chrome(executable_path=r'C:\Program Files\webdriver\chromedriver.exe')
    browser.get('https://www.instagram.com/explore/tags/'+hashtag)
    #browser.get("http://www.instagram.com")
    # username = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    # password = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
    # username.clear()
    # username.send_keys("issuesissue")
    # password.clear()
    # password.send_keys("issuesolvesissue")
    # button = WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    # not_now = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    # not_now2 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    #target the search input field
    # searchbox = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    # searchbox.clear()

    #search for the hashtag cat
    # keyword = "#goa2018"
    # searchbox.send_keys(keyword)
    
    # Wait for 5 seconds
    # time.sleep(5)
    # searchbox.send_keys(Keys.ENTER)
    # time.sleep(5)
    # try:
    #     element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "searchbox")))
    # except:
    #     print("ok")
    # searchbox.send_keys(Keys.ENTER)
    # time.sleep(5)
    Pagelength = browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    links=[]
    source = browser.page_source
    data=bs(source, 'html.parser')
    body = data.find('body')
    #print(data.prettify())
    script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
    page_json = script.string.split(' = ', 1)[1].rstrip(';')
    data = json.loads(page_json)
    for link in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
        links.append('https://www.instagram.com'+'/p/'+link['node']['shortcode']+'/')
    print(links)
    print(len(links))
    link1=[]
    for i in links:
        link1.append(i+'?__a=1')
    print(link1)
    #browser.close()

    # j=0
    # result=pd.DataFrame(columns = ['Time','Date','User_id','Full_Name','User_Name','Location_Id','Location_Name','Latitude','Longitude'])
    driver = webdriver.Chrome(executable_path=r'C:\Program Files\webdriver\chromedriver.exe') 
    for i in range(len(link1)):
        flag = 0
        time.sleep(20)
        driver.get(link1[i])  
        html = driver.page_source  
        soup = bs(html, "html.parser")
        all_divs = str(soup.find('pre'))
        data = all_divs[59:-6]
        data_json = json.loads(data)
        try:
            timestamp = data_json['graphql']['shortcode_media']['taken_at_timestamp']
            user_id = data_json['graphql']['shortcode_media']['owner']['id']
            user_name = data_json['graphql']['shortcode_media']['owner']['username']
            name = data_json['graphql']['shortcode_media']['owner']['full_name']
            dt_object = datetime.fromtimestamp(timestamp)
            time = dt_object.time()
            date = dt_object.date()

            location_id = data_json['graphql']['shortcode_media']['location']['id']
            location_name = data_json['graphql']['shortcode_media']['location']['name']
            location_address_json = data_json['graphql']['shortcode_media']['location']['address_json']
            response = requests.get(f"https://www.google.com/search?q={location_name}+coordinates")
            soup = bs(response.text, "html.parser")
            coords = soup.find("div", "BNeawe iBp4i AP7Wnd").text.split(',')
            latitude = coords[0][:7]
            longitude = coords[1].strip()[:7]
            result.loc[j] = [time,date,user_id,name,user_name,location_id,location_name,latitude,longitude]
            j+=1
        except:
            continue
# driver.close() 

print(result)
result.to_csv(r'C:\Users\91771\Downloads\goa2018.csv')


