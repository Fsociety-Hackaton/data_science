import pandas as pd
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from time import time

def scraper(location, country):
    '''
    This function take two arguments, location could be: 
    Colombia
    Mexico
    and country could be:
    co
    mx
    '''

    #Proxies
    proxy = "51.81.82.175:80"

    #Driver for Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % proxy)
    driver = webdriver.Chrome(executable_path='driver/chromedriver.exe')

    #Keywords
    linkedin_kw = [
        'data%20Science',
        'backend',
        'frontend',
        'full%20Stack'
    ]

    indeed_kw = [
        'data+science',
        'backend',
        'frontend',
        'full+stack'
    ]

    for key in linkedin_kw:
        #URL
        linkedin_url = f'https://www.linkedin.com/jobs/search?keywords={key}&location={location}&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&sortBy=R'
        
        driver.get(linkedin_url)

    for key in indeed_kw:
        #URL
        indeed_url = f'https://{country}.indeed.com/jobs?q={key}&l={location}'

        driver.get(indeed_url)

    
    ticjob_url = 'https://ticjob.co/es/search'


    
    sleep(5)

def main():
    scraper('Colombia', 'co')

if __name__ == "__main__":
    main()

