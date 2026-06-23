import pygame

from helper.map_generator import (generate_grid, grid_to_walls)
from helper.damage_handle import deal_damage
from game.menu import Menu
from game.singleplayer import singleplayer_game
from helper.graphics import rotate_img
from game.multiplayer import multiplayer_game
from game.tutorial import tutorial_game
pygame.init()
pygame.mixer.init()
#Screen dimensions
screen_width=800
screen_height=600


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
     
    shoot_sound = pygame.mixer.Sound("sounds/shot.wav")
    hit_sound = pygame.mixer.Sound("sounds/hit.wav")
    victory_sound = pygame.mixer.Sound("sounds/win.wav")
    defeat_sound = pygame.mixer.Sound("sounds/gameover.wav")
    start_sound = pygame.mixer.Sound("sounds/opener.wav")
    shoot_sound.set_volume(0.5)
    hit_sound.set_volume(0.5)
    victory_sound.set_volume(0.5)
    defeat_sound.set_volume(0.5)
    start_sound.set_volume(0.5)

    pygame.mixer.music.load("sounds/gameplay.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1) 

    run = True
    result=None
    while run:
        draw_menu(screen, menu, grass_img, blue_tank_img, red_tank_img)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    menu.move_down()
                elif event.key in (pygame.K_w, pygame.K_UP):
                    menu.move_up()
                elif event.key == pygame.K_RETURN:
                    choice = menu.get_selected()

                    if choice == "Singleplayer":
                        start_sound.play()
                        result = singleplayer_game(screen, grass_img, wall_img,
                                                    blue_tank_img, red_tank_img, bullet_img,
                                                    shoot_sound, hit_sound,
                                                    victory_sound, defeat_sound)
                        if result == "QUIT":
                            run = False
                    elif choice == "Multiplayer":
                        start_sound.play()
                        result = multiplayer_game(screen, grass_img, wall_img,
                                                  blue_tank_img, red_tank_img, bullet_img,
                                                  shoot_sound, hit_sound, victory_sound)
                        if result == "QUIT":
                            run = False
                    elif choice == "Tutorial":
                        result = tutorial_game(screen, grass_img, blue_tank_img, red_tank_img)
                        if result == "QUIT":
                            run = False
                    elif choice == "Quit":
                        run = False
    pygame.quit()


if __name__ == "__main__":
    main()  