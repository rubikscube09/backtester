import event
import numpy as np
import pandas as pd 
import yfinance as yf
import datetime as dt
import quandl

class DataHandler():

    '''
    An abstract class (supposedly) that provides the framework for datahandling 
    in a backtest. The data handling for specific data sources is provided in 
    subclasses.
    '''
    def get_latest_bars(self, symbols, num_bars=1):
        '''
        Get the latest set of num_bars from the provided dataset of a given 
        symbol.

        Arguments:
            symbol : (str)
                Symbols whose bars we need.
            num_bars : (int, default=1)
                Number of bars we want to access. 
        
        Return:
            Returns num_bars of the most recent bars.
        '''
        raise NotImplementedError("Need to implement get_latest_bars")
    def update_bars(self):
        '''

        '''
        raise NotImplementedError("Need to implement update_bars")

class YahooHandler(DataHandler):
    '''
    Data handling class for yahoofinance bars using the yfinance module.

    Attributes:
        symbols
    '''
    def __init__(self,symbols,events):
        self.symbols = symbols
        self.events = events
        self.symbol_data = {}
        self.end_of_data = False
        self.cols = ['Timestamp','Open','High','Low','Close','Volume']
        self.recent_data = {}
        self.gen_dict = {}

    def load_yahoo_data(self, start='1800-01-01', end=dt.date.today(),interval='1d'):
        '''
        Loads yahoo finance financial data using methods provided in the 
        yfinance module. 

        Parameters:
            start, end : (datetime) 
                Specifies the beginning and end range of history to be queried.
                Added support for periods coming soon (TM).
            interval : (str)
                Specifies the frequency at which data is collected. Default is 
                daily. 
        ''' 
        cols = self.cols
        symbols = self.symbols
        func = (yf.Tickers if len(symbols) > 1 else yf.Ticker)
        joined_sym = ' '.join(self.symbols)
        cols_to_ind = dict(zip(cols,range(len(cols))))
        data_multi_df = func(joined_sym).history(start=start, end=end, interval = interval)[cols[1:]]
        if len(symbols) > 1:
            for sym in symbols:
                self.symbol_data[sym] = data_multi_df.xs(sym,axis = 1, level = 1)
                self.symbol_data[sym]['Timestamp'] = self.symbol_data[sym].index
                self.symbol_data[sym] = self.symbol_data[sym][cols]
                self.symbol_data[sym] = self.symbol_data[sym].to_numpy()
        else:
            s = symbols[0]
            self.symbol_data[sym] = data_multi_df
            self.symbol_data[sym]['Timestamp'] = self.symbol_data[sym].index
            self.symbol_data[sym] = self.symbol_data[sym][cols]
            self.symbol_data[sym] = self.symbol_data[sym].to_numpy()
        self.create_gen()
    
    def create_gen(self):
        """
        Helper method to create generators for bars
        """
        for sym in self.symbols:
            self.gen_dict[sym] = self.get_bars(sym)

        #TODO - Forward fill missing data if there is any 

    def get_bars(self,symbol):
        '''
        Creates generator objects out of bars. This is useful for advancing
        '''
        for bar in self.symbol_data[symbol]:
            yield bar


    def get_latest_bars(self,symbol,num_bars = 1):
        '''
        Gets the latest bars received/known at a given time for a given symbol.
        '''
        return self.recent_data[sym][-num_bars:]

    def update_bars(self):
        '''
        Pushes new bars onto the recent_symbol_data structure, and "advances time"
        forward in the sense of the internal backtesting clock, by adding a MarketEvent 
        object onto the event queue (to be written)
        '''
        for sym in self.symbols:
            try:
                bar = next(self.gen_dict[sym])
            except StopIteration:
                self.end_of_data = True
            else:
                bar_prev = self.recent_data.get(sym)
                if bar_prev is not None:
                    self.recent_data[sym] = np.vstack([bar_prev,bar])
                else:
                    arr = np.ndarray(shape = (1,len(self.cols)),dtype = 'object')
                    arr[0] = bar
                    self.recent_data[sym] = arr
        