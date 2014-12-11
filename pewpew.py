#!/usr/bin/env python
import random
import sys

import pygame
from pygame.locals import *

from classes import ship
from classes import monster
from classes import bullet
from classes import wall
from classes import explosion
from classes import world
from classes import renderer

from screens.start import StartScreen
from screens.level import LevelScreen


class PewPew(object):
    """ Primary game object. Not sure this is the best way,
    saw it in someone's game... """

    def __init__(self):
        """Initalize some game constants."""
        pygame.init()   # initialize pygame

        self.W_WIDTH = 800
        self.W_HEIGHT = 600
        self.screen_size = (self.W_WIDTH, self.W_HEIGHT)
        self.FPS = 40
        self.ADD_MONSTER = 40
        self.world = world.World()  # Empty world
        self.renderer = renderer.Renderer(self.screen_size, self.world)

    def run(self):
        """Run the actual game."""

        # Build window
        self.win_surf = self.renderer.create_window()

        # Load our external resources
        self.image_set = self.loadimages()

        # Initialize framerate clock
        fps_clock = pygame.time.Clock()

        # Display Start Screen
        start_screen = StartScreen(self.win_surf, fps_clock, self.FPS)
        start_screen.render()

        #Display Level 1 Screen
        level_screen = LevelScreen(1, self.win_surf, fps_clock, self.FPS)
        level_screen.render()

        #Start the game:
        # Add world items
        self.world.hero = ship.Ship(self.screen_size)   # initialize hero
        self.world.bullets = []
        self.world.monsters = []
        self.world.explosions = []

        sounds = {}
        sounds['shot'] = pygame.mixer.Sound('sounds/blip2.wav')
        sounds['shot'].set_volume(0.2)
        sounds['hit'] = pygame.mixer.Sound('sounds/blip.wav')
        sounds['hit'].set_volume(0.3)
        sounds['explode'] = pygame.mixer.Sound('sounds/beep-41.wav')
        sounds['explode'].set_volume(1.0)
        pygame.mixer.set_num_channels(12)
        pygame.mixer.music.load('sounds/castlevania.mid')
        pygame.mixer.music.play(-1, 0.0)

        walls = [
            wall.Wall(-50, self.W_HEIGHT),
            wall.Wall(self.W_WIDTH, self.W_HEIGHT)
        ]

        self.world.stats = {
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
            time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key in (K_q, K_ESCAPE):
                        self.terminate()
                    elif event.key == K_p:
                        self.pause_game()
                    elif event.key == K_x:  # Reset
                        self.game_over()
                    elif event.key in (K_h, K_LEFT):
                        self.world.hero.activate_thrusters('left')
                    elif event.key in (K_l, K_RIGHT):
                        self.world.hero.activate_thrusters('right')
                    elif event.key == K_SPACE:
                        if len(self.world.bullets) < 2:
                            sounds['shot'].play()
                            b = bullet.Bullet(self.world.hero)
                            self.world.bullets.append(b)
                            self.world.stats['bullets_fired'] += 1
                elif event.type == KEYUP:
                    if event.key in (K_h, K_LEFT):
                        self.world.hero.activate_thrusters('off')
                    elif event.key in (K_l, K_RIGHT):
                        self.world.hero.activate_thrusters('off')
                    elif event.key == K_UP:
                        pass
                    elif event.key == K_DOWN:
                        pass

            win_rect = self.win_surf.get_rect()

            for b in self.world.bullets[:]:
                b.move()
                # look for collisions with monsters
                for m in self.world.monsters[:]:
                    if m.rect.colliderect(b.trail_rect):
                        self.world.stats['bullets_hit'] += 1
                        m.damage(b.strength)
                        m.set_status('injured', time, 50)
                        if m.death:
                            self.world.monsters.remove(m)
                            self.world.stats['monsters_killed'] += 1
                            sounds['explode'].play(maxtime=350)
                            e = explosion.Explosion(m,
                                self.image_set['explosion'])
                            self.world.explosions.append(e)
                        else:
                            sounds['hit'].play()
                        # TODO: Crashes here?
                        self.world.bullets.remove(b)

            for b in self.world.bullets[:]:
                if not win_rect.contains(b.rect):
                    self.world.stats['bullets_missed'] += 1
                    # TODO: Crashes here?
                    self.world.bullets.remove(b)

            if frame_counter >= self.ADD_MONSTER:
                # Trigger a new monster
                frame_counter = 0
                m = monster.Monster(self.screen_size, self.image_set)
                self.world.monsters.append(m)

            for m in self.world.monsters[:]:
                m.update(time)

                if m.rect.colliderect(self.world.hero.rect):
                    self.world.hero.collide(m, 1.0, False)
                    self.world.hero.set_status('injured', time, 50)
                    self.world.hero.damage(m.strength)
                    self.world.monsters.remove(m)
                    self.world.explosions.append(explosion.Explosion(m,
                         self.image_set['explosion']))
                    sounds['explode'].play()
                    if not self.world.hero.death:
                        sounds['hit'].play()
                        continue

                if not win_rect.contains(m.rect):
                    self.world.stats['monsters_missed'] += 1
                    self.world.monsters.remove(m)
                    continue

            if self.world.hero.death:
                e = explosion.Explosion(self.world.hero,
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


            self.renderer.render()

            fps_clock.tick(self.FPS)

        if self.world.hero.death:
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
                    if event.key in (K_ESCAPE, K_q):
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
                    if event.key in (K_ESCAPE, K_q):
                        self.terminate()
                    elif event.key == K_SPACE:
                        paused = False
            fps_clock.tick(self.FPS)


    def loadimages(self):
        """ Returns a dictionary of pygame.image entries. """
        image_set = {}
        image_set['ship'] = pygame.image.load('images/ship.png').convert_alpha()

        image_set['enemy_1'] = pygame.image.load('images/enemy_1_trans.png').convert_alpha()
        image_set['enemy_2'] = pygame.image.load('images/enemy_2.png').convert_alpha()

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

