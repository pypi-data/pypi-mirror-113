class finvizStreamer():
    #Declare class variables
    #---------------------
    #declare dictionary (key:value)  to store ticker and associated html tables
    news_tables = {}
    #declare list (array) to store arrays of parsed data
    parsed_data = []
    tickers = []
    #---------------------
    #constructor
    def __init__(self):
        
        self.url = 'https://www.finviz.com/quote.ashx?t='
        #self.headers = {'Content-Type': 'application/json'}
 
    def scrape_finziz(self):
        from urllib.request import urlopen, Request
        import json
        from bs4 import BeautifulSoup
        import pandas as pd

        symbol = input('What is the symbol of the stock? (Please enter only one.)')

        finviz_url = 'https://www.finviz.com/quote.ashx?t='
        #tickers = ['NVDA', 'SLV', 'MU']
        tickers = [symbol]

        for ticker in tickers:
            url = self.url + ticker

            req = Request(url = url, headers = {'user-agent': 'my-app'})
            print ("request url:" +url)
            response = urlopen(req)

            html = BeautifulSoup(response, 'html')
            news_table = html.find(id = 'news-table')
            self.news_tables[ticker] = news_table
    

        for ticker, news_table in self.news_tables.items():
            for row in news_table.findAll('tr'):

                title = row.a.get_text()
                date_data = row.td.text.split(' ')

                if len(date_data) == 1: # if there is both a date and time it parses them into two columns
                    time = date_data[0]
                else: 
                    date = date_data[0] 
                    time = date_data[1]
                self.parsed_data.append([ticker, date, time, title])
        
        df = pd.DataFrame(self.parsed_data, columns = ['ticker', 'date', 'time', 'title'])  
        return df