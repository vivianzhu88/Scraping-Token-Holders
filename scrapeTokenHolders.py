import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

#Accessing the iFrame that contains the table of balances
driver = webdriver.Chrome(executable_path='/Users/fangrl4ever/Downloads/chromedriver')
driver.get('https://etherscan.io/token/0x168296bb09e24a88805cb9c33356536b980d3fc5#balances')
time.sleep(5)
iframe1 = driver.find_element_by_id('tokeholdersiframe')
driver.switch_to.frame(iframe1)
soup = BeautifulSoup(driver.page_source, 'html.parser')

#Clicking next button
token_holders = soup.find_all('tr')
del token_holders[0]

for i in range(1,20):
    driver.find_element_by_link_text('Next').click()
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    token_holders = token_holders + soup.find_all('tr')
    del token_holders[50*i]
    time.sleep(5)

#Putting all the scraped data from iframe into lists
rank = []
address = []
quantity = []
percent = []

for i in range(0, len(token_holders)):
    h = token_holders[i]
    holder_info = h.find_all('td')

    rank.append(holder_info[0].get_text())
    address.append(holder_info[1].get_text())
    quantity.append(holder_info[2].get_text())
    percent.append(holder_info[3].get_text())

#Putting data into a csv file
import pandas as pd
holders = pd.DataFrame({
    'Rank': rank,
    'Address': address,
    'Quantity': quantity,
    'Percentage': percent
    })
holders = holders[['Rank','Address','Quantity','Percentage']]
holders.to_csv('holders.csv', index=False, encoding='utf-8')



    



