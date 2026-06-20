import pygame
from classes.tank import Tank

class Player(Tank):
    def handle_movement(self, keys, screen_width, screen_height):
        up = keys[pygame.K_w] or keys[pygame.K_UP]
        down = keys[pygame.K_s] or keys[pygame.K_DOWN]
        left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        right = keys[pygame.K_d] or keys[pygame.K_RIGHT]

        pressed = sum([up, down, left, right])
        if pressed != 1:
            return
        if up and self.y - self.speed > 0:
            self.y -= self.speed
            self.direction="up"
        if down and self.y + self.height + self.speed < screen_height:
            self.y += self.speed
            self.direction="down"
        if left and self.x - self.speed > 0:
            self.x -= self.speed
            self.direction="left"
        if right and self.x + self.width + self.speed < screen_width:
            self.x += self.speed
            self.direction="right"