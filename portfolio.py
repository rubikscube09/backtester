import datetime as dt
import event 

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

    def __init__(self, data_handler, events, start_date = dt.datetime.today() - dt.timedelta(days=365), end_date=dt.datetime.today(), starting_capital=10**6):
        '''
        Initializes a basic portfolio, as well as the data needed for running 
        the backtests. Also includes a start, end_date for the duration of testing. 
        Default interval is one year prior to the current date.
        
        '''
        self.data_handler = data_handler
        self.events = events
        self.start_date = start_date
        self.end_date  = end_date
        self.starting_capital = starting_capital
        self.symbols = self.data_handler.symbols

        self.position_history = self.initialize_position_history()
        self.current_positions = {sym:0 for sym in self.symbols}

        self.holding_history = self.initialize_holding_history()
        self.current_holdings = self.initialize_holding_history()[0]
        

    def initialize_position_history(self):
        position_history = {sym:0 for sym in self.symbols}
        position_history['Timestamp'] = self.start_date
        return [position_history] 

    def initialize_holding_history(self):
        holding_history = {sym:0 for sym in self.symbols}
        holding_history['Timestamp'] = self.start_date
        holding_history['Cash'] = self.starting_capital 
        holding_history['Comissions Paid'] = 0
        holding_history['Total'] = self.initial_capital
        return [holding_history]


    def update_fill(self, fill_event):
        '''
        Updates current positions and holdings if a fill event is found on the 
        queue.
        '''
        self.update_current_positions_fill(fill_event)
        self.update_current_holdings_fill(fill_event)

    def update_current_positions_fill(self,fill_event):
        '''
        Updates our position if we have an order filled, with the fill given by 
        the FillEvent. We assume that our entire order gets filled, and there are no 
        partial executions.
        '''
        fill_dir = (1 if fill_event.order.direction == 'LONG' else -1)
        self.current_positions[fill_event.order.symbol] += fill_event.order.quantity*fill_dir

    def update_current_holdings_fill(self,fill_event):
        '''
        Updates holdings due to a filled/cleared trade.
        '''
        symbol, quantity, direction = fill_event.order.symbol, fill_event.order.quantity, fill_event.direction
        fill_dir = (1 if direction == 'LONG' else -1)
        cost = -(fill_dir*quantity*fill_event.fill_price) #Receive cash for short positions, lose it for longs.
        comissions = fill_event.comissions()
        self.current_holdings['Cash'] -= (cost + comissions)
        self.current_holdings['Comissions Paid'] += comissions
        self.current_holdings['Total'] -= (cost + comissions)
        self.current_holdings[symbol] += cost


    def update_histories(self,market_event):
        """
        Updates current positions in the portfolio given a MarketEvent. This is
        not instantaneous, but instead one-step behind. Moreover, this does not
        update due to a fill, but instead adds the already existing current 
        positions to the portfolio along with a timestamp. Not sure where the 
        event fits in here ... 
        """

        # Advance the generator forward one step.
        bars = {}
        for sym in self.symbols:
            bars[sym] = self.data_handler.get_latest_bars(sym)
        
        pos_dict = self.current_positions
        timestamp = self.bars[self.symbols[0]][self.data_handler.cols_to_ind['Timestamp']]
        pos_dict['Timestamp'] = timestamp
        self.position_history.append(pos_dict)

        holdings_dict = self.current_holdings
        for sym in self.symbols:
            val = self.current_positions[sym]*bars[sym][self.data_handler.cols_to_ind['Close']] 
            holdings_dict[sym] = val
            holdings_dict['Total'] += val
        self.holding_history.append(holdings_dict)
    
    def create_simple_order(self,signal):
        '''
        Transacts an order event object given a signal.
        '''
        pos_size = 10 #TODO - FIND A WAY TO IMPLEMENT POSITION SIZING.
        symbol = signal.symbol
        direction = signal.direction
        order_type = 'MKT'

        current_qty = self.current_positions[symbol]
        order = event.OrderEvent(symbol, order_type, pos_size, direction, signal.date_time)
        return order
    
