import pygame
from pygame.math import Vector2
import random
import sys
import math


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
 