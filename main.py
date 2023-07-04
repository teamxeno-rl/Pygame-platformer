import pygame
from pygame.locals import *
import random
import sys
import time

pygame.init()

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
hisc = open("HS.txt","r+")
best = 0
bestscore = int(hisc.read())
hisc.close()
while True:
    best = bestscore
    vec = pygame.math.Vector2
    font = pygame.font.Font('ARIAL.TTF', 32)
    HEIGHT = 800
    WIDTH = 600
    ACC = 2
    FRIC = -1
    FPS = 60
    bestscore = best
    besti = font.render("BEST SCORE: " + str(bestscore), True, white)
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

            img_path = f'player.png'
            self.img = pygame.image.load(img_path)
            self.img = pygame.transform.scale(self.img, (30, 30))
            self.rect = self.img.get_rect(center = (30, 420))

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
            hits = pygame.sprite.spritecollide(PL1, platforms, False)
            if PL1.vel.y > 0:
                if hits:
                    self.vel.y = 0
                    self.pos.y = hits[0].rect.top + 1
        
        def jump(self):
            hits = pygame.sprite.spritecollide(PL1, platforms, False)
            if hits:
                self.vel.y = -18

    class platform(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.surf = pygame.Surface((random.randint(100,250), 10))
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
    PL1 = Player()

    #make floor
    PT1.surf = pygame.Surface((WIDTH, 20))
    PT1.surf.fill((128,0,40))
    PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
    players = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    platforms.add(PT1)
    all_sprites.add(PT1)
    players.add(PL1)

    for x in range(random.randint(6,7)):
        pl = platform()
        platforms.add(pl)
        all_sprites.add(pl)

    gameover = False
    while not gameover:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    PL1.jump()
        
        if PL1.rect.top <= HEIGHT / 3:
            PL1.pos.y += abs(PL1.vel.y)
            for plat in platforms:
                plat.rect.y += abs(PL1.vel.y)
                if plat.rect.top >= HEIGHT:
                    platform.plat_gen()
                    Score = int(Score) + 1
                    Scre = Score
                    text = font.render("SCORE: " + str(Scre), True, white)
                    if Score > bestscore and int(Score) > 0:
                        bestscore = Score
                        besti = font.render("BEST SCORE: " + str(bestscore), True, white)

                        hisc = open("HS.txt","w+")
                        hisc.truncate()
                        hisc.close()

                        hisc = open("HS.txt","w+")
                        hisc.write(str(bestscore))
                        hisc.close()
                    plat.kill()
        
        if PL1.rect.top > HEIGHT:
            for entity in all_sprites:
                entity.kill()
            time.sleep(1)
            displaysurface.fill((255,0,0))
            if Score < best:
                text = font.render("FINAL SCORE: " + str(Scre), True, white)
                text2 = font.render("BEST SCORE: " + str(bestscore), True, green)
                displaysurface.blit(text, (120,300))
                displaysurface.blit(text2, (120,350))
            elif Score == best:
                text = font.render("FINAL SCORE: " + str(Scre), True, green)
                displaysurface.blit(text, (120,300))
            elif Score > best:
                text = font.render("NEW HIGH SCORE: " + str(Scre), True, green)
                displaysurface.blit(text, (120,300))
            pygame.display.update()
            time.sleep(5)
            gameover = True
                
        displaysurface.fill((0,0,0))

        for entity in platforms:
            displaysurface.blit(entity.surf, entity.rect)
        
        for entity in players:
            displaysurface.blit(entity.img, entity.rect)

        displaysurface.blit(text, (200,50))
        displaysurface.blit(besti, (200,100))
        PL1.move()
        PL1.update()
        pygame.display.update()
        FramePerSec.tick(FPS)