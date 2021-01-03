class EventQueue():
    '''
    A basic queue class, written more as an exercise in basic datastructures 
    than anything functional/anything better than the Python provided queue 
    class.
    '''

    def __init__(self,data=[]):
        self.data = data
    
    def enqueue(self,x):
        self.data.append(x)
    def dequeue(self,x)
        self.data.pop(0)

    def is_empty(self)
        return not self.data