from base import BaseScene

class StartScene(BaseScene):
    """ Game intro screen. """

    def __init__(self, win_surf, FPS):
        super(StartScene, self).__init__(win_surf, FPS)
        self.surfaces = StartWorld(self.surf.get_size()).surfaces

