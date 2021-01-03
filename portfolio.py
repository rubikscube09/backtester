import datetime as dt

class Portfolio():

    def place_order(self,signal_event):
        '''
        Places an order for the portfolio given a passed in SignalEvent.
        '''
        raise NotImplementedError('Need to implement a place_order method')
    
    def update_fill(self,fill_event):
        '''
        Updates a portfolio if an order is filled - specified using a 
        FillEvent.
        '''
        raise NotImplementedError('Need to implement a update_fill method')

class BasicPortfolio(Portfolio):

    def __init__(self, data, events, start_date, end_date=dt.datetime.today(), starting_capital=10**6):
        '''
        Initializes a basic portfolio, as well as the data needed for running 
        the backtests. Also includes a start, end_date for the duration of testing. 

        '''
        self.data = data
        self.events = events
        self.start_date = start_date
        self.end_date  = end_date
        self.starting_capital = starting_capital
        self.symbols = self.data.symbols

        self.position_history = self.initialize_position_history()
        self.current_position = {sym:0 for sym in self.symbols}

        self.holding_history = self.initialize_holding_history()

        

    def initialize_position_history(self):
        position_history = {sym:0 for sym in self.symbols}
        position_history['Timestamp'] = self.start_date
        return [position_history]

