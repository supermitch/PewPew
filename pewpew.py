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
from classes import assetloader

from screens.start import StartScreen
from screens.level import LevelScreen


class PewPew(object):
    """ Primary game object. Not sure this is the best way,
    saw it in someone's game... """

    def __init__(self):
        """Initalize some game constants."""
        pygame.init()   # initialize pygame

        self.FPS = 60

        self.W_WIDTH = 800
        self.W_HEIGHT = 600
        self.screen_size = (self.W_WIDTH, self.W_HEIGHT)

        self.renderer = renderer.Renderer(self.screen_size)
        self.assets = assetloader.AssetLoader()
        self.world = world.World(self.screen_size, self.assets)
        self.renderer.world = self.world

    def run(self):
        """Run the actual game."""

        # Initialize framerate clock
        fps_clock = pygame.time.Clock()

        # Display Start Screen
        start_screen = StartScreen(self.renderer.surf, fps_clock, self.FPS)
        start_screen.render()

        #Display Level 1 Screen
        level_screen = LevelScreen(1, self.renderer.surf, fps_clock, self.FPS)
        level_screen.render()

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
        win_rect = self.renderer.surf.get_rect()
        while True:
            # Main game loop
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
                            self.assets.sounds['shot'].play()
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

            self.world.update(time)

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
                            self.world.add_explosion(m)
                            self.assets.sounds['explode'].play(maxtime=350)
                        else:
                            self.assets.sounds['hit'].play()
                        # TODO: Crashes here?
                        self.world.bullets.remove(b)

            for b in self.world.bullets[:]:
                if not win_rect.contains(b.rect):
                    self.world.stats['bullets_missed'] += 1
                    # TODO: Crashes here occasionally?
                    self.world.bullets.remove(b)

            for m in self.world.monsters[:]:
                m.update(time)

                if m.rect.colliderect(self.world.hero.rect):
                    self.world.hero.collide(m, 1.0, False)
                    self.world.hero.set_status('injured', time, 50)
                    self.world.hero.damage(m.strength)
                    self.world.monsters.remove(m)
                    self.world.add_explosion(m)
                    self.assets.sounds['explode'].play()
                    if not self.world.hero.death:
                        self.assets.sounds['hit'].play()
                        continue

                if not win_rect.contains(m.rect):
                    self.world.stats['monsters_missed'] += 1
                    self.world.monsters.remove(m)
                    continue

            if self.world.hero.death:
                self.world.add_explosion(m)
                self.assets.sounds['explode'].play()
                break # out of game loop
            else:
                self.world.hero.update(time)
                for w in walls:
                    if w.rect.colliderect(self.world.hero.rect):
                        self.world.hero.collide(w, 0.5, True)

            # Move to world update
            for e in self.world.explosions[:]:
                e.update()
                if e.complete:
                    self.world.explosions.remove(e)

            self.renderer.render()

            fps_clock.tick(self.FPS)
            self.renderer.plot_fps(fps_clock.get_fps())

            pygame.display.update()

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



    def terminate(self):
        """ Shut 'er down. """
        pygame.quit()   # uninitialize
        sys.exit()


if __name__ == "__main__":
    app = PewPew()  # Instantiate new app
    app.run()

