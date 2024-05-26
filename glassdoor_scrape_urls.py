import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


#--------------------Step One-----------------------#

salaries_url = "https://www.glassdoor.com/Salaries/index.htm"


def get_formated_url(salaries_url, job_title, country):

   with driver_setup() as driver:

      driver.get(salaries_url)

      job_title = job_title
      country = country

      job_input_finder = "typedKeyword"
      country_input_finder = "Autocomplete"
      search_button_finder = "clickSource"

      job_input = driver.find_element(By.NAME, job_input_finder)
      job_input.send_keys(job_title)

      country_input = driver.find_element(By.NAME, country_input_finder)
      country_input.send_keys(country)

      dropdown_item_locator = (By.XPATH, f"//span[@class='query' and text()='{country}']")

      dropdown_item = WebDriverWait(driver, 3).until(
         EC.visibility_of_element_located(dropdown_item_locator)
      )

      dropdown_item.click()

      search_button = driver.find_element(By.NAME, search_button_finder)
      driver.execute_script("arguments[0].click();", search_button)


      pagination_locator_by_span = (By.XPATH, "//div[@data-test='pagination']")
      pagination_locator_by_p = (By.XPATH, "//p[@class='RecentSalariesReport_pageCount__me5vp']")
      try:
         pagination = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located(pagination_locator_by_span)
         )
         pagination = pagination.find_element(By.TAG_NAME, 'span').get_attribute('innerHTML')
      except:
         pagination = WebDriverWait(driver,3).until(
            EC.visibility_of_element_located(pagination_locator_by_p)
         )
         pagination = pagination.get_attribute('innerHTML')
      
           
      total_pages = pagination.split('of ')[-1]
      total_pages = total_pages.replace(',','')
      url = driver.current_url
      url = url[:-4]+"_IP{}"+url[-4:]

      return (url, total_pages)



countries_list = pd.read_csv('./inputs/countries.csv')
jobs_list = pd.read_csv('./inputs/jobs.csv')


with open('data/urls_for_job_in_country.csv','w') as f:
   f.write("""job\tcountry\tnumber_of_pages\tunique_url\n""")

count = 0
total = 60*8

for job in jobs_list['jobs']:
   for country in countries_list['countries']:

      unique_url, number_of_pages = get_formated_url(salaries_url, job, country)

      with open('data/urls_for_job_in_country.csv', 'a') as f:
         line = '\t'.join([job, country, number_of_pages, unique_url])
         f.write(line+'\n')
         count += 1
         print(f"Completed: {count}, Left: {total-count}, Percentage Completed: {(count)/total*100:2f}")