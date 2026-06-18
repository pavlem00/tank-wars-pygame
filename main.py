import pygame
from tank import Tank
from player import Player
from bullet import Bullet
from enemy import Enemy
from wall import Wall
#import random
#from collections import deque
from map_generator import (generate_grid, grid_to_walls, player_spawn, enemy_spawn,
                           grid_size, tank_offset)
from damage_handle import deal_damage
pygame.init()

#Screen dimensions
screen_width=800
screen_height=600

#Screen and objects draw function
def draw(screen, player, player_bullets, enemy, enemy_bullets, walls, 
         grass_img, wall_img, blue_tank_img, red_tank_img):
    screen.blit(grass_img, (0,0))
    screen.blit(blue_tank_img, (player.x, player.y))
    screen.blit(red_tank_img, (enemy.x, enemy.y))
    
    for bullet in player_bullets:
        pygame.draw.rect(screen, (255,255,0), (bullet.x, bullet.y, bullet.width, bullet.height))
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, (255,255,0), (bullet.x, bullet.y, bullet.width, bullet.height))
    for wall in walls:
        screen.blit(wall_img, (wall.rect.x, wall.rect.y))
   
    player_health_text=pygame.font.SysFont('comicsans', 30).render(
        "Player HP: "+ str(player.health), 1, (255,255,255)
    )
    screen.blit(player_health_text, (10,screen_height-40))
    
    enemy_health_text=pygame.font.SysFont('comicsans', 30).render(
        "CPU HP: "+str(enemy.health), 1, (255,255,255)
    )
    screen.blit(enemy_health_text, (10, screen_height-20))


#result text draw on screen
def draw_result(screen, game_result):
    if game_result == "WIN":
        text=pygame.font.SysFont('comicsans', 60).render(
            "YOU WIN! Press R", 1, (0, 0, 255)
        )
    else:
        text=pygame.font.SysFont('comicsans', 60).render(
            "GAME OVER! Press R", 1, (255, 0, 0)
        )
    screen.blit(text, (screen_width//2-text.get_width()//2, screen_height//2-text.get_height()//2))


#Bullet moving update
def update_bullets(bullets):
    for bullet in bullets:
        bullet.update()

    for bullet in bullets[:]:
        if bullet.y <= 0 or bullet.y >= screen_height or bullet.x <= 0 or bullet.x >= screen_width:
                bullets.remove(bullet)


#Function that removes bullets after they hit the wall
def bullet_wall_col(bullets, walls):
    for bullet in bullets[:]:
        for wall in walls:
            if bullet.rect.colliderect(wall.rect):
                bullets.remove(bullet)
                break


    
def main():

    screen=pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tank Wars")
    grass_img = pygame.image.load("pictures/grass.png")
    grass_img = pygame.transform.scale(grass_img, (screen_width, screen_height))
    wall_img = pygame.image.load("pictures/wall.png").convert_alpha()
    wall_img = pygame.transform.scale(wall_img, (40,40))
    blue_tank_img = pygame.image.load("pictures/blue.png").convert_alpha()
    blue_tank_img = pygame.transform.scale(blue_tank_img, (40,40))
    red_tank_img = pygame.image.load("pictures/red.png").convert_alpha()
    red_tank_img = pygame.transform.scale(red_tank_img, (40,40))

    player=Player(player_spawn[0]*grid_size+tank_offset, player_spawn[1]*grid_size+tank_offset)
    enemy=Enemy(enemy_spawn[0]*grid_size+tank_offset, enemy_spawn[1]*grid_size+tank_offset)
    player_bullets=[]
    enemy_bullets=[]
    #walls = [Wall(200, 200), Wall(240, 200), Wall(280, 200), Wall(400,100,40,160)]
    grid=generate_grid()
    walls=grid_to_walls(grid)
    clock=pygame.time.Clock()



    run = True
    game_result=None
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid = generate_grid()
                    walls = grid_to_walls(grid)

                    player = Player(player_spawn[0]*grid_size+tank_offset, player_spawn[1]*grid_size+tank_offset)
                    enemy = Enemy(enemy_spawn[0]*grid_size+tank_offset, enemy_spawn[1]*grid_size+tank_offset)

                    player_bullets.clear()
                    enemy_bullets.clear()

                    game_result = None
                if event.key == pygame.K_SPACE:
                    current_time=pygame.time.get_ticks()
                    player.shoot(current_time, player_bullets)
                    

        keys_pressed=pygame.key.get_pressed()
        
        if game_result is not None:
            draw(screen, player, player_bullets, enemy, enemy_bullets, walls, grass_img, wall_img, blue_tank_img, red_tank_img)
            draw_result(screen, game_result)
            pygame.display.flip()
            continue


        old_x=player.x
        old_y=player.y
        
        player.handle_movement(keys_pressed, screen_width, screen_height)

        for wall in walls:
            if player.rect.colliderect(wall.rect):
                player.x=old_x
                player.y=old_y
                break

        old_ex=enemy.x
        old_ey=enemy.y

        #enemy.enemy_movement(screen_width, screen_height)
        enemy.enemy_upgraded_movement(player, walls, enemy_bullets, screen_width, screen_height)
        for wall in walls:
            if enemy.rect.colliderect(wall.rect):
                enemy.x=old_ex
                enemy.y=old_ey
                break


        if player.rect.colliderect(enemy.rect):
            player.x=old_x
            player.y=old_y
            enemy.x=old_ex
            enemy.y=old_ey


        update_bullets(player_bullets)
        update_bullets(enemy_bullets)


        bullet_wall_col(player_bullets, walls)
        bullet_wall_col(enemy_bullets, walls)
        
        for bullet in player_bullets[:]:
            if bullet.rect.colliderect(enemy.rect):
                deal_damage(player, enemy)
                player_bullets.remove(bullet)

        

        if enemy.health <= 0:
            enemy.health = 0
            game_result="WIN"


        #current_time=pygame.time.get_ticks()
        #enemy.shoot(current_time, enemy_bullets)

        for bullet in enemy_bullets[:]:
            if bullet.rect.colliderect(player.rect):
                deal_damage(enemy, player)
                enemy_bullets.remove(bullet)

        if player.health <= 0:
            player.health = 0
            game_result="LOSS"

        draw(screen, player, player_bullets, enemy, enemy_bullets, walls, 
             grass_img, wall_img, blue_tank_img, red_tank_img)
        if game_result:
            draw_result(screen, game_result)

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()  