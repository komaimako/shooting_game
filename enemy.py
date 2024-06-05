import pygame
from pygame.math import Vector2
import random
import sys
import math

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
