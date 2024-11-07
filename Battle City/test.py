import pygame
from random import randint

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption('Танки')
pygame.display.set_icon(pygame.image.load('images/tank1.png'))

fontUI = pygame.font.Font(None, 30)
fontBig = pygame.font.Font(None, 70)
fontTitle = pygame.font.Font(None, 140)

imgBrick = pygame.image.load('images/block_brick.png')
imgTanks = [
    pygame.image.load('images/tank1.png'),
    pygame.image.load('images/tank2.png'),
    pygame.image.load('images/tank3.png'),
    pygame.image.load('images/tank4.png'),
    pygame.image.load('images/tank5.png'),
    pygame.image.load('images/tank6.png'),
    pygame.image.load('images/tank7.png'),
    pygame.image.load('images/tank8.png'), ]
imgBangs = [
    pygame.image.load('images/bang1.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang3.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang1.png'), ]
imgBonuses = [
    pygame.image.load('images/bonus_star.png'),
    pygame.image.load('images/bonus_tank.png'), ]

sndShot = pygame.mixer.Sound('sounds/shot.wav')
sndDestroy = pygame.mixer.Sound('sounds/destroy.wav')
sndDead = pygame.mixer.Sound('sounds/dead.wav')
sndLive = pygame.mixer.Sound('sounds/live.wav')
sndStar = pygame.mixer.Sound('sounds/star.wav')
sndEngine = pygame.mixer.Sound('sounds/engine.wav')
sndEngine.set_volume(0.5)
sndMove = pygame.mixer.Sound('sounds/move.wav')
sndMove.set_volume(0.5)

pygame.mixer.music.load('sounds/level_start.mp3')
pygame.mixer.music.play()

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
TILE = 32

MOVE_SPEED = [1, 2, 2, 1, 2, 3, 3, 2]
BULLET_SPEED = [4, 5, 6, 5, 5, 5, 6, 7]
BULLET_DAMAGE = [1, 1, 2, 3, 2, 2, 3, 4]
SHOT_DELAY = [60, 50, 30, 40, 30, 25, 25, 30]


class Tank:
    def __init__(self, color, px, py, direct, keysList):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = 2

        self.shotTimer = 0
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1
        self.isMove = False

        self.hp = 5

        self.keyLEFT = keysList[0]
        self.keyRIGHT = keysList[1]
        self.keyUP = keysList[2]
        self.keyDOWN = keysList[3]
        self.keySHOT = keysList[4]

        self.rank = 0
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.moveSpeed = MOVE_SPEED[self.rank]
        self.bulletDamage = BULLET_DAMAGE[self.rank]
        self.bulletSpeed = BULLET_SPEED[self.rank]
        self.shotDelay = SHOT_DELAY[self.rank]

        oldX, oldY = self.rect.topleft
        if keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
            self.isMove = True
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
            self.isMove = True
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2
            self.isMove = True
        elif keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
            self.isMove = True
        else:
            self.isMove = False

        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0: self.shotTimer -= 1

        for obj in objects:
            if obj != self and obj.type == 'block':
                if self.rect.colliderect(obj):
                    self.rect.topleft = oldX, oldY

    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            sndDead.play()
            print(self.color, 'is dead')


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

        bullets.append(self)
        sndShot.play()

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type != 'bang' and obj.type != 'bonus':
                    if obj.rect.collidepoint(self.px, self.py):
                        obj.damage(self.damage)
                        bullets.remove(self)
                        Bang(self.px, self.py)
                        sndDestroy.play()
                        break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)


class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'

        self.px, self.py = px, py
        self.frame = 0

    def update(self):
        self.frame += 0.2
        if self.frame >= 5: objects.remove(self)

    def draw(self):
        img = imgBangs[int(self.frame)]
        rect = img.get_rect(center=(self.px, self.py))
        window.blit(img, rect)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        window.blit(imgBrick, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0: objects.remove(self)


class Bonus:
    def __init__(self, px, py, bonusNum):
        objects.append(self)
        self.type = 'bonus'

        self.px, self.py = px, py
        self.bonusNum = bonusNum
        self.timer = 600

        self.image = imgBonuses[self.bonusNum]
        self.rect = self.image.get_rect(center=(self.px, self.py))

    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            objects.remove(self)

        for obj in objects:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                if self.bonusNum == 0:
                    if obj.rank < len(imgTanks) - 1:
                        obj.rank += 1
                        sndStar.play()
                        objects.remove(self)
                        break
                elif self.bonusNum == 1:
                    obj.hp += 1
                    sndLive.play()
                    objects.remove(self)
                    break

    def draw(self):
        if self.timer % 30 < 15:
            window.blit(self.image, self.rect)


def init_game():
    global bullets, objects, tank1, tank2, bonusTimer, timer, isMove, isWin, y

    bullets = []
    objects = []

    # Создаем танки
    tank1 = Tank('blue', 50, 50, 1, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
    tank2 = Tank('red', 700, 500, 3, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN))

    # Создаем блоки
    for _ in range(100):
        while True:
            x = randint(0, WIDTH // TILE - 1) * TILE
            y = randint(1, HEIGHT // TILE - 1) * TILE
            rect = pygame.Rect(x, y, TILE, TILE)
            fined = False
            for obj in objects:
                if rect.colliderect(obj): fined = True
            if not fined: break
        Block(x, y, TILE)

    # Сбрасываем таймеры и флаги
    bonusTimer = 180
    timer = 0
    isMove = False
    isWin = False
    y = 0

    pygame.mixer.music.load('sounds/level_start.mp3')
    pygame.mixer.music.play()

bullets = []
objects = []
tank1 = Tank('blue', 50, 50, 1, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
tank2 = Tank('red', 700, 500, 3, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN))

for _ in range(100):
    while True:
        x = randint(0, WIDTH // TILE - 1) * TILE
        y = randint(1, HEIGHT // TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE)
        fined = False
        for obj in objects:
            if rect.colliderect(obj): fined = True
        if not fined: break

    Block(x, y, TILE)

bonusTimer = 180
timer = 0
isMove = False
isWin = False
y = 0

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()

    timer += 1
    if timer >= 260 and not isWin:
        if oldIsMove != isMove:
            if isMove:
                sndMove.play()
                sndEngine.stop()
            else:
                sndMove.stop()
                sndEngine.play(-1)

    oldIsMove = isMove
    isMove = False
    for obj in objects:
        if obj.type == 'tank': isMove = isMove or obj.isMove

    if bonusTimer > 0:
        bonusTimer -= 1
    else:
        Bonus(randint(50, WIDTH - 50), randint(50, HEIGHT - 50), randint(0, len(imgBonuses) - 1))
        bonusTimer = randint(120, 240)

    for bullet in bullets: bullet.update()
    for obj in objects: obj.update()

    window.fill('black')
    for bullet in bullets: bullet.draw()
    for obj in objects: obj.draw()

    i = 0
    for obj in objects:
        if obj.type == 'tank':
            pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))

            text = fontUI.render(str(obj.rank), 1, 'black')
            rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
            window.blit(text, rect)

            text = fontUI.render(str(obj.hp), 1, obj.color)
            rect = text.get_rect(center=(5 + i * 70 + TILE, 5 + 11))
            window.blit(text, rect)
            i += 1

    t = 0
    for obj in objects:
        if obj.type == 'tank':
            t += 1
            tankWin = obj

    if t == 1 and not isWin:
        isWin = True
        timer = 1000

    if timer < 260:
        y += 2
        pygame.draw.rect(window, 'black', (WIDTH // 2 - 300, HEIGHT // 2 - 200 + y, 600, 250))
        pygame.draw.rect(window, 'orange', (WIDTH // 2 - 300, HEIGHT // 2 - 200 + y, 600, 250), 3)
        text = fontTitle.render('Т А Н К И', 1, 'white')
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100 + y))
        window.blit(text, rect)
        text = fontBig.render('BATTLE CITY 2D', 1, 'white')
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20 + y))
        window.blit(text, rect)

    if t == 1:
        text = fontBig.render('ПОБЕДИЛ', 1, 'white')
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        window.blit(text, rect)

        pygame.draw.rect(window, tankWin.color, (WIDTH // 2 - 100, HEIGHT // 2, 200, 200))

    if isWin and timer == 1000:
        sndMove.stop()
        sndEngine.stop()

        pygame.mixer.music.load('sounds/level_finish.mp3')
        pygame.mixer.music.play()

    if isWin and timer > 1000:
        if timer > 1200:  # Задержка перед запуском
            init_game()  # Перезапускаем игру

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
