import pygame
import random
import os
import sys

if not os.path.exists("score.txt"):
    with open("score.txt", "w") as f:
        f.write("0")
with open("score.txt", "r") as f:
    hiscore = int(f.read())

pygame.init()
pygame.mixer.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Game Window
screen_width = 1200
screen_height = 700
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background Image
menu_img = pygame.image.load('Assets/snakestart.jpg')
menu_img = pygame.transform.scale(menu_img, (screen_width, screen_height)).convert_alpha()
gamebg_img = pygame.image.load('Assets/gamebg.jpg')
gamebg_img = pygame.transform.scale(gamebg_img, (screen_width, screen_height)).convert_alpha()
game_over_img = pygame.image.load('Assets/gameover.jpg')
game_over_img = pygame.transform.scale(game_over_img, (screen_width, screen_height)).convert_alpha()

# Background sound


def gameover():
    pygame.mixer.music.load("Assets/game_over.wav")


pygame.mixer.music.load("Assets/snake_theme.mp3")
pygame.mixer.music.play()
pygame.mouse.set_visible(False)

# Game Caption/Name
pygame.display.set_caption("Snake")

icon = pygame.image.load("Assets/snake.png")
pygame.display.set_icon(icon)

# Updates portion of screen
pygame.display.update()       # Shows any change coded on screen

# Tracks an amount of time
clock = pygame.time.Clock()

# Puts text on screen
font = pygame.font.SysFont("freesansbold.ttf", 35)


def text_screen(score, x, y):
    score_text = font.render(score, True, (0, 0, 0))
    gameWindow.blit(score_text, [x, y])


def screen_hiscore(hiscore, x, y):
    hiscore_text = font.render(hiscore, True, (255, 0, 0))
    gameWindow.blit(hiscore_text, [x, y])


# Plotting snake
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def game_menu():
    while True:
        keys = pygame.key.get_pressed()
        gameWindow.fill(white) 
        gameWindow.blit(menu_img, (0, 0))
        text_screen('Press Enter to Play', 500, 600)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if keys[pygame.K_RETURN]:
                pygame.mixer.music.pause()
                game_loop(hiscore)
        pygame.display.update()    
        clock.tick(60)


def game_loop(hiscore):
    # Game Variables
    exit_game = False
    game_over = False

    # Snake coordinates at start 
    snake_x = 45
    snake_y = 55

    # Snake size at start
    snake_size = 12
    fps = 60

    # Snake speed at start
    vel_x = 0
    vel_y = 0
    velocity = 3

    # Snake food
    food_x = random.randint(50, 600)
    food_y = random.randint(50, 350)

    score = 0

    snk_list = []
    snk_length = 1
    # Game Loop
    while True:
        keys = pygame.key.get_pressed()
        if game_over:
            if score > hiscore:
                with open("score.txt", "w") as f:
                    f.write(str(score))
                with open("score.txt", "r") as f:
                    hiscore = int(f.read()) 
            gameWindow.fill(black)
            gameWindow.blit(game_over_img, (0, 0))
            for event in pygame.event.get():
                # Condition to quit the game
                if event.type == pygame.QUIT:
                    sys.exit()
                
                if keys[pygame.K_RETURN]:
                    game_menu()

        else:
            # Checks for any event occuring in the gameWindow
            for event in pygame.event.get():
                # Condition to quit the game
                if event.type == pygame.QUIT:
                    sys.exit()

                # Condition for fullscreen display
                if keys[pygame.K_F10]:
                    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    
                # Condition to minimize display
                if keys[pygame.K_F11]:
                    pygame.display.set_mode((screen_width, screen_height))

            # Setting speed and direction of snake.
            # Below vel_y or vel_x are 0 to prevent the snake from moving diagonally.
            if keys[pygame.K_d]:
                vel_x = velocity
                vel_y = 0

            if keys[pygame.K_a]:
                vel_x = -velocity
                vel_y = 0

            if keys[pygame.K_w]:
                vel_y = -velocity
                vel_x = 0

            if keys[pygame.K_s]:
                vel_y = velocity
                vel_x = 0
            if keys[pygame.K_q]:
                score += 100
            snake_x += vel_x
            snake_y += vel_y

            if abs(snake_x - food_x) < 14 and abs(snake_y - food_y) < 14:
                pygame.mixer.music.load("Assets/eating.mp3")
                pygame.mixer.music.play()
                score += 10
                snk_length += 5
                food_x = random.randint(20, 600)
                food_y = random.randint(70, 350)
            gameWindow.fill(white)
            gameWindow.blit(gamebg_img, (0, 0))

            text_screen("Score : " + str(score), 10, 10)
            if hiscore > score:
                screen_hiscore("Hiscore : " + str(hiscore), 1000, 10)
            else:
                screen_hiscore("Hiscore : " + str(score), 1000, 10)
            
            # Snake's first coordinates
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            # calling function
            plot_snake(gameWindow,black,snk_list,snake_size)

            # Maintaining size
            if len(snk_list) > snk_length:
                del snk_list[0]
            
            if head in snk_list[:-1]:
                game_over = True
                gameover()
                pygame.mixer.music.play()
            if snake_x > screen_width or snake_x < 0 or snake_y > screen_height or snake_y < 0:
                game_over = True
                gameover()
                pygame.mixer.music.play()

            pygame.draw.circle(gameWindow, (255, 0, 0), (food_x, food_y), 7)
        pygame.display.update()
        clock.tick(fps)


game_menu()
