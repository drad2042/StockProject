import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#from bs4 import BeautifulSoup
import time
import matplotlib.pyplot as plt
#from IPython.display import display
#import plotly.express as px
import os
import dask.dataframe as dd
from dask.distributed import Client

pd.get_option("display.max_rows")
pd.set_option("display.max_rows",999)

class Call:

    def __init__(self):
        options = Options()
        options.add_argument("headless")
        options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options = options)
        self.stockSymbol = None
        time.sleep(2)


    def checkSymbol(self, symbol):
        symbol = self.df.loc[self.df['Symbol'] == symbol.upper()]
        self.symbol = symbol
        if symbol.empty:
            return 'There is no such symbol on the top 100 currently.'
        return symbol
    





    def timeAnalysis(self, stockSymbol = input("Input the ticker of the stock you want to analyze: ")): #Makes a table for the historical analysis of a stock.        
        stockSymbol = stockSymbol.upper()
        self.stockSymbol = stockSymbol

        period = input('Which time period do you want to see the time for? (1Y, 5Y, Max) ')
        
        if period == '1Y':
            url = f"https://finance.yahoo.com/quote/{stockSymbol}/history?period1=1673481600&period2=1705017600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
        elif period == '5Y':
            url = f"https://finance.yahoo.com/quote/{stockSymbol}/history?period1=1547251200&period2=1705017600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
        elif period == 'Max':
            url = f"https://finance.yahoo.com/quote/{stockSymbol}/history?period1=322099200&period2=1705449600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
        
        self.period = period
        self.driver.get(url)
        self.driver.refresh()

        ## Find the buttons to click for time period.
        '''button = self.driver.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div')
        button.click()
        fiveYearButton = self.driver.find_element(By.XPATH, '//*[@id="dropdown-menu"]/div/ul[2]/li[3]/button')
        fiveYearButton.click()
        applyButton = self.driver.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button')
        applyButton.click()
        '''
        time.sleep(2)



        while True: #Continuously scroll to bottom of the page
            current_height = self.driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
            self.driver.execute_script(f"window.scrollTo(0, {current_height});")
            time.sleep(1)
            new_height = self.driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
            if new_height == current_height:
                break
        
        self.title = self.driver.find_element(By.XPATH, '//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1')
        self.title = self.title.get_property("innerHTML")

        html = self.driver.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table')
        df = pd.read_html(html.get_attribute('outerHTML'))
        df = pd.DataFrame(df[0], columns = ['Date','Open','High','Low','Close*','Adj Close**','Volume'])
        #df = df.drop_duplicates(subset = 'Date', keep = 'first')

        df["Open"] = pd.to_numeric(df["Open"], errors = 'coerce')
        df = df.dropna(subset = ["Open"])
        df = df.drop(df.tail(1).index)
        df = df.iloc[::-1]
        self.driver.quit()

        folderPath = f"Files\\History\\{stockSymbol}"
        if not os.path.exists(folderPath):
            os.mkdir(f"Files\\History\\{stockSymbol}")
        
        df.to_csv(f'Files\\History\\{stockSymbol}\\{stockSymbol}{period}History.csv')
        return df
        #return df[['Date','High','Low', 'Close*']]
            


    def top100Table(self): #Creates a dataframe using Selenium for the top 100 most active stocks.
        url = 'https://finance.yahoo.com/most-active/?count=100'
        self.driver.get(url)
        self.driver.refresh()
        time.sleep(2)
        
        html = self.driver.find_element(By.XPATH, '//*[@id="scr-res-table"]/div[1]/table')
        
        df = pd.read_html(html.get_attribute('outerHTML'))
        df = pd.DataFrame(df[0], columns = ['Symbol','Name','Price (Intraday)','Change','% Change','Volume','Avg Vol (3 month)','Market Cap', 'PE Ratio (TTM)','52 Week Range'])
        self.top100 = df
        
        self.driver.quit()
        
        df.to_csv('Files\\Top100.csv', index = True)
        return df
    

    def gainerTable(self): #Creates a dataframe for the highest gainers today.
        url = 'https://finance.yahoo.com/gainers/'
        self.driver.get(url)
        self.driver.refresh()

        html = self.driver.find_element(By.XPATH, '//*[@id="scr-res-table"]/div[1]/table')
        df = pd.read_html(html.get_attribute('outerHTML'))
        df = pd.DataFrame(df[0])
        df = df.drop(columns = ['52 Week Range'])
        #df['% Change'] = df['% Change'].str.replace('%','')
        df = df.sort_values(by = ['Change'], ascending = False)
        df = df.reset_index(drop = True)
        ''', columns = ['Symbol','Name','Price (Intraday)','Change','% Change','Volume','Avg Vol (3 month)','Market Cap', 'PE Ratio (TTM)','52 Week Range']'''
        # Add into line above if there are misinterpretations.
        
        self.driver.quit()

        df.to_csv('Files\\Gainer.csv', index = True)
        return df
    
    def graphMaker():
        pass
