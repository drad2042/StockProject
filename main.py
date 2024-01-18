from Caller import Call

import matplotlib.pyplot as plt
import pandas as pd
import os
c = Call()

def main():
    stockSymbol = input("Input the ticker of the stock you want to analyze: ")
    stockSymbol = stockSymbol.upper()
    
    temp = c.timeAnalysis(stockSymbol) 
    temp = pd.read_csv(f'Files\\History\\{stockSymbol}\\{stockSymbol}MaxHistory.csv')

    plt.figure(figsize = (30,18))
    plt.plot(temp['Date'],temp['Close*'])
    plt.title(f"{stockSymbol} Stock History")
    plt.xlabel("Share Price (USD)")
    plt.ylabel("Date")
    plt.xticks([])
    #plt.tight_layout()
    plt.show()
main()