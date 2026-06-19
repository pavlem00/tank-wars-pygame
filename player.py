import pygame
from tank import Tank

class Player(Tank):
    def handle_movement(self, keys, screen_width, screen_height):
        up = keys[pygame.K_w]
        down = keys[pygame.K_s]
        left = keys[pygame.K_a]
        right = keys[pygame.K_d]

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