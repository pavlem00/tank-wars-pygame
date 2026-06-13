import pygame
from tank import Tank
from player import Player
from bullet import Bullet
from enemy import Enemy
from wall import Wall
import random
from collections import deque
pygame.init()

#Screen dimensions
screen_width=800
screen_height=600

#map dimensions
grid_size=40
cols=screen_width//grid_size
rows=screen_height//grid_size

player_spawn=(18, 13)
enemy_spawn=(1,1)
tank_offset=(grid_size-30)//2


#Checking spawn zone, so no walls generate in player/enemy spawning zone
def check_spawn_zone(x, y):
    px, py = player_spawn
    ex, ey = enemy_spawn

    if abs(x-px) <= 2 and abs(y-py) <= 2:
        return True

    if abs(x-ex) <= 2 and abs(y-ey) <= 2:
        return True
    
    return False


#Helper function to check if path between enemy and player exists
#Walls should not block path between enemy and player
#Practically BFS algorithm
def path_check(grid):
    queue = deque()
    queue.append(enemy_spawn)

    visited=set()
    visited.add(enemy_spawn)

    directions=[(1,0),(-1,0),(0,1),(0,-1)]
    
    while len(queue) > 0:
        current=queue.popleft()

        x=current[0]
        y=current[1]

        if x == player_spawn[0] and y == player_spawn[1]:
            return True
        
        for direction in directions:
            dx = direction[0]
            dy = direction[1]

            nx = x + dx
            ny = y + dy

            if nx < 0 or nx >= cols:
                continue

            if ny < 0 or ny >= rows:
                continue

            if grid[ny][nx] == 1:
                continue

            if (nx, ny) in visited:
                continue

            visited.add((nx,ny))
            queue.append((nx,ny))

    return False

#Helper function for grid generator
#Generating grid for walls, but checking if path between player and enemy exists
def generate_grid():
    while True:

        grid=[]

        for y in range(rows):
            row = []
            for x in range(cols):
                row.append(0)
            grid.append(row)

        for y in range(rows):
            for x in range(cols):
                if check_spawn_zone(x, y):
                    continue
            

                chance=random.random()

                if chance < 0.25:
                    grid[y][x] = 1
                
        if path_check(grid):
            return grid


def grid_to_walls(grid):
    walls = []

    for y in range(rows):
        for x in range(cols):
            
            if grid[y][x] == 1:
                wall_x=x*grid_size
                wall_y=y*grid_size

                wall = Wall(wall_x, wall_y, grid_size, grid_size)

                walls.append(wall)
        
    return walls



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
            draw(screen, player, player_bullets, enemy, enemy_bullets, walls)
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
            game_result="WIN"


        current_time=pygame.time.get_ticks()
        enemy.shoot(current_time, enemy_bullets)

        for bullet in enemy_bullets[:]:
            if bullet.rect.colliderect(player.rect):
                player.health -= 25
                enemy_bullets.remove(bullet)

        if player.health <= 0:
            game_result="LOSS"

        draw(screen, player, player_bullets, enemy, enemy_bullets, walls)
        if game_result:
            draw_result(screen, game_result)

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()  