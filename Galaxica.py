#!/usr/bin/env python
from __future__ import division
import pygame
import random
from os import path

## assets folder
sprite_folder = path.join(path.dirname(__file__), 'sprites')
sound_folder = path.join(path.dirname(__file__), 'sounds')


WIDTH = 600
HEIGHT = 800
FPS = 60
BAR_LENGTH = 100
BAR_HEIGHT = 10

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('serif')

def main_menu():
    global screen

    pygame.mixer.music.load(path.join(sound_folder, "Panda Eyes & Subkey - Galaxica.ogg"))
    pygame.mixer.music.play(-1)

    title = pygame.image.load(path.join(sprite_folder, "menu.png")).convert()
    title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)

    screen.blit(title, (0,0))
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
                break
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit() 
        else:
            draw_text(screen, "PRESS ANY KEY TO CONTINUE", 20, WIDTH/2, HEIGHT/2 + 50)
            pygame.display.update()

    screen.fill(BLACK)
    draw_text(screen, "GET READY!", 40, WIDTH/2, HEIGHT/2)
    pygame.display.update()
    

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    pct = max(pct, 0) 
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)



def new_asteroid():
    mob_element = asteroid()
    sprites.add(mob_element)
    mobs.add(mob_element)

class explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0 
        self.speedy = 0 
        self.shield = 100
        self.shoot_delay = 250
        self.lives = 3
        self.power = 1
        self.hide_timer = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        
    def update(self):
                
        self.speedy = 0
        self.speedx = 0

        keystate = pygame.key.get_pressed()     
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        elif keystate[pygame.K_DOWN]:
            self.speedy = 5
        #Fire weapons by holding spacebar
        if keystate[pygame.K_SPACE]:
            self.shoot()

        # loop arround
        if self.rect.right > WIDTH:
            self.rect.right = 100
        if self.rect.left < 0:
            self.rect.left = WIDTH - 100
        
        #prevent person from passing the top / bottom
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        if self.power < 1:
            self.power = 1
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = laser(self.rect.centerx, self.rect.top)
                sprites.add(bullet)
                bullets.add(bullet)
                shooting_sound.play()
                
            if self.power == 2:
                bullet1 = laser(self.rect.left, self.rect.centery)
                bullet2 = laser(self.rect.right, self.rect.centery)
                sprites.add(bullet1)
                sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shooting_sound.play()

            if self.power >= 3:
                self.power = 3;
                bullet1 = laser(self.rect.left, self.rect.centery)
                bullet2 = laser(self.rect.right, self.rect.centery)
                beam1 = beam(self.rect.centerx, self.rect.top) 
                sprites.add(bullet1)
                sprites.add(bullet2)
                sprites.add(beam1)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(beam1)
                shooting_sound.play()
                beam_sound.play()

    def powerup(self):
        self.power += 1


# defines the asteroids
class asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(asteroid_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()  ## time when the rotation has to happen
        
    def rotate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50: # in milliseconds
            self.last_update = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360 
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.kill()
            new_asteroid()

## defines the sprite for powerups
class powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

            

# defines the sprite for bullets
class laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y 
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class beam(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = beam_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.timer = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.timer > 500:
            self.kill()


# Load game images
background = pygame.image.load(path.join(sprite_folder, 'nebula.jpg')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(sprite_folder, 'Bruiser-T40.png')).convert()
player_lives = pygame.transform.scale(player_img, (25, 25))
player_lives.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(sprite_folder, 'laserRed16.png')).convert()
beam_img = pygame.image.load(path.join(sprite_folder, 'tractorbeam.png')).convert_alpha()
beam_img = pygame.transform.scale(beam_img, (75, 1000))
asteroid_images = []

for i in range(6):
    filename = 'asteroid0{}.png'.format(i)
    img = pygame.image.load(path.join(sprite_folder, filename)).convert()
    img.set_colorkey(BLACK)
    asteroid_images.append(img)

#explosions
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(6):
    filename = 'explosion0{}.png'.format(i)
    img = pygame.image.load(path.join(sprite_folder, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
    img = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img)
    img = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img)
    

# load power ups
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(sprite_folder, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(sprite_folder, 'bolt_gold.png')).convert()


# Load game sounds
shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'pew.wav'))
beam_sound = pygame.mixer.Sound(path.join(sound_folder, 'rocket.ogg'))
expl_sounds = []
for sound in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(sound_folder, sound)))

player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'rumble1.ogg'))

running = True
menu_display = True
while running:
    if menu_display:
        main_menu()
        pygame.mixer.music.stop()
        pygame.mixer.music.load(path.join(sound_folder, 'AdhesiveWombat - 8 Bit Adventure.ogg'))
        pygame.mixer.music.play(-1)
        pygame.time.wait(3000)
       
        menu_display = False
        
        sprites = pygame.sprite.Group()
        player = Player()
        sprites.add(player)

        mobs = pygame.sprite.Group()
        for i in range(2):
            new_asteroid()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        score = 0
        
    clock.tick(FPS)     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
             
        ## Press ESC to exit game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu_display = True
                pygame.display.update()

    sprites.update()


    # check if a bullet hit a asteroid
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    # now as we delete the asteroid element when we hit one with a bullet, we need to respawn them again
    # as there will be no mob_elements left out 
    for hit in hits:
        score += hit.radius
        random.choice(expl_sounds).play()
        expl = explosion(hit.rect.center, 'lg')
        sprites.add(expl)
        if random.random() > 0.9:
            pow = powerup(hit.rect.center)
            sprites.add(pow)
            powerups.add(pow)
        new_asteroid()

    # check if the player collides with the asteroid
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius
        player.power -= 1
        expl = explosion(hit.rect.center, 'sm')
        sprites.add(expl)
        new_asteroid()
        if player.shield <= 0: 
            player_die_sound.play()
            death_explosion = explosion(player.rect.center, 'player')
            sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # if the player hit a power up
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += 25
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()

    # if player died
    if player.lives == 0 and not death_explosion.alive():
        menu_display = True
        pygame.display.update()

    screen.fill(BLACK)
    screen.blit(background, background_rect)

    sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)     ## 10px down from the screen
    draw_shield_bar(screen, 5, 5, player.shield)

    # Draw lives
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_lives)
    pygame.display.flip()       

pygame.quit()
