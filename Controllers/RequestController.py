'''
Cex.io API request controler
'''

import Config
import logging
import time
import json
from Controllers import LogController
from Controllers.cexapi.cexapi import API

class RequestController:
    api = (API)
    logg = (LogController)
    
    def __init__(self,logger):
        self.api = API(Config.API_USERNAME,Config.API_KEY,Config.API_SECRET)
        self.logg = logger
        
    def tick_data(self):
        ticker = json.loads(self.api.ticker(couple ='GHS/BTC'))
        
        data = []
        data.append(ticker.get("timestamp"))
        data.append(ticker.get("last"))
        data.append(ticker.get("high"))
        data.append(ticker.get("low"))
        data.append(ticker.get("volume"))
        data.append(ticker.get("bid"))
        data.append(ticker.get("ask"))
        return data
    
    def get_balance(self):
        ticker = json.loads(self.api.balance())
        
        data = []
        data.append(ticker.get("BTC").get("available"))
        data.append(ticker.get("BTC").get("orders"))
        data.append(ticker.get("GHS").get("available"))
        data.append(ticker.get("GHS").get("orders"))
        return data
    
    def order_sell(self,price=0.0,amount=1):
        self.api.place_order('sell', amount, price, 'GHS/BTC')
    
    def order_buy(self,price=0.0,amount=1):
        self.api.place_order('buy', amount, price, 'GHS/BTC')
        

        
