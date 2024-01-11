import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import matplotlib.pyplot as plt
from IPython.display import display
#import warnings
#warnings.simplefilter(action='ignore', category=FutureWarning)
pd.get_option("display.max_rows")
pd.set_option("display.max_rows",999)

class Call:

    def __init__(self):
        options = Options()
        options.add_argument("headless")
        options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options = options)
        time.sleep(3)


    def checkSymbol(self, symbol):
        symbol = self.df.loc[self.df['Symbol'] == symbol.upper()]
        self.symbol = symbol
        if symbol.empty:
            return 'There is no such symbol on the top 100 currently.'
        return symbol
    
    def timeAnalysis(self, stockSymbol): #Makes a table for the historical analysis of a stock.
            url = f"https://finance.yahoo.com/quote/{stockSymbol}/history"
            self.driver.get(url)
            self.driver.refresh()
            #self.driver.send_keys(Keys.CONTROL + Keys.END)


            html = self.driver.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table')
            df = pd.read_html(html.get_attribute('outerHTML'))
            df = pd.DataFrame(df[0], columns = ['Date','Open','High','Low','Close*','Adj Close**','Volume'])
            self.driver.quit()

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
        df = df.sort_values(by = ['Change'], ascending = False)

        ''', columns = ['Symbol','Name','Price (Intraday)','Change','% Change','Volume','Avg Vol (3 month)','Market Cap', 'PE Ratio (TTM)','52 Week Range']'''
        # Add into line above if there are misinterpretations.
        
        self.driver.quit()

        df.to_csv('Files\\Gainer.csv', index = True)
        return df
    

'''#caller = Call()

#print(caller.dfCreateSel())
#print(caller.checkSymbol('nvda'))
#print(caller.timeAnalysis('AMD'))
#print(caller.checkSymbol('))

#historyTable = caller.timeAnalysis('ROKU')
#print(historyTable)
#plt.plot(historyTable['Close*'])
#plt.show()

plt.figure(figsize=(15,5))
plt.plot(historyTable['Close*'])
plt.title('Close price.', fontsize=15)
plt.ylabel('Price in dollars.')
plt.show()'''