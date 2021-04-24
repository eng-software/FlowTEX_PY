''' 
  Chronometer.py

    Created: 23/04/2021 17:49:00
    Author: henrique.coser
'''
import time

class Chronometer:
    elapsed = 0
    maxTime = 0
    running = False
    timeValue = 0

    #--------------------------------------------
    # Constructor
    #--------------------------------------------
    def __init__(self):
        self.elapsed = 0;
        self.timeValue = time.time()
        self.maxTime = 0;
        self.running = True;
    #--------------------------------------------
    # Start time counting
    #   - Reset the time statistic
    #--------------------------------------------
    def start(self):
        self.elapsed = 0;
        self.timeValue = time.time()
        self.maxTime = 0
        self.running = True
    #--------------------------------------------
    # Stop the time counting
    #   - Stop the counting and update time statistic
    #--------------------------------------------
    def stop(self):
        if(self.running):
            self.elapsed = time.time() - self.timeValue
            if(self.elapsed > self.maxTime):
                self.maxTime = self.elapsed;        
            self.running = False;
    #--------------------------------------------
    # Restart the time counting
    #   - Restart the counting update and keep time statistic
    #--------------------------------------------
    def restart(self):
        if(self.running):
            self.elapsed = time.time() - self.timeValue
            if(self.elapsed > self.maxTime):
                self.maxTime = self.elapsed;
        self.timeValue = time.time()
        self.running = True;
    #--------------------------------------------
    # Get the maximum elapsed time
    #   - Update the statistic an return the maximum elapsed time measured
    #--------------------------------------------
    def getMax(self):
        if(self.running):
            self.elapsed = time.time() - self.timeValue
            if(self.elapsed > self.maxTime):
                self.maxTime = self.elapsed;
        return self.maxTime;
    #--------------------------------------------
    # Get the elapsed time since start or restart
    #   - Update the statistic an return the elapsed time
    #--------------------------------------------
    def getElapsed(self):
        if(self.running):
            self.elapsed = time.time() - self.timeValue
            if(self.elapsed > self.maxTime):
                self.maxTime = self.elapsed;
        return self.elapsed;
