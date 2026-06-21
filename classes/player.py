import pygame
from classes.tank import Tank

class Player(Tank):
    def __init__(self, x, y, controls, direction = "up"):
        super().__init__(x, y, direction)
        self.controls = controls
    def handle_movement(self, keys, screen_width, screen_height):
        up = any(keys[key] for key in self.controls["up"])
        down = any(keys[key] for key in self.controls["down"])
        left = any(keys[key] for key in self.controls["left"])
        right = any(keys[key] for key in self.controls["right"])

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