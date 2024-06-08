import yfinance as yf
import pandas as pd





msft = yf.Ticker("MSFT")
msft.history(period = "max")





print((msft.dividends))