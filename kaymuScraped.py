import requests,lxml
from bs4 import BeautifulSoup
import pandas as pd
import sys
import re

BASE_URL = "https://www.daraz.com.np/smartphones/?page="
pages = 8 # There are 8 pages containing smartphones 
def scrapeSite():
    for i in range(1,pages+1):
        page_number = i
        page = requests.get(BASE_URL + str(i)) #Append page number to the BASE_URl and read the html content from that page
        soup = BeautifulSoup(page.content,"html.parser")
        # To find the brand of the phone on sale
        all_brands = [ re.sub(r'\xa0','',brand.get_text()) for brand in soup.find_all('span', class_='brand')]

        # To find the description of the phone on sale
        phone_desc = [ re.sub(r'\xa0','',phone.get_text()) for phone in soup.find_all('span', class_='name')]

        # To find the price of the phone 
        prices = [float(re.sub(',','',re.sub(r'\xa0','',phone.get_text()))) for phone in soup.select('span.price-box > span:nth-of-type(1) > span:nth-of-type(2)')]

        # To find the price before the discount
        # prices_old = [re.sub(r'\xa0','',phone.get_text()) for phone in soup.select('span.price-box > span:nth-of-type(2) > span:nth-of-type(2)')]

        createCSV(page_number,all_brands,phone_desc,prices) #Contents scraped from each html pages are added/appended to the CSV file

def createCSV(pageNumber,all_brands,phone_desc,prices):
    all_phones = {
    'Brand':all_brands,
    'Description':phone_desc,
    'Price':prices
    }

    df = pd.DataFrame(all_phones,columns = ['Brand','Description','Price'])
    if(pageNumber==1):
        df.to_csv('kaymu.csv',index = False)# For the first page create a new csv file
    else:
        df.to_csv('kaymu.csv',mode = 'a',header = False,index = False) #From second page onwards append the scraped data to the end of csv file

scrapeSite()
