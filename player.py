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

img_player = pygame.image.load("img/cannon.png")
img_player_bullet = pygame.image.load("img/player_bullet.png")

img_hp_bar = pygame.Surface((500, 20))
img_hp_bar.fill(GREEN)

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

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.direction = Vector2(1, 0)
        self.speed = 5
        self.angle = 0
        self.image = img_player
        self.rect = self.image.get_rect(center=(x, y))
        self.is_blinking = False
        self.blink_start_time = 0
    
    # �L�[�{�[�h���͂ɂ��ړ�
    def move(self, key): 
        if key[pygame.K_a] and self.rect.center[0] > 10: # a�ō��Ɉړ�
            self.rect.move_ip(-self.speed, 0)
        if key[pygame.K_d] and self.rect.center[0] < SCREEN_WIDTH-20: # d�ŉE�Ɉړ�
            self.rect.move_ip(self.speed, 0)
        if key[pygame.K_w] and self.rect.center[1] > 50: # w�ŏ�Ɉړ�
            self.rect.move_ip(0, -self.speed)
        if key[pygame.K_s] and self.rect.center[1] < SCREEN_HEIGHT-20: # s�ŉ��Ɉړ�
            self.rect.move_ip(0, self.speed)
    
    # �}�E�X����v���C���[�̊p�x���X�V
    def update_direction(self, mouse_pos):
        dx, dy = mouse_pos[0] - self.rect.center[0], mouse_pos[1] - self.rect.center[1]
        self.angle = math.degrees(math.atan2(dy, dx))
        if dx !=0 and dy != 0:
            self.direction = Vector2(dx, dy).normalize()
    
    # �e�𔭎�
    def shoot(self):
        return PlayerBullet(self.rect.center, self.direction)

    # �_�ł̃t���O
    def blink(self):
        self.is_blinking = True
        self.blink_start_time = pygame.time.get_ticks()

    def get_player_pos(self):
        return Vector2(self.rect.center[0], self.rect.center[1])
    
    # �v���C���[�̏�Ԃ��X�V
    def update(self):
        if self.is_blinking:
            dt = pygame.time.get_ticks() - self.blink_start_time
            if dt < BLINKING_TIME:
                if dt % (BLINKING_INTERVAL * 2) < BLINKING_INTERVAL:
                    self.image = pygame.transform.rotozoom(img_player, -90-self.angle, 1)
                else:
                    self.image = pygame.Surface((1,1))
            else:
                self.is_blinking = False
        else:
            self.image = pygame.transform.rotozoom(img_player, -90-self.angle, 1)

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.speed = PLAYER_BULLET_SPEED
        self.direction = direction
        self.image = img_player_bullet
        self.rect = self.image.get_rect(center=pos)
        
    def update(self):
        self.rect.move_ip(self.direction * self.speed)
        
        if self.rect.bottom < 0:    # ��ʊO�̒e���폜
            self.kill()
    
    # �e���G�ɓ����������̏���
    def hit(self):
        for enemy in all_enemy_sprites:
            if self.rect.colliderect(enemy.rect):
                hit_sound.play()
                self.kill()
                enemy.hp -= 1
                if enemy.hp <= 0: # �G��HP��0�ɂȂ�����G���폜
                    explosion_sound.play()
                    enemy.kill()
                return True
        return False
 