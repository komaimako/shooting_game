import pygame
from pygame.math import Vector2
import random
import sys
import math
from player import Player, PlayerBullet
from enemy import Enemy, EnemyBullet

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

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT():
                return False
        return True
    
    def update(self):
        pass
    
    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
class TitleScreen(Screen):
    def __init__(self):
        super().__init__()
        self.title_font = pygame.font.SysFont("Arial Black", 50)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.title_text = self.title_font.render("Attack on Titan", True, BLACK)
        self.subtitle_text = self.subtitle_font.render("Press any key to start", True, BLACK)
        self.subtitle_rect = self.subtitle_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+50))
        
    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return STATE_PLAYING
                
        self.screen.fill(WHITE)
        self.screen.blit(self.title_text, self.title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-50)))
        
        if pygame.time.get_ticks() % (TEXT_BLINKING_INTERVAL * 2) < TEXT_BLINKING_INTERVAL:
            self.screen.blit(self.subtitle_text, self.subtitle_rect)
        
        return STATE_TITLE

class PlayScreen(Screen):
    def __init__(self):
        super().__init__()
        self.score_font = pygame.font.Font(None, 32)
        self.score = 0
        self.hp = 100
        self.now = 0
        self.last_fire_time_player = 0
        self.last_fire_time_1 = 0
        self.last_fire_time_2 = 0
        self.last_fire_time_3 = 0
        self.stage = 1
        self.first_time = True
    
    def create_enemy(self, x, y, dir, img, hp, speed, sp_index):
        enemy = Enemy(x, y, dir, img, hp, speed)
        all_enemy_sprites.add(enemy)
        all_sprites.add(enemy)
        if sp_index == 1:
            enemy_1_sprites.add(enemy)
        elif sp_index == 2:
            enemy_2_sprites.add(enemy)
        elif sp_index == 3:
            enemy_3_sprites.add(enemy)
        elif sp_index == -1:
            boss_sprite.add(enemy)
    
    def draw_stage1(self):    
        # �G�������I�ɒe�𔭎˂���  
        if self.now - self.last_fire_time_1 > BULLET_INTERVAL_1:
            for enemy in enemy_1_sprites:
                enemy.update_bullet_direction(random.uniform(0, 2*math.pi))
                enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_1 ,img_enemy_bullet)
                enemy_bullet_sprites.add(enemy_bullet)
                all_sprites.add(enemy_bullet)
                self.last_fire_time_1 = self.now
                
        # �G��0�ɂȂ����玟�̃X�e�[�W��
        if len(all_enemy_sprites) == 0:
            self.first_time = True
            return 2
        elif self.hp <= 0:
            return STATE_GAMEOVER
        return 1
     
    def draw_stage2(self):
        # �G�������I�ɒe�𔭎˂���  
        if self.now - self.last_fire_time_1 > BULLET_INTERVAL_3:
            for enemy in enemy_1_sprites:
                enemy.update_bullet_direction(random.uniform(0, 2*math.pi))
                enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_1 ,img_enemy_bullet)
                enemy_bullet_sprites.add(enemy_bullet)
                all_sprites.add(enemy_bullet)
                self.last_fire_time_1 = self.now
        
        if self.now - self.last_fire_time_2 > BULLET_INTERVAL_1:
            for enemy in enemy_2_sprites:
                for _ in range(0, 8):
                    enemy.update_bullet_direction(math.pi / 4.)
                    enemy_bullet = enemy.shoot(BOSS_BULLET_SPEED ,img_enemy_bullet_2)
                    enemy_bullet_sprites.add(enemy_bullet)
                    all_sprites.add(enemy_bullet)
                    self.last_fire_time_2 = self.now
            
        if len(all_enemy_sprites) == 0:
            self.first_time = True
            return 3
        elif self.hp <= 0:
            return STATE_GAMEOVER
        return 2
    
    def draw_stage3(self):
        # �G�������I�ɒe�𔭎˂���  
        if self.now - self.last_fire_time_1 > BULLET_INTERVAL_1:
            for enemy in enemy_1_sprites:
                enemy.update_bullet_direction(random.uniform(0, 2*math.pi))
                enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_3 ,img_enemy_bullet)
                enemy_bullet_sprites.add(enemy_bullet)
                all_sprites.add(enemy_bullet)
                self.last_fire_time_1 = self.now
        
        if self.now - self.last_fire_time_2 > BULLET_INTERVAL_2:
            for enemy in enemy_2_sprites:
                enemy.aim_at_player(player.get_player_pos())
                enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_3 ,img_enemy_bullet_2)
                enemy_bullet_sprites.add(enemy_bullet)
                all_sprites.add(enemy_bullet)
                self.last_fire_time_2 = self.now
            
        if len(all_enemy_sprites) == 0:
            self.first_time = True
            return 4
        elif self.hp <= 0:
            return STATE_GAMEOVER
        return 3
    
    def draw_stage4(self):
        # �G�������I�ɒe�𔭎˂���  
        if self.now - self.last_fire_time_1 > BULLET_INTERVAL_1:
            for enemy in enemy_1_sprites:
                enemy.update_bullet_direction(random.uniform(0, 2*math.pi))
                enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_3 ,img_enemy_bullet)
                enemy_bullet_sprites.add(enemy_bullet)
                all_sprites.add(enemy_bullet)
                self.last_fire_time_1 = self.now
        
        if self.now - self.last_fire_time_2 > BULLET_INTERVAL_2:
            for enemy in enemy_2_sprites:
                enemy.update_bullet_direction(math.pi / 4.)
                enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_2 ,img_enemy_bullet_2)
                enemy_bullet_sprites.add(enemy_bullet)
                all_sprites.add(enemy_bullet)
                self.last_fire_time_2 = self.now
        
        if self.now - self.last_fire_time_3 > BULLET_INTERVAL_3:
            for enemy in enemy_3_sprites:
                enemy.update_direction(math.pi / 8.)
                for _ in range(0, 8):
                    enemy.update_bullet_direction(math.pi / 4.)
                    enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_3 ,img_enemy_bullet)
                    enemy_bullet_sprites.add(enemy_bullet)
                    all_sprites.add(enemy_bullet)
                    self.last_fire_time_3 = self.now
        
        if len(all_enemy_sprites) == 0:
            self.first_time = True
            return 5
        elif self.hp <= 0:
            return STATE_GAMEOVER
        return 4
    
    def draw_stage5(self):
        # �G�������I�ɒe�𔭎˂���  
        if self.now - self.last_fire_time_1 > BULLET_INTERVAL_3:
            for enemy in boss_sprite:
                enemy.update_direction(math.pi / 4.)
                for _ in range(0, 16):
                    enemy.update_bullet_direction(math.pi / 8.)
                    enemy_bullet = enemy.shoot(BOSS_BULLET_SPEED ,img_enemy_bullet)
                    enemy_bullet_sprites.add(enemy_bullet)
                    all_sprites.add(enemy_bullet)
                    self.last_fire_time_1 = self.now
        
        if self.now - self.last_fire_time_2 > BULLET_INTERVAL_4:
            for enemy in boss_sprite:
                enemy.aim_at_player(player.get_player_pos())
                enemy_bullet = enemy.shoot(BOSS_BULLET_SPEED ,img_enemy_bullet_2)
                enemy_bullet_sprites.add(enemy_bullet)
                all_sprites.add(enemy_bullet)
                self.last_fire_time_2 = self.now
                    
        if len(all_enemy_sprites) == 0:
            man_scream.play()
            self.first_time = True
            return STATE_CLEAR
        elif self.hp <= 0:
            return STATE_GAMEOVER
        return 5
        
    def draw(self):
        # �e�X�e�[�W�̏���
        if self.stage == 1: # �X�e�[�W1
            if self.first_time:
                for _ in range(0, STAGE_1_ENEMY_1):
                    x = random.randint(50, SCREEN_WIDTH-50)
                    y = random.randint(50, SCREEN_HEIGHT-50)
                    dir = Vector2(random.uniform(-10, 10), random.uniform(-10, 10)).normalize()
                    self.create_enemy(x, y, dir, img_enemy_1, 3, 2, 1)
                    
                self.first_time = False
            self.stage = self.draw_stage1()
            
        elif self.stage == 2: # �X�e�[�W2
            if self.first_time:
                for _ in range(0, STAGE_2_ENEMY_1):
                    x = random.randint(50, SCREEN_WIDTH-50)
                    y = random.randint(50, SCREEN_HEIGHT-50)
                    dir = Vector2(random.uniform(-10, 10), random.uniform(-10, 10)).normalize()
                    self.create_enemy(x, y, dir, img_enemy_1, 3, 3, 1)
                    
                for _ in range(0, STAGE_2_ENEMY_2):
                    x = random.randint(50, SCREEN_WIDTH-50)
                    y = random.randint(50, SCREEN_HEIGHT-50)
                    dir = Vector2(0, 0)
                    self.create_enemy(x, y, dir, img_enemy_2, 10, 0, 2)
                    
                self.first_time = False
            self.stage = self.draw_stage2()
            
        elif self.stage == 3: # �X�e�[�W3
            if self.first_time:
                for _ in range(0, STAGE_3_ENEMY_1):
                    x = random.randint(50, SCREEN_WIDTH-50)
                    y = random.randint(50, SCREEN_HEIGHT-50)
                    dir = Vector2(random.uniform(-10, 10), random.uniform(-10, 10)).normalize()
                    self.create_enemy(x, y, dir, img_enemy_1, 4, 5, 1)
                    
                for _ in range(0, STAGE_3_ENEMY_2):
                    x = random.randint(50, SCREEN_WIDTH-50)
                    y = random.randint(50, SCREEN_HEIGHT-50)
                    dir = Vector2(random.uniform(-10, 10), random.uniform(-10, 10)).normalize()
                    self.create_enemy(x, y, dir, img_enemy_2, 6, 4, 2)
        
                self.first_time = False
            self.stage = self.draw_stage3()
            
        elif self.stage == 4: # �X�e�[�W4
            if self.first_time:
                for _ in range(0, STAGE_4_ENEMY_1):
                    x = random.randint(50, SCREEN_WIDTH-50)
                    y = random.randint(50, SCREEN_HEIGHT-50)
                    dir = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
                    self.create_enemy(x, y, dir, img_enemy_1, 5, 5, 1)
                    
                for _ in range(0, STAGE_4_ENEMY_2):
                    x = random.randint(50, SCREEN_WIDTH-50)
                    y = random.randint(50, SCREEN_HEIGHT-50)
                    dir = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
                    self.create_enemy(x, y, dir, img_enemy_2, 6, 4, 2)

                for _ in range(0, STAGE_4_ENEMY_3):
                    self.create_enemy(300, 300, Vector2(3, 1).normalize(), img_enemy_3, 30, 1.5, 3)
                    
                self.first_time = False
            
            for enemy in enemy_3_sprites:
                enemy.update_image()
            
            self.stage = self.draw_stage4()
        
        elif self.stage == 5: # �X�e�[�W5
            if self.first_time:
                for _ in range(0, 1):
                    self.create_enemy(500, 500, Vector2(3, 1).normalize(), img_boss, 100, 5, -1)
                self.first_time = False
            
            for enemy in boss_sprite:
                enemy.play_boss_damage()    
            self.stage = self.draw_stage5()   
            
        elif self.stage == STATE_CLEAR:
            man_scream.play()
            return STATE_CLEAR
        
        self.now = pygame.time.get_ticks()
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed()[0]:
            if self.now - self.last_fire_time_player > PLAYER_BULLET_INTERVAL:
                player_bullet = player.shoot()
                player_bullet_sound.play()
                player_bullet_sprites.add(player_bullet)
                all_sprites.add(player_bullet)
                self.last_fire_time_player = self.now
        
        # �v���C���[�̓���        
        player.move(pygame.key.get_pressed())
        player.update_direction(pygame.mouse.get_pos())
        for bullet in player_bullet_sprites:
            if bullet.hit():
                self.score += 100
        
        # �G�̒e���v���[���[�ɓ��������Ƃ��̏���
        for bullet in enemy_bullet_sprites:
            if bullet.hit():
                self.hp -= 5
                damage_sound.play()
                if self.hp <= 0:
                    self.hp = 100
                    return STATE_GAMEOVER    
            
        all_sprites.update()
        
        # ��ʂ̕`��
        self.screen.fill(WHITE)
        
        for sprite in all_sprites:
            self.screen.blit(sprite.image, sprite.rect)
        
        score_text = self.score_font.render(f"SCORE: {self.score}", True, BLACK)
        hp_bar_width = int(self.hp / 100 * img_hp_bar.get_width())
        hp_bar_rect = pygame.Rect(0, 0, hp_bar_width, img_hp_bar.get_height())
        img_hp_bar_to_draw = img_hp_bar.subsurface(hp_bar_rect)
        self.screen.blit(img_hp_bar_to_draw, (SCREEN_WIDTH // 2 - img_hp_bar.get_width() // 2, 10))
        self.screen.blit(score_text, score_text.get_rect(topright=(SCREEN_WIDTH-10, 10)))
        
        return STATE_PLAYING

class GameOverScreen(Screen):
    def __init__(self):
        super().__init__()
        self.title_font = pygame.font.Font(None, 128)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.title_text = self.title_font.render("GAME OVER", True, RED)
        self.subtitle_text = self.subtitle_font.render("Press any key to restart", True, BLACK)
        self.subtitle_rect = self.subtitle_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return STATE_PLAYING

        self.screen.fill(WHITE)
        
        for sprite in all_sprites:
            self.screen.blit(sprite.image, sprite.rect)
        
        self.screen.blit(self.title_text, self.title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-50)))
        self.screen.blit(self.subtitle_text, self.subtitle_rect)
        
        return STATE_GAMEOVER

class ClearScreen(Screen):
    def __init__(self):
        super().__init__()
        self.title_font = pygame.font.SysFont("impact", 128)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.title_text = self.title_font.render("YOU WIN", True, RED)
        self.subtitle_text = self.subtitle_font.render("Press any key to restart", True, WHITE)
        self.subtitle_rect = self.subtitle_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return STATE_PLAYING

        self.screen.fill(WHITE)
        self.screen.blit(player.image, player.rect)
        self.screen.blit(self.title_text, self.title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-50)))
        
        return STATE_CLEAR
  