import pandas as pd
import datetime
from datetime import date
import requests
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from bs4 import BeautifulSoup
from time import sleep
from time import time
import lxml
import db
import json

def replace(key):
    '''
    This function parse the categories
    '''
    return key.replace("%20"," ").replace("+", " ")


def parser(driver):
    '''
    This function gets the page source and creates the bs4 soup
    '''
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')

    return soup

def scraper(location, country):
    '''
    This function take two arguments, location could be: 
    Colombia
    Mexico
    and country could be:
    co
    mx
    '''
    #Driver for Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    driver = webdriver.Chrome(executable_path='driver/chromedriver.exe', options = options)

    #Keywords
    linkedin_kw = [
        'data%20science',
        'backend',
        'frontend',
        'full%20stack'
    ]
    indeed_kw = [
        'data+science',
        'backend',
        'frontend',
        'full+stack'
    ]

    for key in linkedin_kw:
        
        #URL
        linkedin_url_relevant = f'https://www.linkedin.com/jobs/search?keywords={key}&location={location}&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&sortBy=R'
        linkedin_url_daily = f'https://www.linkedin.com/jobs/search?keywords={key}&location={location}&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&sortBy=DD'
        
        #Open the driver's window
        driver.get(linkedin_url_daily)
        sleep(5)

        #Get page source
        source = parser(driver)
        job_list = source.find('ul', attrs={'class':'jobs-search__results-list'})
        print(f'Found {len(job_list)} {replace(key)} jobs in {location}')

        #Job information
        job_title = []
        job_image = []
        job_company = []
        job_country = []
        job_location = []
        job_date = []
        job_description = []
        job_link = []
        job_category = []

        for job in job_list:
            job_title.append(job.find('h3', attrs={'job-result-card__title'}).get_text())
            job_country.append(location)
            job_location.append(job.find('span', attrs={'job-result-card__location'}).get_text())
            job_date.append(job.select_one('time')['datetime'])
            job_link.append(job.find('a', attrs={"result-card__full-card-link"}).get('href'))
            job_category.append(replace(key))

        #Loop for click each job
        for n in range(1,len(job_list)+1):
            #Try to Click on each job
            try:
                job_click = f"/html/body/main/div/section/ul/li[{n}]/a"
                driver.find_element_by_xpath(job_click).click()
            except ElementClickInterceptedException:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            #Sleep to let the scraper to gets the data
            sleep(1)
            try:
                job_company.append(driver.find_element_by_xpath('//section[@class="topcard"]/div/div/h3/span/a').text)
            except:
                job_company.append('Sin información de la compañia')
            try:
                job_image.append(driver.find_element_by_xpath("/html/body/main/section/div[2]/section[1]/div[1]/a/img").get_attribute('src'))
            except:
                job_image.append('Sin imagen')
            job_description.append(driver.find_element_by_xpath("/html/body/main/section/div[2]/section[2]/div").text)
            
            #Increase the counter
            n+=1
        
        jobs = pd.DataFrame({
            'title': job_title,
            'company': job_company,
            'image': job_image,
            'country': job_country,
            'location': job_location,
            'date': job_date,
            'description': job_description,
            'link': job_link,
            'category': job_category
        })
        
        #Insert into DB
        try:
            jobs_convert = jobs.to_json(orient='records')
            jobs_json = json.loads(jobs_convert)
            #Conection to DB
            conection = db.connection()
            insert_jobs = conection.jobs_test

            result = insert_jobs.insert_many(jobs_json)

            print('Values were successfully inserted into DB')
            
        except NameError:
            print(f'No objects were inserted {NameError}')
    
            
    for key in indeed_kw:
        
        #URL
        indeed_url = f'https://{country}.indeed.com/jobs?q={key}&l={location}&sort=date'

        #Open the driver's window
        driver.get(indeed_url)
        sleep(4)

        #Get page source
        source = parser(driver)
        job_list = source.find_all('div',attrs={'class':'clickcard'})
        print(f'Found {len(job_list)} {replace(key)} jobs in {location}')

        #Job information
        job_title = []
        job_company = []
        job_country = []
        job_location = []
        job_date = []
        job_description = []
        job_link = []
        job_category = []


        for job in job_list:
    
            job_title.append(job.find('a', attrs={'class':'jobtitle'}).get_text())

            try:
                job_company.append(job.find('span', attrs={'class':'company'}).get_text())
            except:
                job_company.append('Sin información de la compañia')

            try:
                job_location.append(job.find('span', attrs={'class':'location'}).get_text())
            except:
                job_location.append('Sin información sobre ubicación')

            job_country.append(location)
            job_date.append(date.today().strftime("%Y-%m-%d"))

            link = job.find('a', attrs={'class':'jobtitle'}).get('href')
            link_formated = f'https://{country}.indeed.com' + link
            job_link.append(link_formated)

            job_category.append(replace(key))

        #Get Description for each link
        for link in job_link:
            try:
                driver.get(link)
            except:
                print('No se pudo obtener el link {}'.format(link))

            #Sleep to let the scraper gets the data
            sleep(2)
            try:
                job_description.append(driver.find_element_by_xpath('//div[@id="content"]').text)
            except:
                try:
                    job_description.append(driver.find_element_by_xpath('//div[@id="jobDescriptionText"]').text)
                except:
                    job_description.append('Sin descripción')

            
        jobs = pd.DataFrame({
            'title': job_title,
            'company': job_company,
            'image': 'Sin imagen',
            'country': job_country,
            'location': job_location,
            'date': job_date,
            'description': job_description,
            'link': job_link,
            'category': job_category
        })

        #Insert into DB
        try:
            jobs_convert = jobs.to_json(orient='records')
            jobs_json = json.loads(jobs_convert)
            #Conection to DB
            conection = db.connection()
            insert_jobs = conection.jobs_test

            result = insert_jobs.insert_many(jobs_json)

            print('Values were successfully inserted into DB')
            
        except NameError:
            print(f'No objects were inserted {NameError}')

def main():
    locations = ['Colombia', 'Mexico']
    countries = ['co', 'mx']

    scraper(locations[0], countries[0])
    scraper(locations[1], countries[1])

if __name__ == "__main__":
    main()

