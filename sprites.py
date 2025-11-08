#Sprite modules contain all the sprites
#Sprites include: player, mob - moving obj

import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import Cooldown
from random import randint
from random import choice
vec = pg.math.Vector2

#Player Sprite
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_players
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # self.rect.x = x * TILESIZE[0]
        # self.rect.y = y * TILESIZE[1]
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.speed = 250
        self.health = 100
        self.coins = 0
        self.cd = Cooldown(1000)
    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vel.y = -self.speed*self.game.dt
            # self.rect.y -= self.speed
            # self.bullet_direction = "up"
        if keys[pg.K_a]:
            self.vel.x = -self.speed*self.game.dt
            # self.rect.x -= self.speed
            # self.bullet_direction = "left"
        if keys[pg.K_s]:
            self.vel.y = self.speed*self.game.dt
            # self.rect.y += self.speed
            # self.bullet_direction = "down"  
        if keys[pg.K_d]:
            self.vel.x = self.speed*self.game.dt
            # self.rect.x += self.speed
            # self.bullet_direction = "right"
        # accounting for diagonal
        if self.vel[0] != 0 and self.vel[1] != 0:
            self.vel *= 0.7071
    def collide_with_walls(self, dir):
        # x axis
        if dir == 'x':
            #hits is colliding with walls
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                # print(self.pos)
                # moving forwards
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                        
                # moving backwards        
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                # hits[0].vel.x = 0
                self.rect.x = self.pos.x
        # y axis
        if dir == 'y':
            #hits is colliding with walls
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                # print(self.pos)
                # moving forwards
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.width
                        
                # moving backwards        
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                # hits[0].vel.y = 0
                self.rect.y = self.pos.y
    #Collision
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits: 
            # hitting a mob
            if str(hits[0].__class__.__name__) == "Mob":
                if self.cd.ready():
                    self.health -= 10
                    self.cd.start()
            # hitting the goal
            if str(hits[0].__class__.__name__) == "Goal":
                pass
            
            if str(hits[0].__class__.__name__) == "Ball":
                pass

    def update(self):
        # movement and collision
        self.get_keys()
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

        self.collide_with_stuff(self.game.all_mobs, False)
        self.collide_with_stuff(self.game.all_coin, True)
        self.collide_with_stuff(self.game.all_balls, False)

        # print(self.cd.ready())
        if not self.cd.ready():
            self.image.fill(BLUE)
            # print("not ready")
        else:
            self.image.fill(GREEN)
            # print("ready")

        # print("x" + str(self.pos.x))
        # print("y" + str(self.pos.y))
        # print(" ")

       
#Mob Sprite
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface(TILESIZE)
        #Coloring the Mob
        self.image.fill((RED))
        #Rectangle
        self.rect = self.image.get_rect()
        self.vel = vec(choice([-1,1]),choice([-1,1]))
        self.pos = vec(x,y)*TILESIZE[0]
        #Coordinates
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y * TILESIZE[1]
        #Speed
        self.speed = 4
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                # print(self.pos)
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.rect.x = self.pos.x
                self.vel.x *= choice([-1,1])
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.rect.y = self.pos.y
                self.vel.y *= choice([-1,1])
    
    def update(self):
        # mob behavior
        if self.game.ball.pos.x > self.pos.x:
            self.vel.x = 1
        else:
            self.vel.x = -1
        if self.game.ball.pos.y > self.pos.y:
            self.vel.y = 1
        else:
            self.vel.y = -1
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')


#Coin Sprite
class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coin
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface(TILESIZE)
        #Coloring the Mob
        self.image.fill(YELLOW)
        #Rectangle
        self.rect = self.image.get_rect()
        #Coordinates
        self.rect.x = x*TILESIZE[0]
        self.rect.y = y*TILESIZE[1]
    def update(self):
        #Coin behavior
        pass

#Wall Sprite
class Wall(Sprite):
    def __init__(self, game, x, y, state):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface(TILESIZE)
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.state = state
        # print("wall created at", str(self.rect.x), str(self.rect.y))
    def update(self):
        # wall
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

#Ball Sprite
class Ball(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        # self.rect.x = x * TILESIZE[0]
        # self.rect.y = y * TILESIZE[1]
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.speed = 250
        self.health = 100
        self.count = 0
        self.cd = Cooldown(1000)




    def collide_with_walls(self, dir):
        # x axis
        if dir == 'x':
            #hits is colliding with walls
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                #If it touches the coordinates that are the edges of the screen
                if  hits[0].rect.left == 0:
                    #Switches direction and adds a little speed to not be stuck on the wall
                    self.vel.x = self.vel.x * -1.02
                elif hits[0].rect.right == 1024:
                    self.vel.x = self.vel.x *-1.02
                
                # # print(self.pos)
                # # moving forwards
                # if self.vel.x > 0:
                #     self.pos.x = hits[0].rect.left - self.rect.width
                        
                # # moving backwards        
                # if self.vel.x < 0:
                #     self.pos.x = hits[0].rect.right
                # # hits[0].vel.x = 0
                # self.rect.x = self.pos.x
        # y axis
        if dir == 'y':
            #hits is colliding with walls
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                #Same as the x 
                if  hits[0].rect.top == 0:
                    self.vel.y = self.vel.y * -1.02
                elif hits[0].rect.bottom == 768:
                    self.vel.y = self.vel.y * -1.02
                #print(hits[0].rect.bottom)

                # # print(self.pos)
                # # moving forwards
                # if self.vel.y > 0:
                #     self.pos.y = hits[0].rect.top - self.rect.width
                        
                # # moving backwards        
                # if self.vel.y < 0:
                #     self.pos.y = hits[0].rect.bottom
                # # hits[0].vel.y = 0
                # self.rect.y = self.pos.y

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        self.initBallSpeed = 10
        if hits: 
            # hitting the player
            if str(hits[0].__class__.__name__) == "Player":
                #If the player and the ball are facing the same direction
                if self.vel.x * self.game.player.vel.x > 0:
                    #Moves in the opposite direction
                    self.vel.x = self.vel.x * -1
                else:
                    #If the player hits the ball
                    if self.game.player.vel.x > 0:
                        #Increase speed based on the player
                        self.vel.x = self.game.player.vel.x + self.initBallSpeed
                    elif self.game.player.vel.x < 0:
                        self.vel.x = self.game.player.vel.x - self.initBallSpeed
                    else: #If player isn't moving
                        self.vel.x = self.vel.x * -1
                # print("Player")
                # print(self.game.player.vel.x)
                # print(self.game.player.vel.y)
                # print("Ball")
                # print(self.vel.x)
                # print(self.vel.y)

                #Same as x
                if self.vel.y * self.game.player.vel.y > 0:
                    self.vel.y = self.vel.y * -1
                else:
                    if self.game.player.vel.y > 0:
                        self.vel.y = self.game.player.vel.y + self.initBallSpeed
                    elif self.game.player.vel.y < 0:
                        self.vel.y = self.game.player.vel.y - self.initBallSpeed
                    else:
                        self.vel.y = self.vel.y * -1
                

            # hitting the goal
            if str(hits[0].__class__.__name__) == "Goal":
                self.count += 1
                self.kill()
                

    def update(self):
        #Moving based on the velocity
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        #Collision with stuff
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

        self.collide_with_stuff(self.game.all_mobs, False)
        self.collide_with_stuff(self.game.all_players, False)
        self.collide_with_stuff(self.game.all_goals, False)


        self.slowdownRate = 0.2
        #Value close to 0 because it is hard for the ball to be percisely 0
        self.zero = 0.25
        #Slows down over time
        if self.vel.x > self.zero:
            self.vel.x -= self.slowdownRate
        elif self.vel.x < self.zero:
            self.vel.x += self.slowdownRate
        #If it is very close to 0, make it 0
        if abs(self.vel.x) <= self.zero:
            self.vel.x = 0
        #Same as x
        if self.vel.y > self.zero:
            self.vel.y -= self.slowdownRate
        elif self.vel.y < self.zero:
            self.vel.y += self.slowdownRate

        if abs(self.vel.y) <= self.zero:
            self.vel.y = 0

            # print("v-x:" + str(self.vel.x))
            # print("v-y:" + str(self.vel.y))
            # print("c-X:" + str(self.collideX))
            # print("c-y:" + str(self.collideY))

#Goal Sprite
#Basically the same as wall
class Goal(Sprite):
    def __init__(self, game, x, y, state):
        self.groups = game.all_sprites, game.all_goals
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface(TILESIZE)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.state = state
        # print("wall created at", str(self.rect.x), str(self.rect.y))
    def update(self):
        # goal
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

