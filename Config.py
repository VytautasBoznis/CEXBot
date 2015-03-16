'''
Config handling
'''
import os

#===== Config File Info =====
config_path = os.path.dirname(os.path.realpath(__file__)) + "\configs"
file_name = "configs.cfg"

if not os.path.exists(config_path):
    os.makedirs(config_path)

#===== Config Values =====
STATUS_REPORT_INTERVAL = 60 #Used for info reporting to logs
NUM_OF_DATA_POINTS_IN_USE = 180 #The number of data points to keep in memory
NUM_TO_GROUP_DATA_POINTS = 6#The number of data points to group for calculations
NUM_STREAK_BUY_START = 3#The number of times the price must change to the better for buying to sell
NUM_STREAK_SELL_START = 3#The number of times the price must change to the worse for buying to sell
NUM_OF_BALANCE_TO_USE = 0.5#Number of balance to use in trades (MAX) in percent
#===== Login Data =====
API_USERNAME = "ideolt"
API_SECRET = "jLGfTJte8HQ4xpLy55BzJtGCG8"
API_KEY = "0FvLEqtLmCFetCMY7D4FRw6vefw"