class GameScene(BaseScene):
    """ Play the game """
    def __init__(self, renderer):
        self.renderer = renderer
        super(StartScene, self).__init__(self.renderer.surf, self.renderer.FPS)

        """ Initalize some game constants """
        self.FPS = 60

        self.W_WIDTH = width
        self.W_HEIGHT = height
        self.screen_size = (self.W_WIDTH, self.W_HEIGHT)
        self.surfaces = GameWorld(self.surf.get_size()).surfaces

        self.world = world.World(self.screen_size, self.assets)
        self.world.levels = level.get_levels()
        self.world.set_level(self.world.levels[self.current_level])
        self.goal = self.world.level.end_time()

        self.assets = assetloader.AssetLoader()
        self.renderer.world = self.world
        self.collider = collider.Collider(self.world)

        self.stats = {
            'fps': self.FPS,
            'bullets_fired': 0,
            'bullets_hit': 0,
            'monsters_killed': 0,
            'monsters_missed': 0,
            'score': 0,
        }
        self.world.stats = self.stats

        result = self.game_loop()

    def set_level(level_number):
        self.current_level = level_number

    def game_loop(self):
        """ Run the game loop """
        time_of_death = None
        level_start = pygame.time.get_ticks() / 1000

        while True:

            time = (pygame.time.get_ticks() / 1000) - level_start

            # TODO: Remove some day
            self.stats['fps'] = self.clock.get_fps()

            if time < 3 and not self.world.stage_start:
                self.world.stage_start = True
                self.assets.sounds['level-success'].play()
            elif time > 3:
                self.world.stage_start = False

            if time > self.goal + 3:
                self.world.set_level(self.world.levels[self.world.level.number])
                self.goal = self.world.level.end_time()
                level_start = pygame.time.get_ticks() / 1000  # Reset timer
                continue

            if time > self.goal and not self.world.stage_clear:
                if self.world.level.number == len(self.world.levels):
                    return 'won'  # Beat the final level
                self.world.stage_clear = True
                self.assets.sounds['level-success'].play()

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type in (KEYUP, KEYDOWN):
                    self.world.hero.receive_message(event.type, event.key)
                    if event.key in (K_q, K_ESCAPE):
                        terminate()
                    elif event.key == K_p:
                        self.pause_game()

            self.world.update(time)

            if self.world.infection >= 100:
                return 'infected'

            self.collider.update()

            if self.world.hero.dead:
                if time_of_death is None:
                    time_of_death = time
                else:
                    if time - time_of_death > 2:
                        return 'died'
            self.renderer.render()

            self.clock.tick(self.FPS)

    def pause_game(self):
        """ Pauses the game. """

        # Semi-transparent background
        s = pygame.Surface(self.renderer.surf.get_size(), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        self.renderer.surf.blit(s, (0, 0))

        text = pygame.font.Font(None, 60)
        surf = text.render("Paused!", True, Color('cornflowerblue'))
        self.renderer.surf.blit(surf, (self.W_WIDTH/2 - surf.get_width()/2,
                                  self.W_HEIGHT/2 - surf.get_height()/2))
        small_text = pygame.font.Font(None, 30)
        surf = small_text.render("(Press spacebar to resume)", True, Color('ivory'))
        self.renderer.surf.blit(surf, (self.W_WIDTH/2 - surf.get_width()/2,
                                  self.W_HEIGHT/2 - surf.get_height()/2 + 60))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key in [K_ESCAPE, K_q]:
                        terminate()
                    elif event.key == K_SPACE:
                        return True


