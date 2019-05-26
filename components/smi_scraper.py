#Python Script---------------------------------------------------------------------------------------------------------------------------
#Title: smi_scraper
# coding: utf-8
#----------------------------------------------------------------------------------------------------------------------------------------

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
import numpy as np
import pandas as pd
import json
from MatterhornLabSDK import MatterhornLabAPI, Company, Entry
from json import JSONEncoder

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder.default  # Save unmodified default.
JSONEncoder.default = _default # Replace it.


#Cleaning Data Functions     
def isFloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False  

def data_clean(input):
    if input == None:
        input = ""
    if input.strip() == "":
        input = "NaN"
    #Transform % string into float values
    if "%" in input:
        input = float(input.strip("%")) / 100
    
    #Transform Input into Float if it is    
    if isFloat(input):  
        input = float(input) 
        
    return input
        
def six_ratios_scraper(ISINS):
    CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
    options = webdriver.ChromeOptions()
    #options.binary_location = chrome_bin
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    #options.add_argument('headless') #activate if not open chrome
    options.add_argument('window-size=1200x600')
    driver = webdriver.Chrome(options=options)
    
    
    #prepare DataFrame for all results
    result = pd.DataFrame()
    
    #Iterate trough all ISINS
    for ISIN in ISINS:
        
        #launch url
        url = "https://www.six-group.com/exchanges/shares/security_info_en.html?id="+ ISIN
        
        # create a new Chrome session
        driver.implicitly_wait(30)
        driver.get(url)
    
        #After opening the url above, Selenium clicks the specific button
        python_button = driver.find_element_by_id('swx_widget__ImageTabButton_4') 
        python_button.click() #click button
        
        #Wait 10s to load and make sure that our scraper is not considered as a network attack
        time.sleep(10)
        
        #Selenium hands the page source to Beautiful Soup
        soup_level1 = BeautifulSoup(driver.page_source, 'lxml')
        
        #Find Indexes of First and Last Item  
        start = "NaN"
        end = "NaN" 
        for i in range(1, len(soup_level1.find_all('td', align="left", valign="top"))):     
            if soup_level1.find_all('td', align="left", valign="top")[i].string == "Gross margin":
                start = i

            if soup_level1.find_all('td', align="left", valign="top")[i].string == "Cash flow per share":
                end = i  
        
        #Create Dictionary consisting of all Scraped Datapoints
        #If Datapoints are available
        if start != "NaN" and end != "NaN":
            data = {}
            for i in range(start, end, 2):
               data.update({soup_level1.find_all('td', align="left", valign="top")[i].string: data_clean(soup_level1.find_all('td', align="left", valign="top")[i+1].string)})
            Key_Ratios =  pd.DataFrame.from_dict(data, orient = "index", columns=[ISIN])
       
        #If no datapoints are available fill with NaN
        else:
            Key_Ratios = pd.DataFrame(len(result.axes[0]) * [float("NaN")], index = result.axes[0], columns=[ISIN])

        #Merge Data to Dataframe
        result = pd.concat([result, Key_Ratios], axis=1)
        
        print(datetime.datetime.now(), ISIN, "has just been scraped")
        
    #end the Selenium browser session
    driver.quit()
    
    return result   


def six_stock_price_scraper():
    import requests
    url = 'https://www.six-group.com/exchanges/shares/explorer/download/download_en.html'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    #Try to access webpage and download HTML
    try:
        r = requests.get(url, headers=headers, timeout=5)
    
    except requests.ConnectionError as e:
        print("Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("Timeout Error")
        print(str(e))
    except requests.RequestException as e:
        print("General Error")
        print(str(e))
    except KeyboardInterrupt:
        print("Someone closed the program")
    
    #If Webpage access succeeds, scrape content check for all available Dates. If today's date is available download it.
    if r:
        soup = BeautifulSoup(r.content)
    
        Dates = []
        for i in  soup.find_all(align="left", class_="first", valign="top"):
           Dates.append(i.string)
        
        if datetime.datetime.today().strftime("%d.%m.%Y") in Dates and datetime.datetime.now().time().hour >= 23 and datetime.datetime.now().time().minute >= 35 :
            url_csv = "https://www.six-group.com/exchanges/data/market/statistics/swiss_blue_chip_shares_" +str(datetime.datetime.today().strftime("%Y-%m-%d")) +".csv"
            Stock_Data  = pd.read_csv(url_csv, sep = ";") 
            url_smi_csv = "https://www.six-group.com/exchanges/downloads/indexdata/hsmi.csv"
            SMI_Data = pd.read_csv(url_smi_csv,skiprows=6, sep=";")
            
            #Combine Stock Data and SMI Data into a Dataframe called Current_prices
            DB_Stock_Info = pd.read_csv("data/DB_Stock_Info.csv", sep = ";")
            Current_prices = pd.merge(DB_Stock_Info[["ISIN", "Reuters"]],Stock_Data[["ISIN", "ClosingPrice"]])
            Current_prices = Current_prices.append({"ISIN": "NaN", "Reuters": "SSMI", "ClosingPrice":SMI_Data["Close"].iloc[0]}, ignore_index=True)  
            
            
            #Now upload all the Data on the Database
            #Database starts at 1 and has 20 Stocks + 1 Index(SMI)    
            #Download the different tickers and identify the prices and then add them to the database
            api = MatterhornLabAPI()            
            for x in range(1, 22):
                name = api.companies.get(x)
                tickers = api.companies.get_tickers(x)
                date = datetime.datetime.today().strftime("%Y-%m-%d")
                price = Current_prices.ClosingPrice[Current_prices["Reuters"] == tickers].get_values()[0]
                new_entry = Entry(company=name, price=price, timestamp=date)
                print(new_entry)
                new_entry = api.entries.add(new_entry)
            return Current_prices
        else:
            print("No Data Available, please wait till new data has been uploaded after 23:35")
       
    else:
        print('An error has occurred.')


