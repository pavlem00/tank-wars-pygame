import pygame
from tank import Tank
import random

class Enemy(Tank):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.current_movement = random.choice(["up", "down", "left", "right"])
        
        self.last_direction_change=0
        self.direction_change_cooldown=1000
    
    def enemy_movement(self, screen_width, screen_height):
        current_time=pygame.time.get_ticks()

        if current_time - self.last_direction_change >= self.direction_change_cooldown:
            self.direction = random.choice(["up", "down", "left", "right"])

            self.last_direction_change=current_time

        if self.direction == "up" and self.y - self.speed > 0:
            self.y -= self.speed
        elif self.direction == "down" and self.y + self.height + self.speed < screen_height:
            self.y += self.speed
        elif self.direction == "left" and self.x - self.speed > 0:
            self.x -= self.speed
        elif self.direction == "right" and self.x + self.width + self.speed < screen_width:
            self.x += self.speed