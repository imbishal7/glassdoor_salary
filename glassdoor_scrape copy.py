import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time
import os
import requests
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
from threading import Thread

#--------------------Setting Up Driver---------------------#
def driver_setup():
  chrome_options = webdriver.ChromeOptions()
  #chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--disable-gpu")
  driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
  return driver



#------------------Browsing--------------#
urls = "https://www.glassdoor.com/Salaries/data-scientist-salary-SRCH_KO0,14_IP{}.htm"

class_name = "py d-flex align-items-start align-items-lg-center row".replace(" ", ".")



"""
d1 = driver_setup()

with open('./glassdoor_cookie.json', 'r') as f:
    cookies = json.load(f)s


d1.get(urls[0].format(1))

for cookie in cookies:
  if 'sameSite' in cookie:
     cookie['sameSite'] = 'Strict'
  d1.add_cookie(cookie)

d1.refresh()



source = d1.page_source
div = d1.find_elements(By.CLASS_NAME, class_name)


for i in div:
   soup = BeautifulSoup(i.get_attribute("innerHTML"), 'html.parser')
   print(soup.find('a'))
#print(source)"""


with open('./glassdoor_cookie.json', 'r') as f:
      cookies = json.load(f)


count = 0

def save_raw_html(element):
   global count
   html = element.get_attribute('innerHTML')
   with open("raw.html", 'a') as f:
      f.write(html)
      count+=1


def get_html_elements(url):
    driver = driver_setup()

    driver.get(url)
    time.sleep(1)

    divs = driver.find_elements(By.CLASS_NAME, class_name)
    print(f"Scraped link {url} finding {len(divs)} divs....")

    for j in divs:
       save_raw_html(j)  
    print(f"Wrote {count} divs..")
    print(driver.page_source)
    time.sleep(10)
    driver.quit()


for i in range(1,2):
    get_html_elements(urls.format(i))

#-----------Threading------------#
"""threads = [f't{i}' for i in range(1,9)]

for i in range(1,501,8):
   try:
      for j in range(8):
         threads[j] = Thread(target = get_html_elements, args = (urls.format(j+i),))
      for j in threads:
         j.start()
      for j in threads:
         j.join()
   except:
      pass"""