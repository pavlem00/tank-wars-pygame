from collections import deque
import random
from classes.wall import Wall

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