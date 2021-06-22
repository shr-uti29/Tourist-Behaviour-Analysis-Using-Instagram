import requests

from bs4 import BeautifulSoup

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

import time

  

#url of the page we want to scrape

url = "https://www.instagram.com/p/Bvll6dggSIr/?__a=1"

  

# initiating the webdriver. Parameter includes the path of the webdriver.

driver = webdriver.Chrome(executable_path=r'C:\Program Files\webdriver\chromedriver.exe') 

driver.get(url) 

  

  

html = driver.page_source

  

# this renders the JS code and stores all

# of the information in static HTML code.

  

# Now, we could simply apply bs4 to html variable

soup = BeautifulSoup(html, "html.parser")
#print(soup.prettify())

all_divs = soup.find('pre')
print(all_divs)
# job_profiles = all_divs.find_all('a')

  

# # printing top ten job profiles

# count = 0

# for job_profile in job_profiles :

#     print(job_profile.text)

#     count = count + 1

#     if(count == 10) :

#         break

  

driver.close() # closing the webdriver