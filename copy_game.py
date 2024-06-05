# -*- coding: shift-jis -*-

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

PLAYER_BULLET_INTERVAL = 50

BULLET_INTERVAL_1 = 1000
BULLET_INTERVAL_2 = 300
BULLET_INTERVAL_3 = 1000

STAGE_1_ENEMY_1 = 5

STAGE_2_ENEMY_1 = 7
STAGE_2_ENEMY_2 = 2

STAGE_3_ENEMY_1 = 10
STAGE_3_ENEMY_2 = 3

STAGE_4_ENEMY_1 = 3
STAGE_4_ENEMY_2 = 1
STAGE_4_ENEMY_3 = 1

img_player = pygame.image.load("img/cannon.png")
img_player_bullet = pygame.image.load("img/player_bullet.png")
img_enemy_bullet = pygame.image.load("img/enemy_bullet_red.png")
img_enemy_bullet_2 = pygame.image.load("img/enemy_bullet_brown.png")
img_enemy_bullet_3 = pygame.image.load("img/enemy_bullet_blue.png")
img_enemy_1 = pygame.image.load("img/enemy_green.png")
img_enemy_2 = pygame.image.load("img/enemy_gray.png")
img_enemy_3 = pygame.image.load("img/enemy_black.png")

img_hp_bar = pygame.Surface((500, 20))
img_hp_bar.fill(GREEN)

player_bullet_sound = pygame.mixer.Sound("snd/shoot2.mp3")
player_bullet_sound.set_volume(0.03)
damage_sound = pygame.mixer.Sound("snd/damage.mp3")
damage_sound.set_volume(0.03)
explosion_sound = pygame.mixer.Sound("snd/attack1.mp3")
explosion_sound.set_volume(0.05)

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
    
    # キーボード入力により移動
    def move(self, key): 
        if key[pygame.K_a] and self.rect.center[0] > 10: # aで左に移動
            self.rect.move_ip(-self.speed, 0)
        if key[pygame.K_d] and self.rect.center[0] < SCREEN_WIDTH-20: # dで右に移動
            self.rect.move_ip(self.speed, 0)
        if key[pygame.K_w] and self.rect.center[1] > 50: # wで上に移動
            self.rect.move_ip(0, -self.speed)
        if key[pygame.K_s] and self.rect.center[1] < SCREEN_HEIGHT-20: # sで下に移動
            self.rect.move_ip(0, self.speed)
    
    # マウスからプレイヤーの角度を更新
    def update_direction(self, mouse_pos):
        dx, dy = mouse_pos[0] - self.rect.center[0], mouse_pos[1] - self.rect.center[1]
        self.angle = math.degrees(math.atan2(dy, dx))
        if dx !=0 and dy != 0:
            self.direction = Vector2(dx, dy).normalize()
    
    # 弾を発射
    def shoot(self):
        return PlayerBullet(self.rect.center, self.direction)

    # 点滅のフラグ
    def blink(self):
        self.is_blinking = True
        self.blink_start_time = pygame.time.get_ticks()

    # プレイヤーの状態を更新
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
        
        if self.rect.bottom < 0:    # 画面外の弾を削除
            self.kill()
    
    # 弾が敵に当たったら弾と敵を削除
    def hit(self):
        for enemy in self.all_enemy_sprites:
            if self.rect.colliderect(enemy.rect):
                self.kill()
                enemy.hp -= 1
                if enemy.hp <= 0: # 敵のHPが0になったら敵を削除
                    explosion_sound.play()
                    enemy.kill()
                return True
        return False
 
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
        self.direction += Vector2(math.cos(angle), math.sin(angle)) * 5.
        self.direction.normalize()
    
    def update_bullet_direction(self, angle):
        self.angle += angle
        self.bullet_dir = Vector2(math.cos(self.angle), math.sin(self.angle))
    
    def update_image(self):
        self.img_rot += 2
        self.img_rot %= 360
        self.image = pygame.transform.rotozoom(img_enemy_3, self.img_rot, 1.2)
        
    def update(self):
        if self.rect.center[0] < 10 or self.rect.center[0] > SCREEN_WIDTH-10:
            self.direction.x *= -1
        elif self.rect.center[1] < 10 or self.rect.center[1] > SCREEN_HEIGHT-10:
            self.direction.y *= -1
        self.rect.move_ip(self.direction * self.speed)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed, img):
        super().__init__()
        self.speed = speed
        self.direction = direction
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
        self.title_font = pygame.font.SysFont("Arial Black", 64)
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
        
        self.all_sprites = pygame.sprite.Group()
    
        self.all_enemy_sprites = pygame.sprite.Group()
        self.enemy_1_sprites = pygame.sprite.Group()
        self.enemy_2_sprites = pygame.sprite.Group()
        self.enemy_3_sprites = pygame.sprite.Group()
    
        self.player_bullet_sprites = pygame.sprite.Group()
        self.enemy_bullet_sprites = pygame.sprite.Group()
        
        player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.all_sprites.add(player)
    
    def create_enemy(self, x, y, dir, img, hp, speed):
        enemy = Enemy(x, y, dir, img, hp, speed)
        
        self.all_enemy_sprites.add(enemy)
    
    def draw_stage1(self):    
        # 敵が周期的に弾を発射する  
        if self.now - self.last_fire_time_1 > BULLET_INTERVAL_1:
            for enemy in self.enemy_1_sprites:
                enemy.update_bullet_direction(random.uniform(0, 2*math.pi))
                enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_1 ,img_enemy_bullet)
                self.enemy_bullet_sprites.add(enemy_bullet)
                self.all_sprites.add(enemy_bullet)
                self.last_fire_time_1 = self.now
                
        # 敵が0になったら次のステージへ
        if len(self.all_enemy_sprites) == 0:
            self.first_time = True
            return 2
        elif self.hp <= 0:
            return STATE_GAMEOVER
        return 1
     
    def draw_stage2(self):
        # 敵が周期的に弾を発射する  
        if self.now - self.last_fire_time_1 > BULLET_INTERVAL_1:
            for enemy in self.enemy_1_sprites:
                enemy.update_bullet_direction(random.uniform(0, 2*math.pi))
                enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_1 ,img_enemy_bullet)
                self.enemy_bullet_sprites.add(enemy_bullet)
                self.all_sprites.add(enemy_bullet)
                self.last_fire_time_1 = self.now
        
        if self.now - self.last_fire_time_2 > BULLET_INTERVAL_2:
            for enemy in self.enemy_2_sprites:
                enemy.update_bullet_direction(math.pi / 4.)
                enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_2 ,img_enemy_bullet_2)
                self.enemy_bullet_sprites.add(enemy_bullet)
                self.all_sprites.add(enemy_bullet)
                self.last_fire_time_2 = self.now
            
        if len(self.all_enemy_sprites) == 0:
            self.first_time = True
            return 3
        elif self.hp <= 0:
            return STATE_GAMEOVER
        return 2
    
    def draw_stage3(self):
        # 敵が周期的に弾を発射する  
        if self.now - self.last_fire_time_1 > BULLET_INTERVAL_1:
            for enemy in self.enemy_1_sprites:
                enemy.update_bullet_direction(random.uniform(0, 2*math.pi))
                enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_3 ,img_enemy_bullet)
                self.enemy_bullet_sprites.add(enemy_bullet)
                self.all_sprites.add(enemy_bullet)
                self.last_fire_time_1 = self.now
        
        if self.now - self.last_fire_time_2 > BULLET_INTERVAL_2:
            for enemy in self.enemy_2_sprites:
                enemy.update_bullet_direction(random.uniform(0, 2*math.pi))
                enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_2 ,img_enemy_bullet_2)
                self.enemy_bullet_sprites.add(enemy_bullet)
                self.all_sprites.add(enemy_bullet)
                self.last_fire_time_2 = self.now
            
        if len(self.all_enemy_sprites) == 0:
            self.first_time = True
            return 4
        elif self.hp <= 0:
            return STATE_GAMEOVER
        return 3
    
    def draw_stage4(self):
        # 敵が周期的に弾を発射する  
        if self.now - self.last_fire_time_1 > BULLET_INTERVAL_1:
            for enemy in self.enemy_1_sprites:
                enemy.update_bullet_direction(random.uniform(0, 2*math.pi))
                enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_3 ,img_enemy_bullet)
                self.enemy_bullet_sprites.add(enemy_bullet)
                self.all_sprites.add(enemy_bullet)
                self.last_fire_time_1 = self.now
        
        if self.now - self.last_fire_time_2 > BULLET_INTERVAL_2:
            for enemy in self.enemy_2_sprites:
                enemy.update_bullet_direction(math.pi / 4.)
                enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_2 ,img_enemy_bullet_2)
                self.enemy_bullet_sprites.add(enemy_bullet)
                self.all_sprites.add(enemy_bullet)
                self.last_fire_time_2 = self.now
        
        if self.now - self.last_fire_time_3 > BULLET_INTERVAL_3:
            for enemy in self.enemy_3_sprites:
                enemy.update_direction(math.pi / 8.)
                for _ in range(0, 8):
                    enemy.update_bullet_direction(math.pi / 4.)
                    enemy_bullet = enemy.shoot(ENEMY_BULLET_SPEED_3 ,img_enemy_bullet_3)
                    self.enemy_bullet_sprites.add(enemy_bullet)
                    self.all_sprites.add(enemy_bullet)
                    self.last_fire_time_3 = self.now
        
        if len(self.all_enemy_sprites) == 0:
            self.first_time = True
            return STATE_CLEAR
        elif self.hp <= 0:
            return STATE_GAMEOVER
        return 4
    
    def draw_stage5(self):
        pass
        
    def draw(self):
        # 各ステージの処理
        if self.stage == 1:
            if self.first_time:
                for _ in range(0, STAGE_1_ENEMY_1):
                    x = random.randint(50, SCREEN_WIDTH-50)
                    y = random.randint(50, SCREEN_HEIGHT-50)
                    dir = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
                    
                    self.create_enemy(x, y, dir, img_enemy_1, 3, 2, self.enemy_1_sprites)
                    
                    # enemy = Enemy(x, y, dir, img_enemy_1, 3, 2)
                    # self.enemy_1_sprites.add(enemy)
                    # self.all_enemy_sprites.add(enemy)
                    # self.all_sprites.add(enemy)
                self.first_time = False
            self.stage = self.draw_stage1()
            
        elif self.stage == 2:
            if self.first_time:
                for _ in range(0, STAGE_2_ENEMY_1):
                    x = random.randint(50, SCREEN_WIDTH-50)
                    y = random.randint(50, SCREEN_HEIGHT-50)
                    dir = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
                    enemy = Enemy(x, y, dir, img_enemy_1, 3, 2)
                    self.enemy_1_sprites.add(enemy)
                    self.all_enemy_sprites.add(enemy)
                    self.all_sprites.add(enemy)
                    
                for _ in range(0, STAGE_2_ENEMY_2):
                    x = random.randint(50, SCREEN_WIDTH-50)
                    y = random.randint(50, SCREEN_HEIGHT-50)
                    dir = Vector2(0, 0)
                    enemy = Enemy(x, y, dir, img_enemy_2, 10, 0)
                    self.enemy_2_sprites.add(enemy)
                    self.all_enemy_sprites.add(enemy)
                    self.all_sprites.add(enemy)
                    
                self.first_time = False
            self.stage = self.draw_stage2()
            
        elif self.stage == 3:
            if self.first_time:
                for _ in range(0, STAGE_3_ENEMY_1):
                    x = random.randint(50, SCREEN_WIDTH-50)
                    y = random.randint(50, SCREEN_HEIGHT-50)
                    dir = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
                    enemy = Enemy(x, y, dir, img_enemy_1, 5, 5)
                    self.enemy_1_sprites.add(enemy)
                    self.all_enemy_sprites.add(enemy)
                    self.all_sprites.add(enemy)
                    
                for _ in range(0, STAGE_3_ENEMY_2):
                    x = random.randint(50, SCREEN_WIDTH-50)
                    y = random.randint(50, SCREEN_HEIGHT-50)
                    dir = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
                    enemy = Enemy(x, y, dir, img_enemy_2, 6, 2)
                    self.enemy_2_sprites.add(enemy)
                    self.all_enemy_sprites.add(enemy)
                    self.all_sprites.add(enemy)
                    
                self.first_time = False
            self.stage = self.draw_stage3()
        elif self.stage == 4:
            if self.first_time:
                for _ in range(0, STAGE_4_ENEMY_1):
                    x = random.randint(50, SCREEN_WIDTH-50)
                    y = random.randint(50, SCREEN_HEIGHT-50)
                    dir = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
                    enemy = Enemy(x, y, dir, img_enemy_1, 5, 5)
                    self.enemy_1_sprites.add(enemy)
                    self.all_enemy_sprites.add(enemy)
                    self.all_sprites.add(enemy)
                    
                for _ in range(0, STAGE_4_ENEMY_2):
                    x = random.randint(50, SCREEN_WIDTH-50)
                    y = random.randint(50, SCREEN_HEIGHT-50)
                    dir = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
                    enemy = Enemy(x, y, dir, img_enemy_2, 6, 4)
                    self.enemy_2_sprites.add(enemy)
                    self.all_enemy_sprites.add(enemy)
                    self.all_sprites.add(enemy)
                
                for _ in range(0, STAGE_4_ENEMY_3):
                    enemy = Enemy(300, 300, Vector2(3, 1).normalize(), img_enemy_3, 30, 1.5)
                    self.enemy_3_sprites.add(enemy)
                    self.all_enemy_sprites.add(enemy)
                    self.all_sprites.add(enemy)
                
                self.first_time = False
            
            for enemy in self.enemy_3_sprites:
                enemy.update_image()
            
            self.stage = self.draw_stage4()
        elif self.stage == STATE_CLEAR:
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
                self.player_bullet_sprites.add(player_bullet)
                self.all_sprites.add(player_bullet)
                self.last_fire_time_player = self.now
        
        # プレイヤーの動き        
        player.move(pygame.key.get_pressed())
        player.update_direction(pygame.mouse.get_pos())
        for bullet in self.player_bullet_sprites:
            if bullet.hit():
                self.score += 100
        
        # 敵の弾がプレーヤーに当たったときの処理
        for bullet in self.enemy_bullet_sprites:
            if bullet.hit():
                self.hp -= 5
                damage_sound.play()
                if self.hp <= 0:
                    self.hp = 100
                    return STATE_GAMEOVER    
            
        self.all_sprites.update()
        
        # 画面の描画
        self.screen.fill(WHITE)
        
        for sprite in self.all_sprites:
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
        
        for sprite in self.all_sprites:
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
    
if __name__ == '__main__':
    
    pygame.display.set_caption("komakomagame")
    
    title_screen = TitleScreen()
    playing_screen = PlayScreen()
    gameover_screen = GameOverScreen()
    clear_screen = ClearScreen()
    
    
    
    clock = pygame.time.Clock()
    
    state = STATE_TITLE
    while True:
        if state == STATE_TITLE:
            state = title_screen.draw()
        elif state == STATE_PLAYING:
            state = playing_screen.draw()
        elif state == STATE_GAMEOVER:
            state = gameover_screen.draw()
        elif state == STATE_CLEAR:
            state = clear_screen.draw()
            
        pygame.display.update()
        clock.tick(60)  # フレームレート    
        