import pygame
import os

WIDTH, HEIGHT = 1365, 710
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 5, HEIGHT)
FPS = 60
Velocity = 5
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BULLET_VEL = 7
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('GalaxyShot', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('GalaxyShot','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

def draw_window(WINDOW, red, yellow):
    WINDOW.fill(BLUE)
    pygame.draw.rect(WINDOW, BLACK, BORDER)
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))
    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - Velocity > 0: #LEFT
            yellow.x -= Velocity
        if keys_pressed[pygame.K_d] and yellow.x + Velocity + yellow.width < BORDER.x: #RIGHT
            yellow.x += Velocity
        if keys_pressed[pygame.K_w] and yellow.y - Velocity > 0: #UP
            yellow.y -= Velocity
        if keys_pressed[pygame.K_s] and yellow.y + Velocity + yellow.height < HEIGHT: #DOWN
            yellow.y += Velocity

def red_handle_movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x - Velocity > BORDER.x + BORDER.width: #LEFT
            red.x -= Velocity
        if keys_pressed[pygame.K_RIGHT] and red.x + Velocity + red.width < WIDTH: #RIGHT
            red.x += Velocity
        if keys_pressed[pygame.K_UP] and red.y - Velocity > 0: #UP
            red.y -= Velocity
        if keys_pressed[pygame.K_DOWN] and red.y + Velocity + red.height < HEIGHT: #DOWN
            red.y += Velocity

def main():
    red = pygame.Rect(700, 400, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    bullet = []
    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("wELCOME TO GALAXY SHOT!")
    
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(red.x, red.y + red.height/2 - 2, 10, 5)
                    red_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        draw_window(WINDOW, red, yellow)


    pygame.quit()

if __name__ == "__main__":
    main()
