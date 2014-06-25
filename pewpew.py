import sys, random
import pygame
from pygame.locals import *

from classes.ship import Ship
from classes.monster import Monster
from classes.bullet import Bullet
from classes.wall import Wall
from classes.explosion import Explosion
from classes.world import World

class PewPew(object):
    """ Primary game object. Not sure this is the best way,
    saw it in someone's game... """

    def __init__(self):
        """Initalize some game constants."""
        pygame.init()   # initialize pygame

        self.W_WIDTH = 800
        self.W_HEIGHT = 600
        self.screen_size = (self.W_WIDTH, self.W_HEIGHT)
        self.BG_COLOR = (0, 0, 0)
        self.FPS = 40
        self.ADD_MONSTER = 40
        self.world = World()  # Empty world

    def run(self):
        """Run the actual game."""

        # Build window
        global win_surf
        self.win_surf = pygame.display.set_mode(self.screen_size,
                                                RESIZABLE)
        win_surf = self.win_surf
        pygame.display.set_caption('Pew Pew 1.0') 

        # Load our external resources
        self.image_set = self.loadimages()

        # Initialize framerate clock
        fps_clock = pygame.time.Clock()

        # Add world items
        self.world.hero = Ship(self.screen_size)   # initialize hero
        self.world.bullets = []
        self.world.monsters = []
        self.world.explosions = []

        sounds = {}
        sounds['shot'] = pygame.mixer.Sound('sounds/blip2.wav')
        sounds['shot'].set_volume(0.2)
        sounds['hit'] = pygame.mixer.Sound('sounds/blip.wav')
        sounds['hit'].set_volume(0.3)
        sounds['explode'] = pygame.mixer.Sound('sounds/smash.wav')
        sounds['explode'].set_volume(0.2)
        pygame.mixer.set_num_channels(12)
        #pygame.mixer.music.load('sounds/castlevania.mid')
        #pygame.mixer.music.play(-1, 0.0)

        walls = [
            Wall(-50, self.W_HEIGHT),
            Wall(self.W_WIDTH, self.W_HEIGHT)
        ]

        stats = {
            'bullets_fired': 0,
            'bullets_missed': 0,
            'bullets_hit': 0,
            'monsters_killed': 0,
            'monsters_missed': 0,
        }

        # Game loop:
        frame_counter = 0
        while True:
            # Main game loop
            frame_counter += 1
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
                        self.world.hero.accelerate('left')
                    elif event.key == K_RIGHT:
                        self.world.hero.accelerate('right')
                    elif event.key == K_SPACE:
                        if len(self.world.bullets) < 2:
                            sounds['shot'].play()
                            b = Bullet(self.world.hero)
                            self.world.bullets.append(b)
                            stats['bullets_fired'] += 1
                elif event.type == KEYUP:
                    if event.key == K_LEFT:
                        self.world.hero.accelerate('off')
                    elif event.key == K_RIGHT:
                        self.world.hero.accelerate('off')
                    elif event.key == K_UP:
                        pass
                    elif event.key == K_DOWN:
                        pass
            
            win_surf.fill(self.BG_COLOR)
            win_rect = win_surf.get_rect()

            for b in self.world.bullets[:]:
                collision = False
                b.move()
                # look for collisions with monsters
                for m in self.world.monsters[:]:
                    if m.rect.colliderect(b.trail_rect):
                        stats['bullets_hit'] += 1
                        m.damage(b.strength)
                        if m.death:
                            self.world.monsters.remove(m)
                            stats['monsters_killed'] += 1
                            sounds['explode'].play(maxtime=400)
                        else:
                            sounds['hit'].play()
                        e = Explosion(m, self.image_set['explosion'])
                        self.world.explosions.append(e)
                        self.world.bullets.remove(b)

            for b in self.world.bullets[:]:
                if not win_rect.contains(b.rect):
                    stats['bullets_missed'] += 1
                    self.world.bullets.remove(b)

            if frame_counter >= self.ADD_MONSTER:
                # Trigger a new monster
                frame_counter = 0
                m = Monster(self.screen_size, self.image_set)
                self.world.monsters.append(m)

            for m in self.world.monsters[:]:
                m.move()

                if m.rect.colliderect(self.world.hero.rect):
                    self.world.hero.collide(m, 1.0, False)
                    self.world.hero.damage(m.strength)
                    self.world.monsters.remove(m)
                    self.world.explosions.append(Explosion(m,
                         self.image_set['explosion']))
                    sounds['explode'].play()
                    if not self.world.hero.death:
                        sounds['hit'].play()
                        continue

                if not win_rect.contains(m.rect):
                    stats['monsters_missed'] += 1
                    self.world.monsters.remove(m)
                    continue

            if self.world.hero.death:
                e = Explosion(self.world.hero,
                              self.image_set['explosion'])
                self.world.explosions.append(e)
                sounds['explode'].play()
                break # out of game loop
            else:
                self.world.hero.move()
                for w in walls:
                    if w.rect.colliderect(self.world.hero.rect):
                        self.world.hero.collide(w, 0.5, True)

            for e in self.world.explosions[:]:
                e.update()
                if e.complete:
                    self.world.explosions.remove(e)
 
            # Text displays
            colour = (100, 100, 255)
            self.plot_stats(stats, colour)
            self.plot_fuel(self.world.hero.fuel,
                           self.world.hero.max_fuel, colour)
            self.plot_health(self.world.hero.health,
                             self.world.hero.damage,
                             self.world.hero.max_health, colour)

            self.render()
            pygame.display.update()

            fps_clock.tick(self.FPS)

        if self.world.hero.death:
            self.game_over()

    def render(self):
        """ Blit our game objects to the screen. """
        self.win_surf.blit(*self.world.hero.draw())
        for monster in self.world.monsters:
            self.win_surf.blit(*monster.draw())
        for explosion in self.world.explosions:
            self.win_surf.blit(*explosion.draw())
        for bullet in self.world.bullets:
            # Bullets are filled rects, for now.
            pygame.draw.rect(win_surf, *bullet.draw())
        return None

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

    def plot_stats(self, stats, colour):
        """ Plots text statistics, but doesn't display them. """
        try:
            accuracy = float(stats['bullets_hit']) / stats['bullets_fired'] * 100
        except ZeroDivisionError:
            accuracy = 0.0
        text = pygame.font.Font(None, 20)
        left = 20
        surf = text.render("Accuracy: %0.2f %%" % accuracy,
                           True, colour)
        self.win_surf.blit(surf, (left, 20))

        surf = text.render("Enemies killed: %d" % stats['monsters_killed'],
                           True, colour)
        self.win_surf.blit(surf, (left, 40))

        surf = text.render("Enemies missed: %d" % stats['monsters_missed'],
                           True, colour)
        self.win_surf.blit(surf, (left, 60))

    def plot_fuel(self, fuel, max_fuel, colour):
        """ Plots text statistics, but doesn't display them. """
        left = 20
        text = pygame.font.Font(None, 20)

        surf = text.render("Fuel burned: %0.2f" % (max_fuel - fuel),
                           True, colour)
        self.win_surf.blit(surf, (left, 80))

        surf = text.render("Fuel remaining: %0.2f" % fuel,
                           True, colour)
        self.win_surf.blit(surf, (left, 100))

    def plot_health(self, health, damage, max_health, colour):
        """ Display hero health info. """
        left = 20
        try:
            percentage = float(health) / max_health * 100
        except ZeroDivisionError:
            accuracy = 0.0
        text = pygame.font.Font(None, 20)
        surf = text.render("Health: %0.1f %%" % percentage,
                           True, colour)
        self.win_surf.blit(surf, (left, 120))

        surf = text.render("Remaining: %0.2f" % health,
                           True, colour)
        self.win_surf.blit(surf, (left, 140))

    def loadimages(self):
        """ Returns a dictionary of pygame.image entries. """
        image_set = {} 
        image_set['ship'] = pygame.image.load('images/ship.png').convert()

        image_set['enemy_1'] = pygame.image.load('images/enemy_1.png').convert()
        image_set['enemy_2'] = pygame.image.load('images/enemy_2.png').convert()

        sprite_sheet = pygame.image.load("images/explosion_1.png")
        explosion = [
            sprite_sheet.subsurface((46,46,100,100)),
            sprite_sheet.subsurface((238,238,100,100)),
            sprite_sheet.subsurface((430,430,100,100)),
            sprite_sheet.subsurface((622,622,100,100)),
            sprite_sheet.subsurface((814,814,100,100)),
        ]
        image_set['explosion'] = explosion
        return image_set

    def terminate(self):
        """ Shut 'er down. """
        pygame.quit()   # uninitialize
        sys.exit()


if __name__ == "__main__":
    app = PewPew()  # Instantiate new app
    app.run()

