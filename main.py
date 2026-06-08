import pygame
from tank import Tank
from player import Player
from bullet import Bullet
from enemy import Enemy
from wall import Wall
pygame.init()


screen_width=800
screen_height=600



#Screen and objects draw function
def draw(screen, player, player_bullets, enemy, enemy_bullets, walls):
    screen.fill((0,100,0))
    pygame.draw.rect(screen, (0,0,255), (player.x, player.y, player.width, player.height))
    pygame.draw.rect(screen, (255,0,0), (enemy.x, enemy.y, enemy.width, enemy.height))
    
    for bullet in player_bullets:
        pygame.draw.rect(screen, (255,255,0), (bullet.x, bullet.y, bullet.width, bullet.height))
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, (255,255,0), (bullet.x, bullet.y, bullet.width, bullet.height))
    for wall in walls:
        pygame.draw.rect(screen, (78,78,78), wall.rect)
   
    player_health_text=pygame.font.SysFont('comicsans', 30).render(
        "Player HP: "+ str(player.health), 1, (255,255,255)
    )
    screen.blit(player_health_text, (10,screen_height-40))
    
    enemy_health_text=pygame.font.SysFont('comiscsans', 30).render(
        "CPU HP: "+str(enemy.health), 1, (255,255,255)
    )
    screen.blit(enemy_health_text, (10, screen_height-20))

   
    pygame.display.flip()

#result text draw on screen
def draw_result(screen, game_result):
    if game_result == "WIN":
        text=pygame.font.SysFont('comicsans', 60).render(
            "YOU WIN!", 1, (0, 0, 255)
        )
    else:
        text=pygame.font.SysFont('comicsans', 60).render(
            "GAME OVER!", 1, (255, 0, 0)
        )
    screen.blit(text, (screen_width//2-text.get_width()//2, screen_height//2-text.get_height()//2))
    pygame.display.flip()
    pygame.time.delay(3000)


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
    
    player=Player(400, 300)
    enemy=Enemy(100, 100)
    player_bullets=[]
    enemy_bullets=[]
    walls = [Wall(200, 200), Wall(240, 200), Wall(280, 200), Wall(400,100,40,160)]
    clock=pygame.time.Clock()



    run = True
    game_result=None
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_time=pygame.time.get_ticks()
                    player.shoot(current_time, player_bullets)
                    

        keys_pressed=pygame.key.get_pressed()
        
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

        enemy.enemy_movement(screen_width, screen_height)

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
                enemy.health-=25
                player_bullets.remove(bullet)

        

        if enemy.health <= 0:
            print("YOU WIN")
            game_result="WIN"
            run = False


        current_time=pygame.time.get_ticks()
        enemy.shoot(current_time, enemy_bullets)

        for bullet in enemy_bullets[:]:
            if bullet.rect.colliderect(player.rect):
                player.health -= 25
                enemy_bullets.remove(bullet)

        if player.health <= 0:
            print("GAME OVER")
            game_result="LOSS"
            run = False

        draw(screen, player, player_bullets, enemy, enemy_bullets, walls)
        if game_result:
            draw_result(screen, game_result)
    pygame.quit()


if __name__ == "__main__":
    main()  