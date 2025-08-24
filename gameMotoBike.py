# Import thư viện
import random
import sys

import pygame
import pygame.gfxdraw
from pygame.locals import *

# Khởi tạo màn hình game
WINDOWWIDTH = 400
WINDOWHEIGHT = 600

# Đường biên và làn xe
X_MARGIN = 80
LANEWIDTH = 60

# Khơi tạo xe
CARWIDTH = 37
CARHEIGHT = 57
CARSPEED = 3
CARIMG = pygame.image.load('img/car.png')

# Khởi tạo chướng ngại vật
DISTANCE = 200
OBSTACLESSPEED = 2
CHANGESPEED = 0.001
OBSTACLESIMG = pygame.image.load('img/obstacles.png')

# Khởi tạo nền game
BGSPEED = 1.5
BGIMG = pygame.image.load('img/background.png')
pygame.mixer.init()

# Load audio
hit = pygame.mixer.Sound("audio/explode.wav")
hit.set_volume(0.6)
hit1 = pygame.mixer.Sound("audio/CARTOON-LAUGH.mp3")
hit1.set_volume(0.6)

pygame.mixer.music.load('audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

pygame.init()

FPS = 60
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Đua Xe Tốc Độ - by LeNghia')


# Tạo lớp nền
class Background:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = BGSPEED
        self.img = BGIMG
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def draw(self):
        DISPLAYSURF.blit(self.img, (int(self.x), int(self.y)))
        DISPLAYSURF.blit(self.img, (int(self.x), int(self.y - self.height)))

    def update(self):
        self.y += self.speed
        if self.y > self.height:
            self.y -= self.height


# Tạo lớp chướng ngại vật
class Obstacles:
    def __init__(self):
        self.width = CARWIDTH
        self.height = CARHEIGHT
        self.distance = DISTANCE
        self.speed = OBSTACLESSPEED
        self.changeSpeed = CHANGESPEED
        self.ls = []
        for i in range(5):
            y = -CARHEIGHT - i * self.distance
            lane = random.randint(0, 3)
            self.ls.append([lane, y])

    def draw(self):
        for i in range(5):
            x = int(X_MARGIN + self.ls[i][0] * LANEWIDTH + (LANEWIDTH - self.width) / 2)
            y = int(self.ls[i][1])
            DISPLAYSURF.blit(OBSTACLESIMG, (x, y))

    def update(self):
        for i in range(5):
            self.ls[i][1] += self.speed
        self.speed += self.changeSpeed
        if self.ls[0][1] > WINDOWHEIGHT:
            self.ls.pop(0)
            y = self.ls[3][1] - self.distance
            lane = random.randint(0, 3)
            self.ls.append([lane, y])


# tạo lớp xe
class Car:
    def __init__(self):
        self.width = CARWIDTH
        self.height = CARHEIGHT
        self.x = (WINDOWWIDTH - self.width) / 2
        self.y = (WINDOWHEIGHT - self.height) / 2
        self.speed = CARSPEED
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 255, 255))

    def draw(self):
        DISPLAYSURF.blit(CARIMG, (int(self.x), int(self.y)))

    def update(self, moveLeft, moveRight, moveUp, moveDown):
        if moveLeft:
            self.x -= self.speed
        if moveRight:
            self.x += self.speed
        if moveUp:
            self.y -= self.speed
        if moveDown:
            self.y += self.speed

        if self.x < X_MARGIN:
            self.x = X_MARGIN
        if self.x + self.width > WINDOWWIDTH - X_MARGIN:
            self.x = WINDOWWIDTH - X_MARGIN - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > WINDOWHEIGHT:
            self.y = WINDOWHEIGHT - self.height


# tạo lớp tính điểm
class Score:
    def __init__(self):
        self.score = 0

    def draw(self):
        font = pygame.font.SysFont('consolas', 30)
        scoreSuFace = font.render('Point: ' + str(int(self.score)), True, (0, 0, 0))
        DISPLAYSURF.blit(scoreSuFace, (10, 10))

    def update(self):
        self.score += 0.02


def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0] + rect2[2] and rect2[0] <= rect1[0] + rect1[2] and rect1[1] <= rect2[1] + rect2[3] and \
            rect2[1] <= rect1[1] + rect1[3]:
        return True
    return False


def isGameover(car, obstacles):
    carRect = [car.x, car.y, car.width, car.height]
    for i in range(5):
        x = int(X_MARGIN + obstacles.ls[i][0] * LANEWIDTH + (LANEWIDTH - obstacles.width) / 2)
        y = int(obstacles.ls[i][1])
        obstaclesRect = [x, y, obstacles.width, obstacles.height]
        if rectCollision(carRect, obstaclesRect):
            return True
    return False


def gameStart(bg):
    bg.__init__()
    font = pygame.font.SysFont('consolas', 40)
    headingSuFace = font.render('ĐUA XE', True, (255, 0, 0))
    headingSize = headingSuFace.get_size()

    font = pygame.font.SysFont('consolas', 20)
    commentSuFace = font.render('"SPACE" TO START', True, (0, 0, 0))
    commentSize = commentSuFace.get_size()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == K_SPACE:
                    return
        bg.draw()
        DISPLAYSURF.blit(headingSuFace, (int((WINDOWWIDTH - headingSize[0]) / 2), 100))
        DISPLAYSURF.blit(commentSuFace, (int((WINDOWWIDTH - commentSize[0]) / 2), 400))
        pygame.display.update()
        fpsClock.tick(FPS)


def gamePlay(bg, car, obstacles, score):
    car.__init__()
    obstacles.__init__()
    bg.__init__()
    score.__init__()
    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    moveLeft = True
                    print("===> moveLeft")
                if event.key == K_RIGHT:
                    moveRight = True
                    print("===> moveRight")
                if event.key == K_UP:
                    moveUp = True
                    print("===> moveUp")
                if event.key == K_DOWN:
                    moveDown = True
                    print("===> moveDown")
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False
        if isGameover(car, obstacles):
            return

        bg.draw()
        bg.update()
        car.draw()
        car.update(moveLeft, moveRight, moveUp, moveDown)
        obstacles.draw()
        obstacles.update()
        score.draw()
        score.update()
        pygame.display.update()
        fpsClock.tick(FPS)


def gameOver(bg, car, obstacles, score):
    font = pygame.font.SysFont('consolas', 60)
    headingSuFace = font.render('CHƠI NGU QUÁ', True, (255, 0, 0))
    headingSize = headingSuFace.get_size()

    font = pygame.font.SysFont('consolas', 20)
    commentSuFace = font.render('SPACE TO AGAIN', True, (0, 0, 0))
    commentSize = commentSuFace.get_size()

    pygame.mixer.music.load('audio/moonlight.wav')
    pygame.mixer.music.pause()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == K_SPACE:
                    pygame.mixer.music.load('audio/moonlight.wav')
                    pygame.mixer.music.play(-1, 0.0)
                    pygame.mixer.music.set_volume(0.6)
                    return
            bg.draw()
            car.draw()
            obstacles.draw()
            score.draw()
            DISPLAYSURF.blit(headingSuFace, (int((WINDOWWIDTH - headingSize[0]) / 2), 100))
            DISPLAYSURF.blit(commentSuFace, (int((WINDOWWIDTH - commentSize[0]) / 2), 400))
        pygame.display.update()
        fpsClock.tick(FPS)


def main():
    bg = Background()
    car = Car()
    obstacles = Obstacles()
    score = Score()
    gameStart(bg)
    while True:
        gamePlay(bg, car, obstacles, score)
        hit.play()
        hit1.play()
        gameOver(bg, car, obstacles, score)

if __name__ == '__main__':
    main()
