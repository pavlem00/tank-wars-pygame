import pygame
from classes.tank import Tank
from classes.player import Player
from classes.bullet import Bullet
from classes.enemy import Enemy
from classes.wall import Wall
from helper.map_generator import (generate_grid, grid_to_walls, player_spawn, enemy_spawn,
                           grid_size, tank_offset)
from helper.damage_handle import deal_damage
from menu import Menu
pygame.init()

#Screen dimensions
screen_width=800
screen_height=600

def rotate_img(img, direction):
    if direction == "up":
        return img
    elif direction == "down":
        return pygame.transform.rotate(img, 180)
    elif direction == "right":
        return pygame.transform.rotate(img, -90)
    elif direction == "left":
        return pygame.transform.rotate(img, 90)
    return img


#Screen and objects draw function
def draw(screen, player, player_bullets, enemy, enemy_bullets, walls, 
         grass_img, wall_img, blue_tank_img, red_tank_img, bullet_img):
    
    screen.blit(grass_img, (0,0))
    blue_tank = rotate_img(blue_tank_img, player.direction)
    screen.blit(blue_tank, (player.x, player.y))
    red_tank = rotate_img(red_tank_img, enemy.direction)
    screen.blit(red_tank, (enemy.x, enemy.y))
    
    for bullet in player_bullets:
        bullet_rotate = rotate_img(bullet_img, bullet.direction)
        
        bullet_center_x = bullet.x + bullet.width // 2
        bullet_center_y = bullet.y + bullet.height // 2
        draw_x = bullet_center_x - bullet_rotate.get_width() // 2
        draw_y = bullet_center_y - bullet_rotate.get_height() // 2

        screen.blit(bullet_rotate, (draw_x, draw_y))
    for bullet in enemy_bullets:
        bullet_rotate = rotate_img(bullet_img, bullet.direction)

        bullet_center_x = bullet.x + bullet.width // 2
        bullet_center_y = bullet.y + bullet.height // 2
        draw_x = bullet_center_x - bullet_rotate.get_width() // 2
        draw_y = bullet_center_y - bullet_rotate.get_height() // 2

        screen.blit(bullet_rotate, (bullet.x, bullet.y))
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
    color = (0,0,0)
    if game_result == "WIN":
        color = (0,0,255)
        text=pygame.font.SysFont('comicsans', 60).render(
            "YOU WIN! Press R to restart", 1, color
        )
    else:
        color = (255,0,0)
        text=pygame.font.SysFont('comicsans', 60).render(
            "GAME OVER! Press R", 1, color
        )
    screen.blit(text, (screen_width//2-text.get_width()//2, screen_height//2-text.get_height()//2))
    text_quit=pygame.font.SysFont('comicsans', 60).render("Press Q to quit!", 1, color)
    screen.blit(text_quit, (screen_width//2-text_quit.get_width()//2, screen_height//2-text.get_height()//2+100))

def draw_menu(screen, menu, grass_img, blue_tank_img, red_tank_img):
    screen.blit(grass_img, (0,0))
    
    title = pygame.font.SysFont("arialblack", 100).render("TANK WAR", 1, (255, 215, 0))
    blue_menu_tank = rotate_img(blue_tank_img, "left")
    red_menu_tank = rotate_img(red_tank_img, "right")
    blue_menu_tank = pygame.transform.scale(blue_menu_tank, (70,70))
    red_menu_tank = pygame.transform.scale(red_menu_tank, (70,70))
    screen.blit(title, (screen_width//2-title.get_width()//2, 50))
    screen.blit(red_menu_tank, (screen_width//2-title.get_width()//2-60,50))
    screen.blit(blue_menu_tank, (screen_width//2+title.get_width()//2,50))
    option_font = pygame.font.SysFont("arial", 40)
    option_y = 180

    i = 0
    for option in menu.options:
        if i == menu.selected:
            color = (255,255,255)
            text_value = "> " + option
        else:
            color = (120,120,120)
            text_value = option
        text = option_font.render(text_value, 1, color)
        screen.blit(text, (screen_width//2-text.get_width()//2, option_y + i*60))
        i = i + 1

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
    game_state = "MENU"
    menu = Menu()

    screen=pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tank War")
    grass_img = pygame.image.load("pictures/grass.png")
    grass_img = pygame.transform.scale(grass_img, (screen_width, screen_height))
    wall_img = pygame.image.load("pictures/wall.png").convert_alpha()
    wall_img = pygame.transform.scale(wall_img, (40,40))
    blue_tank_img = pygame.image.load("pictures/blue.png").convert_alpha()
    blue_tank_img = pygame.transform.scale(blue_tank_img, (40,40))
    red_tank_img = pygame.image.load("pictures/red.png").convert_alpha()
    red_tank_img = pygame.transform.scale(red_tank_img, (40,40))
    bullet_img = pygame.image.load("pictures/bullet.png").convert_alpha()
    bullet_img = pygame.transform.scale(bullet_img, (30, 30))

    player=Player(player_spawn[0]*grid_size+tank_offset, player_spawn[1]*grid_size+tank_offset)
    enemy=Enemy(enemy_spawn[0]*grid_size+tank_offset, enemy_spawn[1]*grid_size+tank_offset)
    player_bullets=[]
    enemy_bullets=[]
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

            if game_state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        menu.move_down()
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        menu.move_up()
                    elif event.key == pygame.K_RETURN:
                        choice = menu.get_selected()

                        if choice == "Singleplayer":
                            game_state = "SINGLEPLAYER"
                        elif choice == "Quit":
                            run = False
            if game_state == "SINGLEPLAYER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        grid = generate_grid()
                        walls = grid_to_walls(grid)

                        player = Player(player_spawn[0]*grid_size+tank_offset, player_spawn[1]*grid_size+tank_offset)
                        enemy = Enemy(enemy_spawn[0]*grid_size+tank_offset, enemy_spawn[1]*grid_size+tank_offset)

                        player_bullets.clear()
                        enemy_bullets.clear()

                        game_result = None
                    elif event.key == pygame.K_SPACE:
                        current_time=pygame.time.get_ticks()
                        player.shoot(current_time, player_bullets)
                    elif event.key == pygame.K_q:
                        game_state = "MENU"
        if game_state == "MENU":
                draw_menu(screen, menu, grass_img, blue_tank_img, red_tank_img)
                pygame.display.flip()
                continue            

        if game_state == "SINGLEPLAYER":
            keys_pressed=pygame.key.get_pressed()
            
            if game_result is not None:
                draw(screen, player, player_bullets, enemy, enemy_bullets, walls, grass_img, wall_img, blue_tank_img, red_tank_img, bullet_img)
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
                grass_img, wall_img, blue_tank_img, red_tank_img, bullet_img)
            if game_result:
                draw_result(screen, game_result)

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()  