import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread
from math import ceil


#--------------------Setting Up Driver---------------------#
def driver_setup():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--disable-gpu")
  user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
  chrome_options.add_argument(f'user-agent={user_agent}')
  driver = webdriver.Chrome(executable_path='./chromedriver-linux64/chromedriver', options=chrome_options)
  return driver


#----------------------Step Two----------------#


#-----------div selector--------------#
list_div_locator = (By.XPATH, """//*[@id="nodeReplace"]/div/div[2]/div[2]""")

selector = ".py.d-flex.align-items-start.align-items-lg-center.row, .py.d-flex.align-items-start.align-items-lg-center.css-17435dd.row"





def save_data(job, country, element):
   #------------selectors for infos---------------#
   company_name = 'a.css-1ikln7a.el6ke052'
   company_rating = 'span.css-h9sogr m-0 css-60s9ld el6ke050'.replace(' ','.')
   position_title = 'span.d-flex align-items-middle css-1in2cw4 el6ke050'.replace(' ','.')
   median_pay = 'h3.m-0 css-16zrpia el6ke054'.replace(' ','.')

   #unit, low, high
   ranges = 'span.m-0 css-1in2cw4 el6ke050'.replace(' ','.')

   html = element.get_attribute('outerHTML')
   soup = BeautifulSoup(html, 'html.parser')

   try:
      company_name = soup.select(company_name)[0].text
   except:
      company_name = 'NA'
   try:
      company_rating = soup.select(company_rating)[0].text
   except:
      company_rating = 'NA'
   try:
      position_title = soup.select(position_title)[0].text
   except:
      position_title = 'NA'
   try:
      median_pay = soup.select(median_pay)[0].text
   except:
      median_pay = 'NA'
   try:
      addn = soup.select(ranges)
   except:
      addn = []
   try:
      low = addn[1].text
   except:
      low = 'NA'
   try:
      high = addn[2].text
   except:
      high = 'NA'
   try:
      unit = addn[0].text
   except:
      unit = 'NA'

   with open('data/scraped_data.csv', 'a') as f:
      f.write('\t'.join([job, country, company_name, company_rating, position_title, median_pay, low, high, unit])+'\n')
   


def get_html_elements(job, country, url):
    driver = driver_setup()

    driver.get(url)
    time.sleep(1)

    found = False
    while not found:
      try:
         divs_list = WebDriverWait(driver, 2).until(
                  EC.visibility_of_element_located(list_div_locator)
               )
         found = True
      
      except:
         driver.quit()
         driver = driver_setup()
         driver.get(url)
         found = False

    divs = driver.find_elements(By.CSS_SELECTOR, selector)

    print(f"Scraped link {url} found {len(divs)} divs....")

    for j in divs:
       save_data(job, country, j)  

    driver.quit()




def start(row, count):
   job = row['job']
   country = row['country']
   number_of_items = row['number_of_pages']
   pages_to_scrape = ceil(number_of_items/20)
   address = row['unique_url']

   print('\n'.join([job,country,str(number_of_items),address, str(pages_to_scrape)]))


   for page in range(1, pages_to_scrape+1, 8):
      threads = []
      for j in range(8):
         thread = Thread(target=get_html_elements, args = (job, country, address.format(page+j)))
         threads.append(thread)

      try:
         for thread in threads:
            thread.start()
      except:
         pass
      try:
         for thread in threads:
            thread.join()
      except:
         pass

   count += number_of_items
   return count




urls_data = pd.read_csv('./data/urls_for_job_in_country.csv')

count = 0
total_jobs = sum(urls_data['number_of_pages'])


for row in range(len(urls_data)):
   row = urls_data.loc[row]

   count = start(row, count)
   print(f"Completed: {count}, left: {total_jobs-count}, Percentage Completed: {round((count/total_jobs)*100,3)} %")

