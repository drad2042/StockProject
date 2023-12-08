import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

'''driver = webdriver.Chrome()
driver.get('https://finance.yahoo.com/most-active/?count=100')
time.sleep(3)
driver.refresh()'''

newalltabs = pd.read_html('https://finance.yahoo.com/most-active/?count=100')
time.sleep(3)

df = pd.DataFrame(newalltabs[0],  columns = ['Symbol','Name','Price (Intraday)','Change','% Change','Volume','Avg Vol (3 month)','Market Cap', 'PE Ratio (TTM)','52 Week Range'])
print(df)

## Find the row where the Symbol is AMD.
AMD = df.loc[df['Symbol'] == 'AMD']

print(AMD)