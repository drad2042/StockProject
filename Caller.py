import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


class Caller:

    def __init__(self):
        options = Options()
        options.add_argument("headless")
        driver = webdriver.Chrome(options = options)
        

        driver.get('https://finance.yahoo.com/most-active/?count=100')
        driver.refresh()
        self.driver = driver
        #self.site = pd.read_html('https://finance.yahoo.com/most-active/?count=100')
        time.sleep(3)

    def createDf(self): #Function that creates a dataframe for the top 25 most active stocks of the day.
        df = pd.DataFrame(self.site[0],  columns = ['Symbol','Name','Price (Intraday)','Change','% Change','Volume','Avg Vol (3 month)','Market Cap', 'PE Ratio (TTM)','52 Week Range'])
        self.df = df
        return self.df

    def checkSymbol(self, symbol):
        symbol = self.df.loc[self.df['Symbol'] == symbol.upper()]
        self.symbol = symbol
        if symbol.empty:
            return 'There is no such symbol on the top 25 currently.'
        return symbol
    
    def timeAnalysis(self, stockSymbol): #Makes a table for the historical analysis of a stock.
            #For now this only uses stock symbols in the initial dataframe, needs to be changed.
            time.sleep(3)
            self.site2 = pd.read_html(f'https://finance.yahoo.com/quote/AMD/')
            #self.df2 = pd.DataFrame(site2[0], columns = ['Date','Open','High','Low','Close*','Adj Close**','Volume'])
            
            return self.site2

    
    def dfCreateSel(self):
        html = self.driver.find_element(By.XPATH, '//*[@id="scr-res-table"]/div[1]/table')
        df = pd.read_html(html.get_attribute('outerHTML'))
        df = pd.DataFrame(df[0], columns = ['Symbol','Name','Price (Intraday)','Change','% Change','Volume','Avg Vol (3 month)','Market Cap', 'PE Ratio (TTM)','52 Week Range'])
        self.df = df
        
        self.driver.quit()
        
        return df
    
        

caller = Caller()

print(caller.dfCreateSel())
print(caller.checkSymbol('nvda'))
#print(caller.checkSymbol('AMD'))
#print(caller.checkSymbol('))




