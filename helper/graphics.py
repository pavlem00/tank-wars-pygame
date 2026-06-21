import pygame

screen_width = 800
screen_height = 600

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

def update_bullets(bullets):
    for bullet in bullets:
        bullet.update()

    for bullet in bullets[:]:
        if bullet.y <= 0 or bullet.y >= screen_height or bullet.x <= 0 or bullet.x >= screen_width:
                bullets.remove(bullet)


def bullet_wall_col(bullets, walls):
    for bullet in bullets[:]:
        for wall in walls:
            if bullet.rect.colliderect(wall.rect):
                bullets.remove(bullet)
                break

def draw(screen, player, player_bullets, enemy, enemy_bullets, walls, 
         grass_img, wall_img, blue_tank_img, red_tank_img, bullet_img, text1 ,text2):
    
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

        screen.blit(bullet_rotate, (draw_x, draw_y))
    for wall in walls:
        screen.blit(wall_img, (wall.rect.x, wall.rect.y))
   
    player_health_text=pygame.font.SysFont('comicsans', 30).render(
        text1+ str(player.health), 1, (255,255,255)
    )
    screen.blit(player_health_text, (10,screen_height-40))
    
    enemy_health_text=pygame.font.SysFont('comicsans', 30).render(
        text2+str(enemy.health), 1, (255,255,255)
    )
    screen.blit(enemy_health_text, (10, screen_height-20))


def draw_result(screen, game_result, text3, text4):
    color = (0,0,0)
    if game_result == "WIN":
        color = (0,0,255)
        text=pygame.font.SysFont('comicsans', 60).render(
            text3, 1, color
        )
    else:
        color = (255,0,0)
        text=pygame.font.SysFont('comicsans', 60).render(
            text4, 1, color
        )
    screen.blit(text, (screen_width//2-text.get_width()//2, screen_height//2-text.get_height()//2))
    text_quit=pygame.font.SysFont('comicsans', 60).render("Press Q to quit!", 1, color)
    screen.blit(text_quit, (screen_width//2-text_quit.get_width()//2, screen_height//2-text.get_height()//2+100))

