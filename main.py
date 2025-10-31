#Importing from other libaries
import math
import random
import sys
import pygame as pg
from settings import *
from sprites import *
from os import path
from utils import *

class Game:
    def __init__(self):
        pg.init()
        #Time
        self.clock = pg.time.Clock()
        #Screen resolution
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        #Printng Text
        pg.display.set_caption("Game")
        self.playing = True
    #Sets up a game foler directory path using the current folder containting this file
    #Gives the game class a map property which uses the map class to parse the level1.txt file
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, 'map.txt'))

    def new(self):
        self.load_data()
        #The sprite Group allows us to uptdate and draw sprite in grouped batches
        self.all_sprites = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coin = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_players = pg.sprite.Group()
        self.all_balls = pg.sprite.Group()
        for row, tiles, in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    #Creataing a tile on every tile '1'
                    Wall(self, col, row, "")
                elif tile == 'C':
                    #Creating a coin on every tile 'C'
                    Coin(self, col, row,)    
                elif tile == 'P':
                    #Instanciation of a Player in the variable self.player
                    self.player = Player(self, col, row)
                elif tile == 'M':
                    #Creating a mob on every tile 'M'
                    Mob(self, col, row)
                elif tile == 'B':
                    self.ball = Ball(self, col, row)
                                    
                    
    def run(self):
        while self.playing == True:
            self.dt = self.clock.tick(FPS) / 1000
            #Input
            self.events()
            #Process
            self.update()
            #Output
            self.draw()    
        pg.quit()
    def events(self):
        for event in pg.event.get():
            #Exiting the game
            if event.type == pg.QUIT:
                self.playing = False
            #Action after pressing the mouse button

    def update(self):
        #Refreshing the sprites
        self.all_sprites.update()
        seconds = pg.time.get_ticks()//1000
        countdown = 10
        self.time = countdown - seconds
    def draw_text(self, surface, text, size, color, x, y):
        #Font
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
    def draw(self):
        #BG color
        self.screen.fill(WHITE)
        #Displaying health on the screen 
        self.draw_text(self.screen, str(self.player.health), 24, BLACK, 100, 100)
        #Displaying score on the screen
        self.draw_text(self.screen, str(self.player.coins), 24, BLACK, 400, 100)
        self.draw_text(self.screen, str(self.time), 24, BLACK, 700, 100 )
        #Adding all of the sprites
        self.all_sprites.draw(self.screen)
        pg.display.flip()

 #Creating an instance of the Game class
if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
