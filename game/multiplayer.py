import pygame

from classes.player import Player
from helper.map_generator import(
    grid_size, grid_to_walls, generate_grid, player_spawn, enemy_spawn, tank_offset
)
from helper.damage_handle import deal_damage
from helper.graphics import (update_bullets, bullet_wall_col,
                              draw_result, draw) 

screen_width = 800
screen_height = 600

blue_controls = {
    "up" : [pygame.K_UP],
    "down" : [pygame.K_DOWN],
    "left" : [pygame.K_LEFT],
    "right" : [pygame.K_RIGHT]
}

red_controls = {
    "up" : [pygame.K_w],
    "down" : [pygame.K_s],
    "left" : [pygame.K_a],
    "right" : [pygame.K_d]
}

text1 = "BLUE HP: "
text2 = "RED HP: "
text3 = "BLUE WINS! Press R to restart"
text4 = "RED WINS! Press R to restart"

def reset_game():
    grid = generate_grid()
    walls = grid_to_walls(grid)

    player1 = Player(player_spawn[0]*grid_size + tank_offset, 
                    player_spawn[1]*grid_size + tank_offset,
                    blue_controls,
                    "up")
    player2 = Player(enemy_spawn[0]*grid_size + tank_offset, 
                     enemy_spawn[1]*grid_size + tank_offset,
                     red_controls,
                     "down")

    return player1, player2, walls


def multiplayer_game(screen, grass_img, wall_img, blue_tank_img, red_tank_img, bullet_img):
    clock = pygame.time.Clock()

    player1, player2, walls = reset_game()

    player1_bullets = []
    player2_bullets = []

    game_result = None

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "MENU"
                if event.key == pygame.K_r:
                    player1, player2, walls = reset_game()
                    
                    player1_bullets.clear()
                    player2_bullets.clear()

                    game_result = None
                if event.key == pygame.K_BACKSPACE:
                    current_time = pygame.time.get_ticks()
                    player1.shoot(current_time, player1_bullets)
                if event.key == pygame.K_SPACE:
                    current_time = pygame.time.get_ticks()
                    player2.shoot(current_time, player2_bullets)
        if game_result is None:
            keys_pressed = pygame.key.get_pressed()

            old_x1 = player1.x
            old_y1 = player1.y

            player1.handle_movement(keys_pressed, screen_width, screen_height)

            for wall in walls:
                if player1.rect.colliderect(wall.rect):
                    player1.x=old_x1
                    player1.y=old_y1
                    break

            old_x2 = player2.x
            old_y2 = player2.y

            player2.handle_movement(keys_pressed, screen_width, screen_height)

            for wall in walls:
                if player2.rect.colliderect(wall.rect):
                    player2.x=old_x2
                    player2.y=old_y2
                    break
            
            if player1.rect.colliderect(player2.rect):
                player1.x=old_x1
                player1.y=old_y1
                player2.x=old_x2
                player2.y=old_y2

            update_bullets(player1_bullets)
            update_bullets(player2_bullets)

            bullet_wall_col(player1_bullets, walls)
            bullet_wall_col(player2_bullets, walls)

            for bullet in player1_bullets[:]:
                if bullet.rect.colliderect(player2.rect):
                    deal_damage(bullet, player2)
                    player1_bullets.remove(bullet)
            
            if player2.health <= 0:
                player2.health = 0
                game_result="WIN"

            for bullet in player2_bullets[:]:
                if bullet.rect.colliderect(player1.rect):
                    deal_damage(bullet, player1)
                    player2_bullets.remove(bullet)

            if player1.health <= 0:
                player1.health = 0
                game_result="LOSS"

        draw(screen, player1, player1_bullets, player2, player2_bullets, walls, 
                grass_img, wall_img, blue_tank_img, red_tank_img, bullet_img, text1, text2)
        if game_result:
                draw_result(screen, game_result, text3, text4)
        pygame.display.flip()