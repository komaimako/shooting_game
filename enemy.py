import pygame
from pygame.math import Vector2
import random
import sys
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

STATE_TITLE = -1
STATE_PLAYING = -2
STATE_GAMEOVER = -3
STATE_CLEAR = -4

TEXT_BLINKING_INTERVAL = 600

BLACK = (0, 0, 0)
WHITE = (230, 230, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BLINKING_TIME = 500
BLINKING_INTERVAL = 100

PLAYER_BULLET_SPEED = 10

ENEMY_BULLET_SPEED_1 = 3
ENEMY_BULLET_SPEED_2 = 2
ENEMY_BULLET_SPEED_3 = 5
BOSS_BULLET_SPEED = 7

PLAYER_BULLET_INTERVAL = 50

BULLET_INTERVAL_1 = 1500
BULLET_INTERVAL_2 = 500
BULLET_INTERVAL_3 = 1000
BULLET_INTERVAL_4 = 80

STAGE_1_ENEMY_1 = 6

STAGE_2_ENEMY_1 = 10
STAGE_2_ENEMY_2 = 3

STAGE_3_ENEMY_1 = 7
STAGE_3_ENEMY_2 = 3

STAGE_4_ENEMY_1 = 3
STAGE_4_ENEMY_2 = 2
STAGE_4_ENEMY_3 = 1

"""�摜����"""
img_player = pygame.image.load("img/cannon.png")
img_player_bullet = pygame.image.load("img/player_bullet.png")
img_enemy_bullet = pygame.image.load("img/enemy_bullet_red.png")
img_enemy_bullet_2 = pygame.image.load("img/enemy_bullet_purple.png")
img_enemy_bullet_3 = pygame.image.load("img/enemy_bullet_blue.png")
img_enemy_1 = pygame.image.load("img/enemy_blue.png")
img_enemy_2 = pygame.image.load("img/enemy_gray.png")
img_enemy_3 = pygame.image.load("img/enemy_black.png")
img_boss = pygame.image.load("img/hiroshi.png")
""""""

img_hp_bar = pygame.Surface((500, 20))
img_hp_bar.fill(GREEN)

"""��������"""
player_bullet_sound = pygame.mixer.Sound("snd/shoot2.mp3")
player_bullet_sound.set_volume(0.05)
damage_sound = pygame.mixer.Sound("snd/damage.mp3")
damage_sound.set_volume(0.05)
explosion_sound = pygame.mixer.Sound("snd/attack1.mp3")
explosion_sound.set_volume(0.1)
hit_sound = pygame.mixer.Sound("snd/select05.mp3")
hit_sound.set_volume(0.05)
man_damage = pygame.mixer.Sound("snd/man_damage.mp3")
man_damage.set_volume(0.2)
man_scream = pygame.mixer.Sound("snd/man_scream.mp3")
man_scream.set_volume(0.7)
""""""

img_enemy_bullet = pygame.image.load("img/enemy_bullet_red.png")
img_enemy_bullet_2 = pygame.image.load("img/enemy_bullet_purple.png")
img_enemy_bullet_3 = pygame.image.load("img/enemy_bullet_blue.png")
img_enemy_1 = pygame.image.load("img/enemy_blue.png")
img_enemy_2 = pygame.image.load("img/enemy_gray.png")
img_enemy_3 = pygame.image.load("img/enemy_black.png")
img_boss = pygame.image.load("img/hiroshi.png")

player_bullet_sound = pygame.mixer.Sound("snd/shoot2.mp3")
player_bullet_sound.set_volume(0.05)
damage_sound = pygame.mixer.Sound("snd/damage.mp3")
damage_sound.set_volume(0.05)
explosion_sound = pygame.mixer.Sound("snd/attack1.mp3")
explosion_sound.set_volume(0.1)
hit_sound = pygame.mixer.Sound("snd/select05.mp3")
hit_sound.set_volume(0.05)
man_damage = pygame.mixer.Sound("snd/man_damage.mp3")
man_damage.set_volume(0.2)
man_scream = pygame.mixer.Sound("snd/man_scream.mp3")
man_scream.set_volume(0.7)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, dir, img, hp, speed):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.direction = dir
        self.hp = hp
        self.bullet_dir = Vector2(random.uniform(-10,10), random.uniform(-10,10)).normalize()
        self.angle = 0.
        self.img_rot = 0
        
    def shoot(self, speed ,img):
        return EnemyBullet(self.rect.center, self.bullet_dir, speed, img)
    
    def update_direction(self, angle):
        self.direction += Vector2(math.cos(angle), math.sin(angle))
        self.direction.normalize()
    
    def update_bullet_direction(self, angle):
        self.angle += angle
        self.bullet_dir = Vector2(math.cos(self.angle), math.sin(self.angle))
    
    def aim_at_player(self, pos):
        self.bullet_dir = pos - Vector2(self.rect.center[0], self.rect.center[1])
        self.bullet_dir.normalize()
    
    def update_image(self):
        self.img_rot += 2
        self.img_rot %= 360
        self.image = pygame.transform.rotozoom(img_enemy_3, self.img_rot, 1.2)
        
    def update(self):
        if self.rect.center[0] < 20 or self.rect.center[0] > SCREEN_WIDTH-20:
            self.direction.x *= -1
        elif self.rect.center[1] < 30 or self.rect.center[1] > SCREEN_HEIGHT-20:
            self.direction.y *= -1
        self.direction
        self.rect.move_ip(self.direction * self.speed)
        
    def play_boss_damage(self):
        for bullet in player_bullet_sprites:
            if self.rect.colliderect(bullet.rect):
                man_damage.play()            

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed, img):
        super().__init__()
        self.speed = speed
        self.direction = direction.normalize()
        self.image = img
        self.rect = self.image.get_rect(center=pos)
    
    def hit(self):
        if self.rect.colliderect(player.rect):
            self.kill()
            player.blink()
            return True
        return False
    
    def update(self):
        self.rect.move_ip(self.direction * self.speed)
        
        if self.rect.bottom < 0:
            self.kill()
