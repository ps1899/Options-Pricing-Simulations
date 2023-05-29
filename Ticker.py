import datetime
import requests_cache
import matplotlib.pyplot as plt
from pandas_datareader import data as wb

class Ticker:

    @staticmethod
    def getHistoricalData(ticker, startDate = None, endDate = None, cacheData = True, cacheDays = 1):
        try:
            expire_after = datetime.timedelta(days = 1)
            session = requests_cache.CachedSession(cache_name = 'cache', backend = 'sqlite', expire_after = expire_after)
            session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Accept': 'application/json;charset = utf-8'}
            if(startDate is not None and endDate is not None):
                data = wb.DataReader(ticker, dataSource = 'yahoo', start = startDate, end = endDate, session = session)
            else:
                data = wb.DataReader(ticker, dataSource = 'yahoo', session = session)
    
            if data is None:
                return None
            return data
        
        except Exception as e:
            print(e)
            return None
        
    @staticmethod
    def getColumns(data):
        if(data is None):
            return None
        return [column for column in data.columns]
    
    @staticmethod
    def getLastPrice(data, columnName):
        if data is None or columnName is None:
            return None
        if columnName not in Ticker.getColumns(data):
            return None
        return data[columnName].iloc[len(data) - 1]
    
    @staticmethod
    def plotData(data, ticker, columnName):
        try:
            if data is None:
                return
            data[columnName].plot()
            plt.xlabel('Date')
            plt.ylabel(f'{columnName}')
            plt.title(f'Historical data for {ticker} - {columnName}')
            plt.legend(loc = 'best')
            plt.show()
        
        except Exception as e:
            print(e)
            return