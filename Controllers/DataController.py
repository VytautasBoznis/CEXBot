'''
Data storage and statistic controller
'''
import time
import Config
import logging
from math import floor
from Controllers import LogController
from Controllers.DataPoint import DataPoint
from Controllers.RequestController import RequestController

grouped_stats = []    
last_buy_price = 0.0
last_sell_price = 0.0

class Statistics:
    logg = (LogController)
    #==== ACOUNT STATUS ======
    
    #==== BTC Data =====
    BTC_available = 0
    BTC_max_to_use_in_trades = 0
    BTC_orders = 0
        
    #==== GH/S Data =====
    GHS_available = 0
    GHS_orders = 0
    
    def __init__(self,data,log):
        logg = log
        self.BTC_available = data[0]
        self.BTC_orders = data[1]
        self.GHS_available = data[2]
        self.GHS_orders = data[3]
        
    def update_balance(self,data):
        self.BTC_available = data[0]
        self.BTC_orders = data[1]
        self.GHS_available = data[2]
        self.GHS_orders = data[3]
        
    #==== Market stats =====
    #Market status info:
    #ID:-1 - UNKNOWN -> Still calculating
    #ID:0 - HGHT DOWN -> Market price falling fast (2-3++x less then last difference) 
    #ID:1 - SLOW_DOWN -> Market price falling slow (0-1x less then last difference)
    #ID:2 - STOP -> Market price unchanged
    #ID:3 - SLOW_UP -> Market price going up slow (0-1x more then last difference)
    #ID:4 - HIGH_UP -> Market price going up fast (2-3++x more then last difference)
    
    BUY_MARKET_STATUS = -1
    SELL_MARKET_STATUS = -1

    sell_last_difference = 0.0
    sell_difference = 0.0
    
    buy_last_difference = 0.0
    buy_difference = 0.0
    
    #if the sign of market difference remains the same for (Config set amount of times) starts selling/
    sell_change_streak = 0
    buy_change_streak = 0
    BTC_both = False
    should_buy = False
    should_sell = False

    #==== Simulation results ====
    
    #in percent (might be - )
    profit_percent = 0.0
    #in units (BTC probably)
    total_profit = 0.0
    
    #what = 0 ->sell else its buy
    def calc_difference(self):
        last_id = grouped_stats.__len__()-1
            
        if(last_id < 1):
            return
            
        self.sell_last_difference = self.sell_difference
        self.sell_difference = grouped_stats[last_id].ask - grouped_stats[last_id-1].ask
         
    #what == 0 -> sell else its buy
    def find_market_status(self):
        #Streak calculations.
        if(self.sell_difference>self.sell_last_difference):
            self.buy_change_streak = 0
            self.sell_change_streak += 1
        elif(self.sell_difference<self.sell_last_difference):
            self.sell_change_streak = 0
            self.buy_change_streak +=1
               
        if(self.sell_difference >= 1):
            self.BUY_MARKET_STATUS = 4
        elif(self.sell_difference <= 1 and self.sell_difference >= 0.05):
            self.BUY_MARKET_STATUS = 3
        elif(self.sell_difference <= 0.05 and self.sell_difference >= -0.05):
            self.BUY_MARKET_STATUS = 2
        elif(self.sell_difference <= -0.5 and self.sell_difference >= -1):
            self.BUY_MARKET_STATUS = 1
        else:
            self.BUY_MARKET_STATUS = 0


    
    def update_stats(self):
        self.calc_difference()
        self.find_market_status()            
    
    def find_action(self):
        
        self.update_stats()
        
        if((self.BTC_both == True) and (self.sell_change_streak == Config.NUM_STREAK_SELL_START)):
            self.should_buy = True
        
        if((self.BTC_both == False) and (self.buy_change_streak == Config.NUM_STREAK_SELL_START)):
            self.should_sell = True
            
        if(self.BUY_MARKET_STATUS == 4):
            print(self.sell_difference)
            '''self.logg.log(logging.INFO,time.asctime()+": The price is rising extremely rapidly if the user has no assets now he should buy at (with minimum price up and HOLD)")
            self.logg.log(logging.INFO,last_buy_price)'''
        elif(self.BUY_MARKET_STATUS == 3):
            print(self.sell_difference)
            '''self.logg.log(logging.INFO,time.asctime()+": User should order buys")
            self.logg.log(logging.INFO,(last_buy_price-self.buy_difference).__str__()+" "+(last_buy_price))'''
        elif(self.BUY_MARKET_STATUS == 2):
            print(self.sell_difference)
            '''self.logg.log(logging.INFO,time.asctime()+": User should order buys")'''
        elif(self.BUY_MARKET_STATUS == 1):
            print(self.sell_difference)
            '''self.logg.log(logging.INFO,time.asctime()+": User should order buys")
            self.logg.log(logging.INFO,(last_buy_price-self.buy_difference)+" "+(last_buy_price))'''
        elif(self.BUY_MARKET_STATUS == 0):
            print(self.sell_difference)
            '''self.logg.log(logging.INFO,time.asctime()+": The price is falling extremely rapidly the user should not have any assets and wait (sell everything at minimum price with a little up)")'''

            
class Data_Controller:
    data_points = [] #used for active data point storage
    logg = (LogController)
    request_controller = (RequestController)
    stats = (Statistics)
    
    def __init__(self,logger,request_controller):
        self.logg = logger
        self.request_controller = request_controller
        self.stats = Statistics(self.request_controller.get_balance(),self.logg)
    
    def group_points(self):
        to = floor(self.data_points.__len__()/Config.NUM_TO_GROUP_DATA_POINTS)
        
        grouped_stats.clear()
        data_group = [0,0.0,0.0,0.0,0.0,0.0,0.0]
        
        for i in range(0,to):
            for j in range(0,Config.NUM_TO_GROUP_DATA_POINTS):
                data_point_id = (self.data_points.__len__() - (i*Config.NUM_TO_GROUP_DATA_POINTS)) - j -1
                data_group[0] += int(self.data_points[data_point_id].time_stamp)
                data_group[1] += float(self.data_points[data_point_id].last)
                data_group[2] += float(self.data_points[data_point_id].high)
                data_group[3] += float(self.data_points[data_point_id].low)
                data_group[4] += float(self.data_points[data_point_id].volume)
                data_group[5] += float(self.data_points[data_point_id].bid)
                data_group[6] += float(self.data_points[data_point_id].ask)
            
            data_group[0] /= Config.NUM_TO_GROUP_DATA_POINTS
            data_group[1] /= Config.NUM_TO_GROUP_DATA_POINTS
            data_group[2] /= Config.NUM_TO_GROUP_DATA_POINTS
            data_group[3] /= Config.NUM_TO_GROUP_DATA_POINTS
            data_group[4] /= Config.NUM_TO_GROUP_DATA_POINTS
            data_group[5] /= Config.NUM_TO_GROUP_DATA_POINTS
            data_group[6] /= Config.NUM_TO_GROUP_DATA_POINTS           
            
            grouped_stats.append(DataPoint(data_group))
            data_group = [0,0.0,0.0,0.0,0.0,0.0,0.0]
                
    def add_point(self):
        data = self.request_controller.tick_data()
        
        if(self.data_points.__len__() < Config.NUM_OF_DATA_POINTS_IN_USE):
            data_point = DataPoint(data)
            self.data_points.append(data_point)
            last_buy_price = data_point.bid 
            last_sell_price = data_point.ask      
        else:
            data_point = DataPoint(data)
            self.data_points.pop(0)
            self.data_points.append(data_point)
            last_buy_price = data_point.bid 
            last_sell_price = data_point.ask 
            
        self.group_points()
        self.stats.find_action()
        
        print("should buy: "+self.stats.should_buy.__str__())
        print("should sell: "+self.stats.should_sell.__str__())

        if(self.stats.should_buy):
            self.buy_all()
        elif(self.stats.should_sell):
            self.sell_all()
        
        
    def sell_all(self):
        data = self.request_controller.tick_data()
        price = float(data[1])
        amount = self.stats.BTC_available
        
        self.request_controller.order_sell(price,amount)
        self.stats.BTC_both = False
        print("Selling ALL")
        
    def buy_all(self):
        data = self.request_controller.tick_data()
        price = float(data[1])
        amount = self.stats.GHS_available
        
        self.buy_all(price,amount)
        self.stats.BTC_both = True
        print("Buying ALL")
