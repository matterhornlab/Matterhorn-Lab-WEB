#Python Script---------------------------------------------------------------------------------------------------------------------------
#Title: APSScheduler
# coding: utf-8
#----------------------------------------------------------------------------------------------------------------------------------------


from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import pandas as pd
from components import isFloat, data_clean, six_ratios_scraper, six_stock_price_scraper

import pandas as pd
import time
import numpy as np
import json
from MatterhornLabSDK import MatterhornLabAPI, Company, Entry
from json import JSONEncoder

sched = BlockingScheduler()


#Daily download of SMI Data at 23:50
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=23, minute = 50)
def scheduled_job():
    Current_prices = six_stock_price_scraper()
    print(datetime.datetime.now(), 'The data has been downloaded and added to the database')


#Monthly download of Key Ratio SMI Data 
@sched.scheduled_job('cron', year='*', month='*', day=1, week='*', day_of_week='*', hour=23, minute=55, second=0)
def scheduled_job():
    DB_Stock_Info = pd.read_csv("data/DB_Stock_Info.csv", sep = ";")
    df = six_ratios_scraper(ISINS = DB_Stock_Info["ISIN"])
    df.to_csv("data/DB_Stock_Key_Ratios.csv", sep = ";")
    print(datetime.datetime.now(), 'The Key Ratios have been downloaded and written to a csv file')
    
sched.start()



