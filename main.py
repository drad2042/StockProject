from Caller import Call
from IPython.display import display, HTML
c = Call()

def main():
    temp = c.timeAnalysis('AMZN')
    print(temp)


main()