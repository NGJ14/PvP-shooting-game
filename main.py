import math
import sys

import pygame

pygame.init()

screen = pygame.display.set_mode((1000, 700))

background = pygame.image.load("bg.jpg")

pygame.display.set_caption("Space Wars")

# setting FPS
clock = pygame.time.Clock()
FPS = 60

# player 1
p1Img = pygame.image.load("p1.png")
p1X = 90
p1Y = 300
p1Y_change = 0

# player 2
p2Img = pygame.image.load("p2.png")
p2X = 800
p2Y = 300
p2Y_change = 0

# bullet 1
b1Img = pygame.image.load("b1.png")
b1X = 150
b1Y = 0
b1X_change = 30
b1Y_change = 0
b1_state = "ready"
b1total = 24

# bullet 2
b2Img = pygame.image.load("b2.png")
b2X = 800
b2Y = 0
b2X_change = 30
b2Y_change = 0
b2total = 24
b2_state = "ready"

# healths
h1 = 10
h2 = 10
font = pygame.font.Font("freesansbold.ttf", 32)

h1X = 10
h1Y = 10
h2X = 800
h2Y = 10

# Game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_h1(x, y):
    screen.blit(font.render(f"Bullets : {str(b1total)}", True, (255, 255, 255)), (h1X, h1Y + 30))
    screen.blit(font.render(f"Health : {str(h1)}", True, (255, 255, 255)), (x, y))


def show_h2(x, y):
    screen.blit(font.render(f"Bullets : {str(b2total)}", True, (255, 255, 255)), (h2X, h2Y + 30))
    screen.blit(font.render(f"Health : {str(h2)}", True, (255, 255, 255)), (x, y))


def game_over_text():
    if h1 == 0:
        over_text = over_font.render("PLAYER 2 WINS", True, (255, 255, 255))
        screen.blit(over_text, (250, 250))
    elif h2 == 0:
        over_text = over_font.render("PLAYER 1 WINS", True, (255, 255, 255))
        screen.blit(over_text, (250, 250))


# display player 1
def p1(x, y):
    screen.blit(p1Img, (x, y))


# display player 2
def p2(x, y):
    screen.blit(p2Img, (x, y))


# display bullet 1
def fire_b1(x, y):
    global b1_state
    b1_state = "fire"
    screen.blit(b1Img, (x, y))


# display bullet 2
def fire_b2(x, y):
    global b2_state
    b2_state = "fire"
    screen.blit(b2Img, (x, y))


# collision detection
def isCollision1(p2X, p2Y, b1X, b1Y):
    distance = math.sqrt(math.pow(p2X - b1X, 2) + (math.pow(p2Y - b1Y, 2)))
    return distance < 55


def isCollision2(p1X, p1Y, b2X, b2Y):
    distance = math.sqrt(math.pow(p1X - b2X, 2) + (math.pow(p1Y - b2Y, 2)))
    return distance < 55


running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # player 1 and bullet 1 movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                p1Y_change = -6
            if event.key == pygame.K_x:
                p1Y_change = 6
            if event.key == pygame.K_s and b1_state == "ready" and b1total >= 1:
                b1total -= 1

                b1Y = p1Y + 40
                fire_b1(b1X, b1Y)
        if event.type == pygame.KEYUP and event.key in [pygame.K_w, pygame.K_x]:
            p1Y_change = 0

        # player 2 and bullet 2 movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                p2Y_change = -6
            if event.key == pygame.K_DOWN:
                p2Y_change = 6
            if event.key == pygame.K_SPACE and b2_state == "ready" and b2total > 1:
                b2total -= 1
                b2Y = p2Y + 38
                fire_b2(b2X, b2Y)
        if event.type == pygame.KEYUP and event.key in [pygame.K_UP, pygame.K_DOWN]:
            p2Y_change = 0

    # player 1 movement
    p1Y += p1Y_change
    if p1Y <= -5:
        p1Y = -5
    elif p1Y >= 580:
        p1Y = 580

    # player 2 movement
    p2Y += p2Y_change
    if p2Y <= -5:
        p2Y = -5
    elif p2Y >= 580:
        p2Y = 580

    # bullet 1 movement
    if b1X >= 980:
        b1X = 150
        b1_state = "ready"
    if b1_state == "fire":
        fire_b1(b1X, b1Y)
        b1X += b1X_change

    # bullet 2 movement
    if b2X <= 0:
        b2X = 800
        b2_state = "ready"
    if b2_state == "fire":
        fire_b2(b2X, b2Y)
        b2X -= b2X_change

    if collision := isCollision2(p2X, p2Y + 38, b1X, b1Y):
        b1X = 150
        b1_state = "ready"
        h2 -= 1
    if collision := isCollision1(p1X, p1Y + 40, b2X, b2Y):
        b2X = 800
        b2_state = "ready"
        h1 -= 1

    if h1 == 0 or h2 == 0:
        break

    p1(p1X, p1Y)
    p2(p2X, p2Y)
    show_h1(h1X, h1Y)
    show_h2(h2X, h2Y)
    pygame.display.update()

while True:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    game_over_text()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(1)
            # TODO:Does not exit the window?

    pygame.display.update()
