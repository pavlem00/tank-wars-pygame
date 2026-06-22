import pygame

screen_width = 800
screen_height = 600

def draw_key(screen, text, key_x, key_y, key_width=40, key_height=40):
    pygame.draw.rect(screen, (128,128,128), (key_x, key_y, key_width, key_height))
    pygame.draw.rect(screen, (0,0,0), (key_x, key_y, key_width, key_height), 2)

    label = pygame.font.SysFont("arial", 20).render(text, 1, (0,0,0))

    screen.blit(label, (key_x + key_width//2 - label.get_width()//2,
                        key_y + key_height//2 - label.get_height()//2))
    

def tutorial_game(screen, grass_img, blue_tank_img, red_tank_img):
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "MENU"
        screen.blit(grass_img, (0,0))
        
        pygame.draw.line(screen, (255,255,255), (screen_width//2, 80), (screen_width//2, screen_height-40), 3)


        title_font = pygame.font.SysFont("arialblack", 60)
        text_font = pygame.font.SysFont("arial", 20)    
        title = title_font.render("TUTORIAL", 1, (255,255,255))
        screen.blit(title, (screen_width//2-title.get_width()//2, 20))

        text = text_font.render("SINGLEPLAYER", 1, (255,255,255))
        screen.blit(text, (120, 100))
        screen.blit(blue_tank_img, (170, 130))
        movement = text_font.render("Movement controls:", 1, (250,250,250))
        screen.blit(movement, (100, 200))
        draw_key(screen, "W", 100, 250)
        draw_key(screen, "A", 50, 300)
        draw_key(screen, "S", 100, 300)
        draw_key(screen, "D", 150, 300)
        draw_key(screen, "↑", 250, 250)
        draw_key(screen, "←", 200, 300)
        draw_key(screen, "↓", 250, 300)
        draw_key(screen, "→", 300, 300)
        shooting = text_font.render("Shooting controls:", 1, (255,255,255))
        screen.blit(shooting, (90, 400))
        draw_key(screen, "Space", 110, 450, 160, 40)

        text = text_font.render("MULTIPLAYER", 1, (255,255,255))
        screen.blit(text, (540, 100))
        screen.blit(blue_tank_img, (650, 130))
        screen.blit(red_tank_img, (500, 130))
        movement = text_font.render("Movement controls:", 1, (255,255,255))
        screen.blit(movement, (520, 200))
        draw_key(screen, "W", 470, 250)
        draw_key(screen, "A", 420, 300)
        draw_key(screen, "S", 470, 300)
        draw_key(screen, "D", 520, 300)
        draw_key(screen, "↑", 650, 250)
        draw_key(screen, "←", 600, 300)
        draw_key(screen, "↓", 650, 300)
        draw_key(screen, "→", 700, 300)
        shooting = text_font.render("Shooting controls:", 1, (255,255,255))
        screen.blit(shooting, (510, 400))
        draw_key(screen, "Space", 420, 450, 160, 40)
        draw_key(screen, "Backspace", 630, 450, 120, 40)
        pygame.display.flip()