# Перший проект Python ігра про космос
# ------імпортуємо модулі------------
import pygame
import random
import sys
import os
# -----задаємо значення основним зміним-----
WIDTH = 1100
HEIGHT = 700
FPS = 60
score = 0
game = True
vistril = True
running = True
# ----- кольори які можуть використовуватись------
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
# інеціалізуємо pygame і музику
pygame.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # створюємо окно

pygame.display.set_caption("AsterROCK")  # назва вікна
clock = pygame.time.Clock()  # час

pon = pygame.image.load("img/waw.png")  # іконка для програми
pygame.display.set_icon(pon)

# ===================Створюємо клас ігрока===============


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/1.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_w]:
            self.speedy = -8
        if keystate[pygame.K_s]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.y = 0
        if self.rect.y > HEIGHT-100:
            self.rect.y = HEIGHT - 100

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
# ======================Створюємо клас астероїдів===================


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_img)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 7)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-7, 7)
        self.last_UPDATE = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        self.rotate()
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 7)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_UPDATE > 50:
            self.last_UPDATE = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


# =================================Клас вибухів=========================================


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
# ============================Вжух=============================================


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/27.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
# -------------фунція для малювання тексту----------------


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(("dsd/19505.otf"), size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
# ---------------фунція ка створює астероїди--------------


def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
# ---------------Початковий екран--------------------------


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "ASTER ROCK", 80, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Press a key to begin", 36, WIDTH / 2, HEIGHT - 400)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
# ---------------Кінцевий екран----------------------------------


def game_over():
    screen.blit(background, background_rect)
    draw_text(screen, "Game Over", 70, WIDTH / 2, HEIGHT/2)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
# ----------створюємо музику і графіку----------


shoot_sound = pygame.mixer.Sound('snd/laserpew.ogg')
exp_sound = pygame.mixer.Sound("snd/Muffled Distant Explosion.wav")
pygame.mixer.music.load('snd/Phon.ogg')
pygame.mixer.music.set_volume(0.4)  # гучність музики

background = pygame.image.load("img/11.jpg")
background_rect = background.get_rect()
meteor = ["img/d1.png", "img/d2.png", "img/d3.png", "img/d4.png"]
meteor_img = []
for img in meteor:
    meteor_img.append(pygame.image.load(img))
# ствоюємо групи за допомогою Sprite
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(10):
    new_mob()
# -----анімація вибуху------
explosion_anim = {}
explosion_anim['lg'] = []

for i in range(1, 16):
    filename = 'img/h{}.png'.format(i)
    img = pygame.image.load(filename)
    img_lg = pygame.transform.scale(img, (120, 120))
    explosion_anim['lg'].append(img_lg)

pygame.mixer.music.play(loops=-1)  # робим так щоб музика іграла не зупиняючись
# ========================================================Ігровий цикл==================================================
while running:
    # прописуєм початковий екран
    if game:
        vistril = False
        show_go_screen()
        game = False
        bullets = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(10):
            new_mob()
        score = 0

# робим так щоб ми могли виходити із ігри і стріляти при нажатії і утримуванні миші
    clock.tick(FPS)
    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            vistril = True
        if event.type == pygame.MOUSEBUTTONUP:
            vistril = False
    if vistril:
        player.shoot()

    all_sprites.update()
# робим мобів та іграка смертним)
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 1
        exp_sound.play()
        ex = Explosion(hit.rect.center, 'lg')
        all_sprites.add(ex)
        new_mob()
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    for hit in hits:
        ex = Explosion(hit.rect.center, 'lg')
        all_sprites.add(ex)
        if hits:
            game_over()
# ----------рендеринг-------------------
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 40, 50, 10)
    pygame.display.flip()
# ----------ця функція призначена для вдалого перетворення програми у exe-файл за допомогою pyinstaller


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pygame.quit()  # провсякий випадок закриваєм окно
