import pygame
from tank import Tank

class Player(Tank):
    def handle_movement(self, keys, screen_width, screen_height):
        if keys[pygame.K_w] and self.y - self.speed > 0:
            self.y -= self.speed
            self.direction="up"
        if keys[pygame.K_s] and self.y + self.height + self.speed < screen_height:
            self.y += self.speed
            self.direction="down"
        if keys[pygame.K_a] and self.x - self.speed > 0:
            self.x -= self.speed
            self.direction="left"
        if keys[pygame.K_d] and self.x + self.width + self.speed < screen_width:
            self.x += self.speed
            self.direction="right"