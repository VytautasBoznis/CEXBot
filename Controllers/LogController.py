import logging
import time
import os

#====== Directory creation ======
log_path = os.path.dirname(os.path.realpath(__file__)) + "\logs"
file_name = "CEXBot_log_"+time.strftime("%Y_%b_%d_%Hh_%Mm_%Ss")+".log"

# Used to keep everything in one file,
# the logging formating will not be handled here.
# The format should be kept as:
# LEVEL:CLASS_NAME:DATE:Message
class Log_Controller:
   
    def __init__(self):
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        #====== Logger initialization ======
        logging.basicConfig(filename = os.path.join(log_path, file_name),level=logging.DEBUG)
    
    def get_logger(self,name):
        return logging.getLogger(name);