import pygame

class Bullet:
    def __init__(self, x, y, speed, direction):
        self.x=x
        self.y=y

        self.start_x = x
        self.start_y = y

        self.width=5
        self.height=5
        self.speed=speed
        self.direction=direction
    
    def update(self):
        if self.direction == "up":
            self.y -= self.speed
        if self.direction == "down":
            self.y += self.speed
        if self.direction == "left":
            self.x -= self.speed
        if self.direction == "right":
            self.x += self.speed
            
    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)