# TANK WAR

Tank war is 2D tank battle game developed in Python using Pygame.
The game features both Singleplayer and Multiplayer modes, algorithm-based map generation, enemy AI, collision detection, direction based damage mechanics, sound effects, and simple menu system.



## Singleplayer Mode

- Battle against an AI-controlled enemy tank.
- Enemy AI uses multiple behavior states:
    - wander
    - attack
    - search
- Line-of-sight detection allows enemies to react(shoot) only when player is "visible".



## Multiplayer Mode

- Local two-player gameplay on the same keyboard.



## Map Generation

- Maps are generated randomly at start of each game.
- A BFS-based path validation algorithm makes sure that a valid path always exists between both spawn locations.
- Spawn zones remain free from walls.



## Combat System

- Projectile-based combat.
- Shooting cooldown system.
- Damage depends on:
    - Distance traveled by the fired projectile.
    - Side of tank that was hit (front, side, or rear).


##  Additional Features
- Sound effects and background music.
- Main menu and tutorial screen.
- Health tracking and win/lose behavior.



## Controls

### Singleplayer

Movement:
- W/A/S/D
- Arrow keys

Shooting:
- Space

### Multiplayer

Blue Tank:
- Arrow keys (movement)
- Backspace (shooting)

Red Tank:
- W/A/S/D (movement)
- Space (shooting)



## How To Run

1. Install Python:
    sudo apt update
    sudo apt install python3 python3-pip
2. Install Pygame:
    pip install pygame
3. Run:
    python3 main.py



## Project Structure

classes/
    bullet.py
    tank.py
    enemy.py
    player.py
    wall.py
game/
    menu.py
    singleplayer.py
    multiplayer.py
    tutorial.py
helper/
    damage_handle.py
    graphics.py
    map_generator.py
main.py



## Possible Improvements

- Multiple AI difficulty levels
- Destructible walls
- Score tracking and statistics