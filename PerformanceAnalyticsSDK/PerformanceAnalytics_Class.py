#Python Script---------------------------------------------------------------------------------------------------------------------------
#Title: Performance Analytics
# coding: utf-8
#---
import pandas as pd

import datetime 
import time
import math
import csv
import numpy as np
import scipy
from scipy.stats import trim_mean, kurtosis
from scipy.stats.mstats import mode, gmean, hmean
from scipy.stats import norm
from pandas.tseries.offsets import BDay
import ta as ta


class Performance():
    def __init__(self, Reuters):
        self.reuters  = Reuters
        
        #actual price data
        url_csv = "http://matterhorn-lab.herokuapp.com/download/"+ str(self.reuters)
        prices_data  = pd.read_csv(url_csv, sep = ",") 
        start, stop, step = 0, -14, 1
        prices_data["Date"] = prices_data["Date"].str.slice(start, stop, step)
        
        prices_data = prices_data[::-1].reset_index()
        prices_data = prices_data.drop(['index'], axis=1)
        prices_data = prices_data.sort_values(["Date"], ascending = [1]).reset_index()
        prices_data = prices_data.drop(['index'], axis=1)
        
        
        #static
        stock_info = pd.read_csv('data/DB_Stock_Info.csv', sep=';')
        key_ratios = pd.read_csv('data/DB_Stock_Key_Ratios.csv', sep=';')
    
        # get the number of business days
        c_size = len(prices_data.columns)
        r_size = prices_data.shape[0]
         
        date_data = prices_data.iloc[:,0]
        today = date_data.iloc[r_size-1:r_size]
        today = pd.to_datetime(today)
        today = datetime.date(int(today.dt.year),int(today.dt.month),int(today.dt.day))
        
        # calculate days yesterday
        yesterday =  today -BDay(1)
        # calculate days last week
        lastweek = today -BDay(5)
        # calculate days  since start month
        startmonth = datetime.date(int(today.strftime('%Y')),int(today.strftime('%m')),1)
        days_start_month = np.busday_count(startmonth,today)
        # calculate days  last month
        lastmonth = datetime.date(int(today.strftime('%Y')),int(today.strftime('%m'))-1,int(today.strftime('%d')))
        days_last_month = np.busday_count(lastmonth,today)
        # calculate days since start year
        yearstart = datetime.date(int(today.strftime('%Y')),1,1)
        days_start_year = np.busday_count(yearstart,today)
        # calculate days one year
        lastyear = datetime.date(int(today.strftime('%Y'))-1,int(today.strftime('%m')),int(today.strftime('%d')))
        days_last_year = np.busday_count(lastyear,today)
        # calculate days three years
        last3years = datetime.date(int(today.strftime('%Y'))-3,int(today.strftime('%m')),int(today.strftime('%d')))
        days_last_3years = np.busday_count(last3years,today)
        # calculate days five years
        last5years = datetime.date(int(today.strftime('%Y'))-5,int(today.strftime('%m')),int(today.strftime('%d')))
        days_last_5years = np.busday_count(last5years,today)
        # calculate days ten years
        last10years = datetime.date(int(today.strftime('%Y'))-10,int(today.strftime('%m')),int(today.strftime('%d')))
        days_last_10years = np.busday_count(last10years,today)
        
        # calculate returns        
        prices = prices_data.iloc[:,1:c_size]
        #returns = math.log(prices/prices.shift(1))
        #prices_year = prices.iloc[r_size-days_year:r_size]
        price_change = pd.DataFrame(prices.values[r_size-1] - prices)
        price_change.columns = [ Reuters]
        returns = prices.pct_change(1)
        
        # calculate price and return today
        returns_today = returns.iloc[r_size-1:r_size]
        prices_today = prices.iloc[r_size-1:r_size]
        price_change_today = price_change.iloc[r_size-1:r_size]
        
        # calculate price and return yesterday
        returns_yesterday = returns.iloc[r_size-2:r_size]
        prices_yesterday = prices.iloc[r_size-2:r_size]
        cum_return_yesterday = prices_yesterday.loc[r_size-1] / prices_yesterday.loc[r_size-2] -1
        average_return_yesterday = np.mean(returns_yesterday)
        price_change_yesterday = price_change.iloc[r_size-2:r_size-1]
        
        # calculate price and return last week
        returns_last_week = returns.iloc[r_size-5:r_size]
        prices_last_week = prices.iloc[r_size-5:r_size]
        cum_return_last_week = prices_last_week.loc[r_size-1] / prices_last_week.loc[r_size-5] -1
        average_return_last_week = np.mean(returns_last_week)
        price_change_last_week = price_change.iloc[r_size-5:r_size]
        vola_last_week = np.std(returns_last_week)
        sharpe_ratio_last_week = average_return_last_week /vola_last_week
        
        # calculate price and return since start month
        returns_start_month = returns.iloc[r_size-days_start_month:r_size]
        prices_start_month = prices.iloc[r_size-days_start_month:r_size]
        cum_return_start_month = prices_start_month.loc[r_size-1] / prices_start_month.loc[r_size-days_start_month] -1
        average_return_start_month = np.mean(returns_start_month)
        price_change_start_month = price_change.iloc[r_size-days_start_month:r_size]
        vola_start_month = np.std(returns_start_month)
        sharpe_ratio_start_month = average_return_start_month /vola_start_month
        
        # calculate price and return last month
        returns_last_month = returns.iloc[r_size-days_last_month:r_size]
        prices_last_month = prices.iloc[r_size-days_last_month:r_size]
        cum_return_last_month = prices_last_month.loc[r_size-1] / prices_last_month.loc[r_size-days_last_month] -1
        average_return_last_month = np.mean(returns_last_month)
        price_change_last_month = price_change.iloc[r_size-days_last_month:r_size]
        
        # calculate price and return since start year
        returns_start_year = returns.iloc[r_size-days_start_year:r_size]
        prices_start_year = prices.iloc[r_size-days_start_year:r_size]
        cum_return_start_year = prices_start_year.loc[r_size-1] / prices_start_year.loc[r_size-days_start_year] -1
        average_return_start_year = np.mean(returns_start_year)
        price_change_start_year = price_change.iloc[r_size-days_start_year:r_size]
        vola_start_year = np.std(returns_start_year)
        sharpe_ratio_start_year = average_return_start_year /vola_start_year
        
        # calculate price and return one year
        returns_last_year = returns.iloc[r_size-days_last_year:r_size]
        prices_last_year = prices.iloc[r_size-days_last_year:r_size]
        cum_return_last_year = prices_last_year.loc[r_size-1] / prices_last_year.loc[r_size-days_last_year] -1
        average_return_last_year = np.mean(returns_last_year)
        price_change_last_year = price_change.iloc[r_size-days_last_year:r_size]
        vola_last_year = np.std(returns_last_year)
        sharpe_ratio_last_year = average_return_last_year /vola_last_year
        
        # calculate price and return three years
        returns_last_3years = returns.iloc[r_size-days_last_3years:r_size]
        prices_last_3years = prices.iloc[r_size-days_last_3years:r_size]
        cum_return_last_3years = prices_last_3years.loc[r_size-1] / prices_last_3years.loc[r_size-days_last_3years] -1
        average_return_last_3years = np.mean(returns_last_3years)
        price_change_last_3years = price_change.iloc[r_size-days_last_3years:r_size]
        vola_last_3years = np.std(returns_last_3years)
        sharpe_ratio_last_3years = average_return_last_3years /vola_last_3years
        
        # calculate price and return five years
        returns_last_5years = returns.iloc[r_size-days_last_5years:r_size]
        prices_last_5years = prices.iloc[r_size-days_last_5years:r_size]
        cum_return_last_5years = prices_last_5years.loc[r_size-1] / prices_last_5years.loc[r_size-days_last_5years] -1
        average_return_last_5years = np.mean(returns_last_5years)
        price_change_last_5years = price_change.iloc[r_size-days_last_5years:r_size]
        vola_last_5years = np.std(returns_last_5years)
        sharpe_ratio_last_5years = average_return_last_5years /vola_last_5years
        
        # calculate price and return ten years
        returns_last_10years = returns.iloc[r_size-days_last_10years:r_size]
        prices_last_10years = prices.iloc[r_size-days_last_10years:r_size]
        cum_return_last_10years = prices_last_10years.loc[r_size-1] / prices_last_10years.loc[r_size-days_last_10years] -1
        average_return_last_10years = np.mean(returns_last_10years)
        price_change_last_10years = price_change.iloc[r_size-days_last_10years:r_size]
        vola_last_10years = np.std(returns_last_10years)
        sharpe_ratio_last_10years = average_return_last_10years /vola_last_10years
        
        # all time
        cum_return_all = prices.loc[r_size-1] / prices.loc[3] -1
        average_return_all = np.mean(returns)
        vola_all = np.std(returns)
        sharpe_ratio_all = average_return_all /vola_all
        # year high, low and range
        year_high = prices_last_year.max()
        year_low = prices_last_year.min()
        range_low_high = year_high - year_low
        range_percent = range_low_high / year_high
        
        # investment of 10000 CHF
        help_investment = returns
        help_investment = help_investment.drop(help_investment.index[0:2])
        help_invest = [0] * (c_size-1)
        help_investment.iloc[0] = help_invest
        investment = (1+help_investment).cumprod() *10000
        
        # describtive statistics
        mean = np.mean(returns_last_year)
        std = np.std(returns_last_year)
        Z_99 = norm.ppf([0.01])
        
        
        # Value at risk
        Covar_Var = -(mean-Z_99*std)
        n_sims = 1000000
        SimVar =[]
        for i in range(c_size-1):
            np.random.seed(i)
            random_numbers = np.random.normal(0, 1, n_sims)
            sim_returns=mean[i]+std[i]*random_numbers
            SimVar = (np.percentile(sim_returns, 1))
        
        HistVar=[]
        for i in range(0,r_size-days_last_year):
            help_VaR = returns.iloc[r_size-days_last_year-i:r_size-i]
            HistVar.append(np.percentile(help_VaR, 1))
         
        df_HistVar = {}
        df_HistVar= {"Name": HistVar}
        HistVar = pd.DataFrame(HistVar)
        
        # Expected Shortfall
        cutoff = int(round(days_last_year * 0.01,0))
                
        ES = []
        for i in range(0,r_size-days_last_year):
            help_ES = returns.Price.iloc[r_size-days_last_year-i:r_size-i]
            losses = help_ES.sort_values()
            expectedloss = np.mean(losses.iloc[0:cutoff])
            ES.append(expectedloss)
         
        data_ES = {}
        data_ES = {"Name": ES}
        ES = pd.DataFrame(ES)
        
        # Drawdown
        Roll_Max = prices.cummax()
        Daily_Drawdown = (prices/Roll_Max - 1.0)
        Max_Daily_Drawdown = Daily_Drawdown.cummin()
        
        Daily_Drawdown = abs(Daily_Drawdown)
        Max_Daily_Drawdown = abs(Max_Daily_Drawdown)
                          
        
        #Key Ratios
        key_ratios.columns= ["Name", "ABBN.S", "ADEN.S", "ALCC.S", "CSGN.S", "GEBN.S", "GIVN.S", 
                             "LHN.S", "LONN.S", "NESN.S", "NOVN.S", "CFR.S", "ROG.S", "SGSN.S",
                             "SIKA.S", "UHR.S", "SLHN.S", "SRENH.S", "SCMN.S", "UBSG.S", "ZURN.S"]
        
        key_ratios_clean = key_ratios["NESN.S"]
        price_earnings_ratio = key_ratios_clean.iloc[4]
        
        # price/book ratio
        price_book_ratio = key_ratios_clean.iloc[5]
        
        # return on equity ratio
        return_on_equity_ratio = key_ratios_clean.iloc[12]
        
        # Dividend yield - indicated annual dividend divided by closing price
        dividend_yield_ratio = key_ratios_clean.iloc[8]
        
        # debt to ratio
        debt_equity_ratio = key_ratios_clean.iloc[20]
        
    
        # =============================================================================
        #Sort all analysis from above to get dataframes which are used on the webpage for the tables and figures
        
        #Overview: Data for Figure Annual Performance
        Data = {'Date':  [lastmonth,lastyear, last3years, last5years, last10years],
                'Price': [cum_return_last_month.Price, cum_return_last_year.Price, cum_return_last_3years.Price, cum_return_last_5years.Price, cum_return_last_10years.Price],
                }
        
        self.df_annual_perf = pd.DataFrame(Data, columns = ['Date','Price'])
        
        #Table Price Performance
        Data_Price_Performance = {
            'Name':  ["Placeholder"],
            '1 month':  [cum_return_last_month.Price],
            '1 Years': [cum_return_last_year.Price],
            '3 Years': [cum_return_last_3years.Price],
            '5 Years': [cum_return_last_5years.Price],
            '10 Years': [cum_return_last_10years.Price],
            'Since Inception': [cum_return_all.Price],
            }
    
        self.df_Price_Performance = pd.DataFrame(Data_Price_Performance, columns = ['1 month','1 Years', '3 Years', '5 Years', '10 Years', 'Since Inception'])
        
        #Overview: Hypothetical Growth   
        V2007 = investment.iloc[r_size-3-days_last_year*12].Price
        V2008 = investment.iloc[r_size-3-days_last_year*11].Price
        V2009 = investment.iloc[r_size-3-days_last_year*10].Price
        V2010 = investment.iloc[r_size-3-days_last_year*9].Price
        V2011 = investment.iloc[r_size-3-days_last_year*8].Price
        V2012 = investment.iloc[r_size-3-days_last_year*7].Price
        V2013 = investment.iloc[r_size-3-days_last_year*6].Price
        V2014 = investment.iloc[r_size-3-days_last_year*5].Price
        V2015 = investment.iloc[r_size-3-days_last_year*4].Price
        V2016 = investment.iloc[r_size-3-days_last_year*3].Price
        V2017 = investment.iloc[r_size-3-days_last_year*2].Price
        V2018 = investment.iloc[r_size-3-days_last_year].Price
        V2019 = investment.iloc[r_size-3].Price
        
        hypothetical_growth = {'Date':  ['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019'],
                'Value': [10000,V2007, V2008,V2009,V2010,V2011,V2012,V2013,V2014,V2015,V2016,V2017,V2018,V2019]
                }
        
        self.df_hypothetical_growth = pd.DataFrame(hypothetical_growth, columns = ['Date','Value'])
        
        #Overview: Figure Average Annual Performance
        annual_perf_average = {'Date':  [lastmonth,lastyear, last3years, last5years, last10years],
                       'Price': [average_return_last_month.Price*252, average_return_last_year.Price*252, average_return_last_3years.Price*252, average_return_last_5years.Price*252, average_return_last_10years.Price*252],
                       }

        self.df_annual_perf_average = pd.DataFrame(annual_perf_average, columns = ['Date','Price'])
        
        
        #Overview: igure Risk Potential
        #Define quantiles for Graph
        q0=-1.854444201294828
        q1=-0.8269888130616426
        q2=0.22536003249425604
        q3=0.6619326773878177
        q4=1.1356494832642325
        SR = sharpe_ratio_last_year.Price * math.sqrt(252)
        
        #Define Values for Figure
        if (SR< q1):
            self.SR_q = 0.09
        elif (SR >= q1 and SR< q2):
            self.SR_q = 0.29
        elif (SR >= q2 and SR < q3):
            self.SR_q = 0.49
        elif (SR >= q3 and SR < q4):
            self.SR_q = 0.69
        elif (SR >= q4):
            self.SR_q = 0.89
         
        
        Data_Current_Statistic = {"Name": ["Price change yesterday",  "Average Annual Return", "Average daily Volatility","1 Year Volatilty", "1 Year Sharpe Ratio"],
           "Numbers": [round(float(price_change_yesterday.values[0]),2),  round(average_return_all.Price*252* 100, 2).astype(str) + '%', round(vola_last_year.Price,3), round(vola_last_year.Price * math.sqrt(252),3), round(sharpe_ratio_last_year.Price * math.sqrt(252),3)]
             }
        
        self.df_Current_Statistic = pd.DataFrame(Data_Current_Statistic, columns = ["Name", "Numbers"])
        
        
        #Price Performance: Table Historic Prices
        Avg_price = pd.DataFrame.mean(prices)
        Data_Historic_Prices = {"Name": ["Current Price", "Price Last Year", "Average Price","Year High", "Year Low"],
               "Numbers": [prices_today.Price.iloc[0],prices_last_year.Price.iloc[0], Avg_price.Price, year_high.Price, year_low.Price]
                 }
        
        self.df_Historic_Prices = pd.DataFrame(Data_Historic_Prices, columns = ["Name", "Numbers"])        
        self.df_Historic_Prices.Numbers = round(self.df_Historic_Prices.Numbers , 2)
    
    
        #Price Performance: Figure Price Development
        date_data_clean = pd.DataFrame(date_data)
        date_data_clean["Prices"] = prices
        
        self.df_Performance_Graph = date_data_clean
        
        #Price Performance: Figure returns 
        date_data_clean2 = pd.DataFrame(date_data)
        date_data_clean2["Returns"] = returns
        
        self.df_Return_Graph = date_data_clean2
        
                    
        #Price Performance: Key Ratios
        Data_Key_Ratios = {"Name": ["Price Earnings Ratio", "Price Book Ratio", "Return on Equity","Debt Equity Ratio", "Dividend Yield Ratio",],
        "Numbers": [round(price_earnings_ratio,2), round(price_book_ratio,2), round(return_on_equity_ratio,2), round(debt_equity_ratio* 100, 2).astype(str) + '%', round(dividend_yield_ratio* 100, 2).astype(str) + '%']
         }

        self.df_Key_Ratios = pd.DataFrame(Data_Key_Ratios, columns = ["Name", "Numbers"])
        
        #Risk Measures: Table 1
        Data_Risk_Measures1 = {"Name": [ "Sharpe Ratio last year", "Sharpe Ratio Total", "Daily Drawdown", "Max Daily Drawdown"],
                               "Numbers": [round(sharpe_ratio_last_year.Price * math.sqrt(252),2), round(sharpe_ratio_all.Price *math.sqrt(r_size),2), round(Daily_Drawdown.Price.iloc[-1]* 100, 2).astype(str) + '%',  round(Max_Daily_Drawdown.Price.iloc[-1]* 100, 2).astype(str) + '%']
                               }

        self.df_Risk_Measure1 = pd.DataFrame(Data_Risk_Measures1, columns = ["Name", "Numbers"])
        
        #Risk Measures: Table 2
        Data_Risk_Measures2 = {"Name": [ "Historic Value at Risk","Simulated Value at Risk", "Parametic Value at Risk","Expected Shortfall"],
                               "Numbers": [ round(float(HistVar.values[0]),4), round(SimVar,4), round(Covar_Var.Price,4) , round(float(ES.values[0]),4)]
         }

        self.df_Risk_Measure2 = pd.DataFrame(Data_Risk_Measures2, columns = ["Name", "Numbers"])
        
        
        #Risk Measures: Value at Risk        
        data_VaR = pd.DataFrame(df_HistVar, columns = ["Name"])
        data_VaR = data_VaR[::-1].reset_index()
        data_VaR = data_VaR.drop(['index'], axis=1)
        Date_VaR = pd.DataFrame(date_data.iloc[days_last_year:r_size]).reset_index()
        Date_VaR = Date_VaR.drop(['index'], axis=1)
        Date_VaR["Price"] = data_VaR
        self.df_VaR = Date_VaR

        
        #Risk Measures: Expected Shortfall
        Data_ES = pd.DataFrame(data_ES, columns = ["Name"])
        Data_ES = Data_ES[::-1].reset_index()
        Data_ES = Data_ES.drop(['index'], axis=1)
        Date_ES = pd.DataFrame(date_data.iloc[days_last_year:r_size]).reset_index()
        Date_ES = Date_ES.drop(['index'], axis=1)
        Date_ES["Price"] = Data_ES
        self.df_ES = Date_ES
                        
        
         #Risk Measures: Drawdown
        date_data_clean1 = pd.DataFrame(date_data)
        date_data_clean1["Max_DD"] = Max_Daily_Drawdown
        date_data_clean1["DD"] = Daily_Drawdown
        date_data_clean1["Roll_Max"] = Roll_Max
        self.df_Max_Daily_Drawdown = date_data_clean1
        
        
        #Technical
        b = prices.Price
        bollinger_mavg = ta.bollinger_mavg(b)
        bollinger_hband = ta.bollinger_hband(b)
        bollinger_lband = ta.bollinger_lband(b)
        bollinger_hband_indicator = ta.bollinger_hband_indicator(b)
        bollinger_lband_indicator=ta.bollinger_lband_indicator(b)
        
        rsi = ta.rsi(b)
        aroon_up = ta.aroon_up(b)
        aroon_down = ta.aroon_down(b)
        
        #Technical Analysis: Table Technical Analysis
        aroon_up_today = aroon_up.values[r_size-2]
        aroon_down_today = aroon_down.values[r_size-2]
        if (aroon_up_today  > aroon_down_today):
            if (aroon_up_today > 50):
                aroon_text = 'The Aroon Indicator detects a current strong upwards trend'
            else:
                aroon_text = 'The Aroon Indicator detects a current weak upwards trend'
        else:
            if (aroon_down_today > 50):
                aroon_text = 'The Aroon Indicator detects a current strong downwards trend'
            else:
                aroon_text = 'The Aroon Indicator detects a current weak downwards trend'
        
        
        rsi_today = rsi.values[r_size-2]
        if (rsi_today  > 70):
            rsi_text = 'The Relative Strength Index detects a current overvaluation of the stock'
        elif(rsi_today > 30 and rsi_today <70):
            rsi_text = 'The Relative Strength Index detects no current overvaluation or undervaluation of the stock'    
        else:
            rsi_text = 'The Relative Strength Index detects a current undervaluation of the stock'
      
        bollinger_hband_indicator_today = bollinger_hband_indicator.values[r_size-2]
        bollinger_lband_indicator_today = bollinger_lband_indicator.values[r_size-2]
        if (bollinger_hband_indicator_today  > bollinger_lband_indicator_today):
            bollinger_text = 'The Bollinger Band Oscillator detects that the current price is higher than the higher Bollinger Band and therefore recommends a buy of the stock'
        elif(bollinger_lband_indicator_today > 0):
            bollinger_text = 'The Bollinger Band Oscillator detects that the current price is lower than the lower Bollinger Band and therefore recommends  a selling of the stock'
        else:
            bollinger_text = 'The Bollinger Band Oscillator detects that the current price is between the lower and higher Bollinger Band and therefore recommends no trading activities in the stock'



        TechnicalAnalysis = {"Name": [ "Boolinger Band:", "Relative Strength Index:", "Aroon Indicator:"],
       "Implications": [bollinger_text, rsi_text, aroon_text]
         }

        self.df_TechnicalAnalysis= pd.DataFrame(TechnicalAnalysis, columns = ["Name", "Implications"])
        

        #Technical Analyis: Figure Bollinger
        Date_Bollinger = pd.DataFrame(date_data)
        Date_Bollinger["mavg"] = bollinger_mavg
        Date_Bollinger["hband"] = bollinger_hband
        Date_Bollinger["lband"] = bollinger_lband
        self.df_BollingerBands = Date_Bollinger
        
        #Technical Analyis: Figure RSI
        Date_RSI = pd.DataFrame(date_data)
        Date_RSI["RSI"] = rsi
        
        df_RSI = Date_RSI.drop(Date_RSI.index[0:14]).reset_index()
        self.df_RSI = df_RSI.drop(['index'], axis=1)
        
        #Technical Analyis: Figure Aroon
        Date_aroon = pd.DataFrame(date_data)
        Date_aroon["aroon_up"] = aroon_up
        Date_aroon["aroon_down"] = aroon_down
        self.df_AroonIndicator = Date_aroon
                



