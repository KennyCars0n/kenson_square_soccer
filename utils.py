from settings import *
import pygame as pg


#Object 
class Map:
    def __init__(self, filename):
        #Creates an empty list for map data
        self.data = []
        #Opens a specific file and closes with 'with'
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        #Properties of Map that allow us to define length and width
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * 32
        self.height = self.tileheight * 32

        

# This class can be used to create a Cooldown
class Cooldown:
    def __init__(self, time):
        self.start_time = 0
        self.time = time
    def start(self):
        self.start_time = pg.time.get_ticks()
    def ready(self):
        # sets current time to 
        current_time = pg.time.get_ticks()
        # if the difference between current and start time are greater than self.time
        # return True
        if current_time - self.start_time >= self.time:
            return True
        return False
        
    