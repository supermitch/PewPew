import sys, random
import pygame
from pygame.locals import *
    
class Ship(object):
    
    def __init__(self, screen_size):

        self.img = pygame.image.load('_images/ship.png')
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.color = (100, 100, 150)

        self.x = (screen_size[0] / 2) - (self.width / 2)
        self.y = screen_size[1] - (self.height * 2)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.health = 50
        self.death = False

        self.mass = 10
        self.accel = 0
        self.ACCELERATION = 0.5
        self.speed = 0
        self.max_speed = 15
        self.mv = {'left':False, 'right':False, 'up':False, 'down':False}
        self.facing = {'west':False, 'east':False, 'north':True, 'south':False}

    def accelerate(self, direction):

        if direction == 'left':
            self.accel = -1 * self.ACCELERATION
        elif direction == 'right':
            self.accel = self.ACCELERATION
        elif direction == 'off':
            self.accel = 0
        else:
            # log error: "Bad acceleration"
            self.accel = 0
        # can't accelerate past max speed
        if (abs(self.speed) >= self.max_speed) \
            and ((self.speed < 0) == (self.accel < 0)):
            self.accel = 0

    def set_speed(self, accel):
        self.speed += self.accel

    def move(self):
        self.set_speed(self.accel)

        self.rect.move_ip(self.speed, 0)
        if self.speed > 0:
            self.dir_ew = 'right'
        if self.speed < 0:
            self.dir_ew = 'left'    # East / West direction

    def damage(self, strength):
        """Damage our object, kill it if zero health."""
        self.health = self.health - strength
        if self.health <= 0:
            self.death = True

    def collide(self, other, elasticity, reset):
        # this code assumes only some overlap, not total object crossing!
        if reset:
            if other.rect.left < self.rect.left < other.rect.right:
                self.rect.left = other.rect.right
            elif other.rect.right > self.rect.right > other.rect.left:
                self.rect.right = other.rect.left
        self.speed = (self.speed * (self.mass - other.mass) + \
                     2 * other.mass * other.speed_x) / (self.mass + other.mass)
        self.speed *= elasticity    # scale by elasticity
    def draw(self):

        global win_surf
        win_surf.blit(self.img, self.rect.topleft)

class Monster(object):
    
    def __init__(self, screen_size, image_set):
        if random.choice([True, False]):
            self.img = image_set['enemy_1']
            self.speed_y = 1
            self.strength = 10
            self.health = 50
            self.mass = 20
        else:
            self.img = image_set['enemy_2']
            self.speed_y = 3
            self.strength = 2
            self.health = 10
            self.mass = 2

        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.death = False

        self.x = random.randint(20+self.width, screen_size[0] - (20+self.width))
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.speed_x = 0

        self.mv = {'left':False, 'right':False, 'up':False, 'down':True}

    def move(self):

        if self.mv['left']:
            self.rect.move_ip(-self.speed_x, 0)
        elif self.mv['right']:
            self.rect.move_ip(self.speed_x, 0)
        if self.mv['up']: 
            self.rect.move_ip(0, -self.speed_y)
        elif self.mv['down']:
            self.rect.move_ip(0, self.speed_y)

    def damage(self, strength):
        """Damage our object, kill it if zero health."""
        self.health = self.health - strength
        if self.health <= 0:
            self.death = True

    def draw(self):

        global win_surf
        win_surf.blit(self.img, self.rect.topleft)

class Bullet(object):
    
    def __init__(self, shooter):
        
        self.width = 4
        self.height = 4
        self.color = (250, 255, 255)

        self.strength = 10

        self.x = shooter.rect.midtop[0] - (self.width / 2)
        self.y = shooter.rect.midtop[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.speed_y = 40
        self.speed_x = shooter.speed

        self.mv = {'up':True}
        # inherit shooter's left & right velocity
        self.mv['right'] = False
        self.mv['left'] = False
        if shooter.speed > 0:
            self.mv['right'] = True
        elif shooter.speed < 0:
            self.mv['left'] = True

    def move(self):
        if self.mv['up']: 
            old_bottom = self.rect.bottom
            self.rect.move_ip(0, -self.speed_y)
            trail_height = (old_bottom - self.rect.top)
            self.trail_rect = pygame.Rect(self.rect.topleft,
                                        (self.rect.width, trail_height))
        if self.mv['left'] or self.mv['right']:
            self.rect.move_ip(self.speed_x, 0)

    def draw(self):

        global win_surf
        pygame.draw.rect(win_surf, self.color, self.rect)

class Explosion(object):
    
    def __init__(self, source, image_list):

        self.explosion = image_list
        self.frame = 0
        self.complete = False
        self.img = self.explosion[self.frame]
        self.x = source.rect.centerx - self.img.get_width()/2
        self.y = source.rect.centery - self.img.get_height()/2
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(),
                                 self.img.get_height())
        self.rect.center = source.rect.center

    def update(self):
        self.frame += 1
        if self.frame < 5:
            self.img = self.explosion[self.frame]
        else:
            self.complete = True

    def draw(self):
        global win_surf
        win_surf.blit(self.img, self.rect.topleft)

class Wall(object):
    """Screen walls"""

    def __init__(self, left, screen_height):

        self.rect = pygame.Rect(left, -50, 50, screen_height + 100)
        self.strength = float("inf")
        self.mass = 1e20 #float("inf")
        self.health = float("inf")
        self.speed_x = 0
        self.speed_y = 0

class PewPew(object):
    """Primary game object. Not sure this is the best way,
    saw it in someone's game..."""

    def __init__(self):
        """Initalize some game constants."""
        pygame.init()   # initialize pygame

        self.W_WIDTH = 800
        self.W_HEIGHT = 600
        self.screen_size = (self.W_WIDTH, self.W_HEIGHT)
        self.BG_COLOR = (0, 0, 0)
        self.FPS = 40
        self.ADD_MONSTER = 40

    def run(self):
        """Run the actual game."""

        # Build window
        global win_surf
        self.win_surf = pygame.display.set_mode(self.screen_size, RESIZABLE)
        win_surf = self.win_surf
        pygame.display.set_caption('Pew Pew 1.0') 

        # Load our external resources
        self.image_set = self.load_images()

        # Initialize framerate clock
        fps_clock = pygame.time.Clock()

        hero = Ship(self.screen_size)   # initialize hero

        sounds = {}
        sounds['shot'] = pygame.mixer.Sound('_sounds/blip2.wav')
        sounds['shot'].set_volume(0.2)
        sounds['hit'] = pygame.mixer.Sound('_sounds/blip.wav')
        sounds['explode'] = pygame.mixer.Sound('_sounds/smash.wav')
        sounds['explode'].set_volume(0.3)
        pygame.mixer.set_num_channels(12)
        #pygame.mixer.music.load('sounds/castlevania.mid')
        #pygame.mixer.music.play(-1, 0.0)

        bullets = []
        monsters = []
        explosions = []
        walls = [
            Wall(-50, self.W_HEIGHT),
            Wall(self.W_WIDTH, self.W_HEIGHT)
        ]

        # Game loop:
        monster_counter = 0
        while True:

            monster_counter += 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.terminate()
                    elif event.key == K_p:
                        self.pause_game()
                    elif event.key == K_x:
                        self.game_over()
                    elif event.key == K_LEFT:
                        hero.accelerate('left')
                    elif event.key == K_RIGHT:
                        hero.accelerate('right')
                    elif event.key == K_SPACE:
                        if len(bullets) < 2:
                            sounds['shot'].play()
                            b = Bullet(hero)
                            bullets.append(b)

                elif event.type == KEYUP:
                    if event.key == K_LEFT:
                        hero.accelerate('off')
                    elif event.key == K_RIGHT:
                        hero.accelerate('off')
                    elif event.key == K_UP:
                        pass
                    elif event.key == K_DOWN:
                        pass
            
            win_surf.fill(self.BG_COLOR)
            win_rect = win_surf.get_rect()

            
            for b in bullets[:]:
                collision = False
                b.move()
                # look for collisions with monsters
                for m in monsters[:]:
                    if m.rect.colliderect(b.trail_rect):
                        m.damage(b.strength)
                        if m.death:
                            monsters.remove(m)
                            sounds['explode'].play(maxtime=400)
                        else:
                            sounds['hit'].play()
                        e = Explosion(m, self.image_set['explosion'])
                        explosions.append(e)
                        bullets.remove(b)

            for b in bullets[:]:
                b.draw()
                if not win_rect.contains(b.rect):
                    bullets.remove(b)

            if monster_counter == self.ADD_MONSTER:
                monster_counter = 0
                m = Monster(self.screen_size, self.image_set)
                monsters.append(m)

            for m in monsters[:]:
                m.move()
                m.draw()

                if m.rect.colliderect(hero.rect):
                    hero.collide(m, 1.0, False)
                    hero.damage(m.strength)
                    monsters.remove(m)
                    explosions.append(Explosion(m, self.image_set['explosion']))
                    sounds['explode'].play()
                    if not hero.death:
                        sounds['hit'].play()
                        continue

                if not win_rect.contains(m.rect):
                    monsters.remove(m)
                    continue

            if hero.death:
                e = Explosion(hero, self.image_set['explosion'])
                explosions.append(e)
                sounds['explode'].play()
                break # out of game loop
            else:
                hero.move()
                for w in walls:
                    if w.rect.colliderect(hero.rect):
                        hero.collide(w, 0.5, True)
                hero.draw()

            for e in explosions[:]:
                e.update()
                e.draw()
                if e.complete:
                    explosions.remove(e)
 
            pygame.display.update()

            fps_clock.tick(self.FPS)

        if hero.death:
            self.game_over()

    def game_over(self):
        fps_clock = pygame.time.Clock()
        print("Game over!")
        print("Do you want to play again? (y/n)")
        waiting_for_answer = True
        while waiting_for_answer:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.terminate()
                    elif event.key == K_n:
                        self.terminate()
                    elif event.key == K_y:
                        waiting_for_answer = False
            pygame.time.Clock().tick(self.FPS)
        self.run()

    def pause_game(self):
        fps_clock = pygame.time.Clock()
        text = pygame.font.Font(None, 60)
        surf = text.render("Paused!", True, (0,0,255))
        self.win_surf.blit(surf, (self.W_WIDTH/2 - surf.get_width()/2,
                                  self.W_HEIGHT/2 - surf.get_height()/2))
        small_text = pygame.font.Font(None, 30)
        surf = small_text.render("(Press spacebar to resume)", True, (0,0,255))
        self.win_surf.blit(surf, (self.W_WIDTH/2 - surf.get_width()/2,
                                  self.W_HEIGHT/2 - surf.get_height()/2 + 60))
        pygame.display.update()

        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.terminate()
                    elif event.key == K_SPACE:
                        paused = False
            fps_clock.tick(self.FPS)
    
    def load_images(self):

        image_set = {} 
        image_set['enemy_1'] = pygame.image.load('_images/enemy_1.png').convert()
        image_set['enemy_2'] = pygame.image.load('_images/enemy_2.png').convert()
        image_set['ship'] = pygame.image.load('_images/ship.png').convert()

        sprite_sheet = pygame.image.load("_images/explosion_1.png")
        explosion = [sprite_sheet.subsurface((46,46,100,100))
                    ,sprite_sheet.subsurface((238,238,100,100))
                    ,sprite_sheet.subsurface((430,430,100,100))
                    ,sprite_sheet.subsurface((622,622,100,100))
                    ,sprite_sheet.subsurface((814,814,100,100))
                    ]
        image_set['explosion'] = explosion
        return image_set

    def terminate(self):
        pygame.quit()   # uninitialize
        sys.exit()


if __name__ == "__main__":
    app = PewPew()
    app.run()
