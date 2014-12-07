import pygame

class Renderer(object):
    """ Render the world. """

    def __init__(self, win_surf, world):
        self.surf = win_surf
        self.world = world
        self.BG_COLOR = (10, 10, 10)

    def render(self):
        # Start with a blank screen
        self.surf.fill(self.BG_COLOR)

        self.surf.blit(*self.world.hero.draw())
        for monster in self.world.monsters:
            self.surf.blit(*monster.draw())
        for explosion in self.world.explosions:
            self.surf.blit(*explosion.draw())
        for bullet in self.world.bullets:
            # Bullets are filled rects, for now.
            pygame.draw.rect(self.surf, *bullet.draw())

        # Text displays
        colour = (180, 180, 255)
        self.plot_stats(self.world.stats, colour)
        self.plot_fuel(self.world.hero.fuel,
                       self.world.hero.max_fuel, colour)
        self.plot_health(self.world.hero.health,
                         self.world.hero.damage,
                         self.world.hero.max_health, colour)

        pygame.display.update()
        return None

    def plot_stats(self, stats, colour):
        """ Plots text statistics, but doesn't display them. """
        try:
            accuracy = float(stats['bullets_hit']) / stats['bullets_fired'] * 100
        except ZeroDivisionError:
            accuracy = 0.0
        text = pygame.font.Font(None, 20)
        left = 20
        surf = text.render("Accuracy: %0.2f %%" % accuracy, True, colour)
        self.surf.blit(surf, (left, 20))

        surf = text.render("Enemies killed: %d" % stats['monsters_killed'],
                           True, colour)
        self.surf.blit(surf, (left, 40))

        surf = text.render("Enemies missed: %d" % stats['monsters_missed'],
                           True, colour)
        self.surf.blit(surf, (left, 60))

    def plot_fuel(self, fuel, max_fuel, colour):
        """ Plots text statistics, but doesn't display them. """
        left = 20
        text = pygame.font.Font(None, 20)

        surf = text.render("Fuel burned: %0.2f" % (max_fuel - fuel),
                           True, colour)
        self.surf.blit(surf, (left, 80))

        surf = text.render("Fuel remaining: %0.2f" % fuel, True, colour)
        self.surf.blit(surf, (left, 100))

    def plot_health(self, health, damage, max_health, colour):
        """ Display hero health info. """
        left = 20
        try:
            percentage = float(health) / max_health * 100
        except ZeroDivisionError:
            accuracy = 0.0
        text = pygame.font.Font(None, 20)
        surf = text.render('Health: %0.1f %%' % percentage, True, colour)
        self.surf.blit(surf, (left, 120))

        surf = text.render('Remaining: %0.2f' % health, True, colour)
        self.surf.blit(surf, (left, 140))

