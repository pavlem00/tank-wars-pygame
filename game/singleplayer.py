import pygame
from classes.player import Player
from classes.enemy import Enemy
from helper.map_generator import(
    grid_size, grid_to_walls, generate_grid, player_spawn, enemy_spawn, tank_offset
)
from helper.damage_handle import deal_damage
from helper.graphics import (update_bullets, bullet_wall_col, draw, draw_result)

screen_width = 800
screen_height = 600

singleplayer_controls = {
    "up" : [pygame.K_w, pygame.K_UP],
    "down" : [pygame.K_s, pygame.K_DOWN],
    "left" : [pygame.K_a, pygame.K_LEFT],
    "right" : [pygame.K_d, pygame.K_RIGHT]
}

text1 = "PLAYER HP: "
text2 = "CPU HP: "
text3 = "YOU WIN! Press R to restart"
text4 = "GAME OVER! Press R"





def reset_game():
    grid = generate_grid()
    walls = grid_to_walls(grid)

    player = Player(player_spawn[0]*grid_size + tank_offset, 
                    player_spawn[1]*grid_size + tank_offset,
                    singleplayer_controls)
    enemy = Enemy(enemy_spawn[0]*grid_size + tank_offset, enemy_spawn[1]*grid_size + tank_offset)

    return player, enemy, walls



def singleplayer_game(screen, grass_img, wall_img, blue_tank_img, red_tank_img, bullet_img):
    clock = pygame.time.Clock()

    player, enemy, walls = reset_game()

    player_bullets = []
    enemy_bullets = []

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
                    player, enemy, walls = reset_game()
                    
                    player_bullets.clear()
                    enemy_bullets.clear()

                    game_result = None
                if event.key == pygame.K_SPACE:
                    current_time = pygame.time.get_ticks()
                    player.shoot(current_time, player_bullets)
        if game_result is None:
            keys_pressed = pygame.key.get_pressed()

            old_x = player.x
            old_y = player.y

            player.handle_movement(keys_pressed, screen_width, screen_height)

            for wall in walls:
                if player.rect.colliderect(wall.rect):
                    player.x=old_x
                    player.y=old_y
                    break

            old_ex=enemy.x
            old_ey=enemy.y

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
                    deal_damage(bullet, enemy)
                    player_bullets.remove(bullet)
            
            if enemy.health <= 0:
                enemy.health = 0
                game_result="WIN"

            for bullet in enemy_bullets[:]:
                if bullet.rect.colliderect(player.rect):
                    deal_damage(bullet, player)
                    enemy_bullets.remove(bullet)

            if player.health <= 0:
                player.health = 0
                game_result="LOSS"

        draw(screen, player, player_bullets, enemy, enemy_bullets, walls, 
                grass_img, wall_img, blue_tank_img, red_tank_img, bullet_img, text1, text2)
        if game_result:
                draw_result(screen, game_result, text3, text4)
        pygame.display.flip()
            