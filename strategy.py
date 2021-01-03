from event import SignalEvent
class Strategy():

    '''
    The main class for creating actual trading strategies, which consist of 
    going long or short respectively, which are signals received by a Portfolio
    class object. In particular, instances of any subclass generate
    SignalEvent objects. Any derived instances will recieve bars from the
    DataHandler class 
    '''
    
    def calculate_signals(self):
        raise NotImplementedError('Need to implement a calculate_signals method')


class BuyAndHold(Strategy):
    
    def __init__(self, data, events):
        self.data = data
        self.events = events
        self.cols_to_ind = self.data.cols_to_ind
        self.symbols = self.data.symbols

    def calculate_signals(self,event):
        if event.type_ = 'MARKET':
            for sym in self.symbols:
                bars = self.get_latest_bars(sym)
                if len(bars) > 0:
                    # Add in logic to check if it's bought.
                    ind = self.cols_to_ind['Timestamp']
                    signal = SignalEvent(symbol,'LONG',bars[-1][ind])
                    signal = self.events.enqueue(signal)