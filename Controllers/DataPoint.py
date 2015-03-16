'''
Data point class used for data storage in memory and statistic manipulation. 
'''

class DataPoint :
    # === Defaults ===
    time_stamp = 0
    last = 0
    high = 0
    low = 0
    volume = 0
    bid = 0
    ask = 0
    # === Initialization ===
    def __init__(self,args):
        self.time_stamp = args[0]#UNIX timestamp
        self.last = args[1] # last BTC price
        self.high = args[2]# last 24 hours price high
        self.low = args[3]# last 24 hours price low
        self.volume = args[4] # last 24 hours volume
        self.bid = args[5]# highest buy order
        self.ask = args[6]# lowest sell order
                                                