import pygame
from classes.bullet import Bullet

class Tank:
    def __init__(self, x, y, direction="up"):
        self.x=x
        self.y=y
        self.direction=direction
        
        self.health=100
        self.width=30
        self.height=30
        self.speed=3

        self.last_shot_time=0
        self.shot_cooldown=1500

    def shoot(self, current_time, bullets):
        if current_time - self.last_shot_time < self.shot_cooldown:
            return
        if self.direction == "up":
            bullets.append(Bullet(self.x+self.width//2, self.y, 5, self.direction))
        elif self.direction == "down":
            bullets.append(Bullet(self.x+self.width//2, self.y+self.height, 5, self.direction))
        elif self.direction == "left":
            bullets.append(Bullet(self.x, self.y+self.height//2, 5, self.direction))
        elif self.direction == "right":
            bullets.append(Bullet(self.x+self.width, self.y+self.height//2, 5, self.direction))
        self.last_shot_time=current_time
    
    def take_damage(self, damage):
        self.health -= damage

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)