import requests
from selenium import webdriver
from bs4 import BeautifulSoup

# #Proxies 
# proxy = {'http':'http://157.230.14.2:3128',
#         'https':'https://157.230.14.2:3128'}
proxy = "51.81.82.175:80"

#geold Colombia = 100876405
#geold Mexico, just change location to mexico
#URL
indeed_url = 'https://co.indeed.com/' 

#Driver for Selenium
options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=%s' % proxy)
driver = webdriver.Chrome(executable_path='driver/chromedriver.exe', chrome_options=options)

driver.get(indeed_url)


