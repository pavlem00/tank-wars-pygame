import pygame
from tank import Tank
import random

class Enemy(Tank):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.current_movement = random.choice(["up", "down", "left", "right"])
        
        self.state="wander"
        self.last_seen_x = None
        self.last_seen_y = None
        
        self.hit_wall = False
        self.last_direction_change=0
        self.direction_change_cooldown=1000
    
        self.combat_direction = None
    #random movement
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

    #helper function
    def in_sight(self, player, walls):
        x1 = self.x + self.width // 2
        y1 = self.y + self.height // 2

        x2 = player.x + player.width // 2
        y2 = player.y + player.height // 2

        for wall in walls:
            if wall.rect.clipline(x1, y1, x2, y2):
                return False
        
        return True
    
    #helper move function
    def move(self, screen_width, screen_height, walls):
        old_x = self.x
        old_y = self.y 

        if self.direction == "up" and self.y - self.speed > 0:
            self.y -= self.speed
        elif self.direction == "down" and self.y + self.height + self.speed < screen_height:
            self.y += self.speed
        elif self.direction == "left" and self.x - self.speed > 0:
            self.x -= self.speed
        elif self.direction == "right" and self.x + self.width + self.speed < screen_width:
            self.x += self.speed

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.x = old_x
                self.y = old_y
                self.hit_wall = True
                return
    


    #small AI enemy movement
    def enemy_upgraded_movement(self, player, walls, enemy_bullets, screen_width, screen_height):
        current_time = pygame.time.get_ticks()
        attack_distance = 200
        too_close = 60
        player_in_sight = self.in_sight(player, walls)
        
        if self.hit_wall:
            self.state = "wander"
            self.direction = random.choice(["up", "down", "right", "left"])
            self.hit_wall = False

        #state switching
        if self.state == "wander":
            if player_in_sight:
                self.last_seen_x = player.x
                self.last_seen_y = player.y
                self.state = "attack"
        elif self.state == "attack":
            if player_in_sight:
                self.last_seen_x = player.x
                self.last_seen_y = player.y
            else:
                self.state = "search"
        elif self.state == "search":
            if player_in_sight:
                self.state = "attack"

        #wandering      
        if self.state == "wander":
            if current_time - self.last_direction_change >= self.direction_change_cooldown:
                self.direction = random.choice(["up", "down", "left", "right"])
                self.last_direction_change = current_time

            self.move(screen_width, screen_height, walls)

        #attacking
        elif self.state == "attack":
            dx = player.x - self.x
            dy = player.y - self.y

            distance = ((dx**2) + (dy**2)) ** 0.5

            if distance > attack_distance:
                self.combat_direction = None
                if abs(dx) > abs(dy):
                    if dx > 0:
                        self.direction = "right"
                    else:
                        self.direction = "left"
                else:
                    if dy > 0:
                        self.direction = "down"
                    else:
                        self.direction = "up"
                self.move(screen_width, screen_height, walls)
                return
            
            if distance < too_close:
                self.combat_direction = None
                if abs(dx) > abs(dy):
                    if dx > 0:
                        self.direction = "left"
                    else:
                        self.direction = "right"
                else:
                    if dy > 0:
                        self.direction = "up"
                    else:
                        self.direction = "down"
                self.move(screen_width, screen_height, walls)
                return
            
            if self.combat_direction is None:
                if abs(dx) > abs(dy):
                    self.combat_direction = random.choice(["up", "down"])
                else:
                    self.combat_direction = random.choice(["left", "right"])

            self.direction = self.combat_direction
            self.move(screen_width, screen_height, walls)

            if current_time - self.last_shot_time >= self.shot_cooldown:
                if abs(dx) > abs(dy):
                    if dx > 0:
                        self.direction = "right"
                    else:
                        self.direction = "left"
                else:
                    if dy > 0:
                        self.direction = "down"
                    else:
                        self.direction = "up"
                self.shoot(current_time, enemy_bullets)
                
                if abs(dx) > abs(dy):
                    self.combat_direction = random.choice(["up", "down"])
                else:
                    self.combat_direction = random.choice(["left", "right"])
        #searching
        elif self.state == "search":
            dx = self.last_seen_x - self.x
            dy = self.last_seen_y - self.y

            distance = ((dx**2) + (dy**2)) ** 0.5

            if distance < 10:
                self.state = "wander"
                return

            if abs(dx) > abs(dy):
                if dx > 0:
                    self.direction = "right"
                else:
                    self.direction = "left"
            else:
                if dy > 0:
                    self.direction = "down"
                else:
                    self.direction = "up"

        
            self.move(screen_width, screen_height, walls)