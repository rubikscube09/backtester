class Event():
    '''
    Base class for all of the different types of events that can happen in a 
    trading environment.

    '''
    def __init__(self,type_=None):
        self.type_ = type_

class MarketEvent(Event):
    def __init___(self):
        super().__init__(type_='MARKET')
    
class SignalEvent(Event):
    '''
    Handles the event of a signal, for example a price crossing over a moving 
    average. 

    Attributes:
        symbols : (list str)
            Symbols on which indicator is computed.
        indicator : indicator
            Indicator being calculated
        date_time : (datetime)
            Date and time on which indicator event occurs.

    '''


    def __init__(self, symbol, direction, date_time):
        super().__init__(type_ = 'SIGNAL')
        self.symbol = symbol
        self.direction = direction
        self.date_time = date_time
        
        

class OrderEvent(Event):
    '''
    Handles the event of sending an order to a brokerage or order execution 
    system. Currently supports long or short orders, and market or limit orders. 

    Attributes:
        symbol : (str)
            Symbol of product being ordered.
        order_type : (str)
            Type of order, eg limit, market, stop-loss, etc.
        quantity : (int)
            Number of units (shares, contracts etc.) being ordered.
        direction : (str)
            Long or Short order.
        date_time : (str)
            Time at which order is placed/becomes active. 
    
    '''

    def __init__(self, symbol, order_type, quantity, direction, date_time):
        super().__init__(type_ = 'ORDER')
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity       
        self.direction = direction 
        self.date_time = date_time

    def print_order(self):
        '''
        Helper method to print orders.
        '''
        order = self.direction + self.symbol + self.direction + ' at ' + self.date_time
        print(order)

class FillEvent(Event):
    '''
    Handles the event in which an order placed using the OrderEvent is filled. 

    Attributes: 
        order : (OrderEvent)
            Order that was filled.
        date_time : (datetime)
            Date and time of fill. 
        fill_price : (float)
            Price at which order filled. Note that this assumes the entire order 
            fills at once, which may or may not be realistic.
        commision : (float)
            Comission that is paid for each transaction. 
           
    '''
    def __init__(self, order, date_time, fill_price, comission_structure = None):
        super().__init__(type_='FILL')
        self.order = order
        self.fill_price = fill_price
        self.date_time = date_time
        self.commissions = (self.compute_commisions(comission_structure) if comission_structure else 0)

    def compute_comissions(self, comission_structure='IB_FIXED'):
            # Interactive Brokers fixed comissions structure.
            # Minimum comissions paid is the maximum of 1 dollar, or .005 for each 
            # share traded. Maximum comissions is  the minimum of 1 percent of 
            # cash spent on the order, or the previously calculated qty.
        comissions = max(1,.005*self.order.quantity)
        comissions = min(comissions,.01*self.order.quantity*self.fill_price)
        return comissions

    


