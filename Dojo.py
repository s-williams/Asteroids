import random

import pygame

# Configs
width = 1600
height = 1200
player_speed = 5
bullet_speed = 20

# PyGame stuff
pygame.init()
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption('Asteroids')
clock = pygame.time.Clock()
crashed = False

# Asset loading
playerImg = pygame.image.load('Player.png')
bulletImg = pygame.image.load('Bullet.png')
bigAsteroidImg = pygame.image.load('bigAsteroid.png')


def player(xx, yy, angles=0):
    rotated_player_img = pygame.transform.rotate(playerImg, angles)
    gameDisplay.blit(rotated_player_img, (xx, yy))


class Bullet:
    def __init__(self, x, y, angle):
        self.x = x + 5
        self.y = y + 5
        if angle == 0:
            self.x_change = 0
            self.y_change = bullet_speed
        if angle == 90:
            self.x_change = bullet_speed
            self.y_change = 0
        if angle == 180:
            self.x_change = 0
            self.y_change = -bullet_speed
        if angle == 270:
            self.x_change = -bullet_speed
            self.y_change = 0

    def update(self):
        self.x -= self.x_change
        self.y -= self.y_change


class Asteroid:
    def __init__(self, x, y, x_speed, y_speed):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.x -= self.x_speed
        self.y -= self.y_speed

# Loop
x = (width * 0.5)
y = (height * 0.5)
x_change = 0
y_change = 0
angle = 0
bullet_list = []
big_asteroid_list = []

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        # MOVE & SHOOT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -5
                angle = 90
            elif event.key == pygame.K_RIGHT:
                x_change = 5
                angle = 270
            if event.key == pygame.K_UP:
                y_change = -5
                angle = 0
            elif event.key == pygame.K_DOWN:
                y_change = 5
                angle = 180
            if event.key == pygame.K_SPACE:
                bullet = Bullet(x, y, angle)
                bullet_list.append(bullet)
        # STOP MOVE
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                x_change = 0
                y_change = 0

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # print(event)

    # add speed changes
    x += x_change
    y += y_change

    # Wrap round screen
    if x > width:
        x = 0
    if y > height:
        y = 0
    if x < 0:
        x = width
    if y < 0:
        y = height

    gameDisplay.fill((0, 0, 0))
    player(x, y, angle)

    for bullet in bullet_list:
        bullet.update()
        gameDisplay.blit(bulletImg, (bullet.x, bullet.y))
        if bullet.x < 0 or bullet.y < 0 or bullet.x > width or bullet.y > height:
            bullet_list.remove(bullet)

    for asteroid in big_asteroid_list:
        asteroid.update()
        gameDisplay.blit(bigAsteroidImg, (asteroid.x, asteroid.y))

        if abs(asteroid.x + 10 - x) < 20 and abs(asteroid.y + 10 - y) < 20:
            crashed = True
            print("game over")
        if asteroid.x < 0 or asteroid.y < 0 or asteroid.x > width or asteroid.y > height:
            big_asteroid_list.remove(asteroid)

    if random.randint(0, 500) > 485:
        big_asteroid = Asteroid(random.choice((0, width)), random.randint(0, height), random.randint(-5, 5), random.randint(-5, 5))
        big_asteroid_list.append(big_asteroid)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
