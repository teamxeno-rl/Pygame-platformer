import pygame
from pygame.locals import *
import random
import sys
import time

pygame.init()

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
while True:

    vec = pygame.math.Vector2
    font = pygame.font.Font('ARIAL.TTF', 32)
    HEIGHT = 800
    WIDTH = 600
    ACC = 2
    FRIC = -1
    FPS = 60
    Score = 0
    Scre = Score
    text = font.render("SCORE: " + str(Scre), True, white)
    FramePerSec = pygame.time.Clock()

    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platformer")

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.surf = pygame.Surface((30,30))
            self.surf.fill((128,255,40))
            self.rect = self.surf.get_rect(center = (30, 420))

            self.pos = vec((20, 670))
            self.vel = vec(0,0)
            self.acc = vec(0,0)

        def move(self):
            self.acc = vec(0,0.5)

            pressed_keys = pygame.key.get_pressed()
            pygame.key.set_repeat(50, 50)

            if pressed_keys[K_LEFT]:
                self.acc.x = -ACC * 2
            if pressed_keys[K_RIGHT]:
                self.acc.x = ACC * 2

            self.acc.x += self.vel.x * FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

            if self.pos.x > WIDTH:
                self.pos.x = 0
            if self.pos.x < 0:
                self.pos.x = WIDTH
            
            self.rect.midbottom = self.pos
        
        def update(self):
            hits = pygame.sprite.spritecollide(P1, platforms, False)
            if P1.vel.y > 0:
                if hits:
                    self.vel.y = 0
                    self.pos.y = hits[0].rect.top + 1
        
        def jump(self):
            hits = pygame.sprite.spritecollide(P1, platforms, False)
            if hits:
                self.vel.y = -18

    class platform(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.surf = pygame.Surface((random.randint(100,250), 24))
            self.surf.fill((128,0,40))
            self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-20), random.randint(0,HEIGHT-60)))

        def plat_gen():
            while len(platforms) < 10 :
                width = random.randrange(100,250)
                p = platform()
                p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-100, 0))
                platforms.add(p)
                all_sprites.add(p)

    PT1 = platform ()
    P1 = Player()

    #make floor
    PT1.surf = pygame.Surface((WIDTH, 20))
    PT1.surf.fill((128,0,40))
    PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 20))

    platforms = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    platforms.add(PT1)
    all_sprites.add(PT1)
    all_sprites.add(P1)

    for x in range(random.randint(6,7)):
        pl = platform()
        platforms.add(pl)
        all_sprites.add(pl)

    run1 = bool(True)
    while run1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    P1.jump()
        
        if P1.rect.top <= HEIGHT / 3:
            P1.pos.y += abs(P1.vel.y)
            for plat in platforms:
                plat.rect.y += abs(P1.vel.y)
                if plat.rect.top >= HEIGHT:
                    platform.plat_gen()
                    Score = int(Score) + 1
                    Scre = Score
                    text = font.render("SCORE: " + str(Scre), True, white)
                    plat.kill()
        
        if P1.rect.top > HEIGHT:
            for entity in all_sprites:
                entity.kill()
                time.sleep(1)
                displaysurface.fill((255,0,0))
                text = font.render("FINAL SCORE: " + str(Scre), True, white)
                displaysurface.blit(text, (120,350))
                pygame.display.update()
                time.sleep(5)
                run1 = bool(0)
                
        displaysurface.fill((0,0,0))

        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)

        displaysurface.blit(text, (200,50)) 
        P1.move()
        P1.update()
        pygame.display.update()
        FramePerSec.tick(FPS)