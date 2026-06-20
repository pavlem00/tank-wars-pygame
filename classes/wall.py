import pygame

class Wall():
    def __init__(self, x, y, width=40, height=40):
        self.rect=pygame.Rect(x, y, width, height)
        