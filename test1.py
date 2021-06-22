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



hashtag='manali2017'
browser = webdriver.Chrome(executable_path=r'C:\Program Files\webdriver\chromedriver.exe')
browser.get('https://www.instagram.com/explore/tags/'+hashtag)
Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


links=[]
source = browser.page_source
data=bs(source, 'html.parser')
body = data.find('body')
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


j=0
result=pd.DataFrame(columns = ['Time','Date','User_id','Full_Name','User_Name','Location_Id','Location_Name','Latitude','Longitude'])
driver = webdriver.Chrome(executable_path=r'C:\Program Files\webdriver\chromedriver.exe') 
for i in range(len(link1)):
    flag = 0
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
    # key_list = []
    # for i in data_json['graphql']['shortcode_media']:
    #     k = (i)
    #     key_list.append(k)
    # for i in range(0,len(key_list)):
    #     if key_list[i]=="location":
    #         flag =1
    #         break
    # print(flag)


    # if flag ==1:
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
result.to_csv(r'C:\Users\91771\Downloads\raj.csv')
print(result)

