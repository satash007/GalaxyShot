import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1365, 710
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 5, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('GalaxyShot','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('GalaxyShot','Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FPS = 60
Velocity = 5
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('GalaxyShot', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('GalaxyShot','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('GalaxyShot', 'space.png')), (WIDTH, HEIGHT))

def draw_window(WINDOW, red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WINDOW.fill(BLUE)
    WINDOW.blit(SPACE, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, RED)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, YELLOW)

    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))

    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))
    


    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)


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

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text, WINDOW, winner_color):
    draw_text = WINNER_FONT.render(text, 1, winner_color)
    WINDOW.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 400, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    bullet = []
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("WELCOME TO GALAXY SHOT!")
    
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
        
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = 0

        if red_health <= 0:
            winner_text = "Yellow Wins!"
            winner_color = YELLOW
        
        if yellow_health <= 0:
            winner_text = "Red Wins!"
            winner_color = RED

        if winner_text != 0:
           draw_winner(winner_text, WINDOW, winner_color)
           break


        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets,yellow, red)

        draw_window(WINDOW, red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

if __name__ == "__main__":
    main()
