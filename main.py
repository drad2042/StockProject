from Caller import Call
from plotnine import ggplot, aes, geom_line
import matplotlib.pyplot as plt
import pandas as pd
import os
import time
import plotly.express as px
c = Call()

def main():
    startTime = time.time()

    temp = c.timeAnalysis() 
    temp = pd.read_csv(f'Files\\History\\{c.stockSymbol}\\{c.stockSymbol}{c.period}History.csv')
    #temp2 = pd.read_csv(f'Files\\History\\RBLX\\RBLXMaxHistory.csv')

    endTime = time.time()
    print(endTime - startTime)

    fig = px.line(temp, x = "Date", y = "Close*")
    fig.show()
    '''plt.figure(figsize = (30,18))
    plt.plot(temp['Date'], temp['Close*'])
    #plt.plot(temp2['Date'],temp2['Close*'])
    #plt.title(f"{c.title} Stock History")
    plt.xlabel("Date")
    plt.ylabel("Share Price (USD)")
    plt.xticks([])

    #mng = plt.get_current_fig_manager()
    #mng.full_screen_toggle()
    #plt.tight_layout()
    plt.show()'''
main()