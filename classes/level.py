class Level(object):
    """ Level base class. """
    def __init__(self):
        self.waves = []
        self.number = None

    def total_monsters(self):
        """ Return the total number of monsters in this level. """
        return sum(1 for wave in self.waves for x in wave[1])

    def end_time(self):
        """ Return the time at which the level should be complete. """
        # Time of last wave plus 5 seconds
        return max(wave[0] for wave in self.waves) + 5


class LevelOne(Level):
    def __init__(self):
        self.waves = [
            #(time, x-pos, type),
            (5, range(300, 481, 40), 'green'),
            (6, range(300, 481, 40), 'green'),
            (7, range(300, 481, 40), 'green'),
            (8, range(300, 481, 40), 'green'),
        ]
        self.number = 1

class LevelTwo(Level):
    def __init__(self):
        self.waves = [
            #(time, x-pos, type),
            (5, range(300, 481, 40), 'green'),
            (8, range(300, 421, 40), 'red'),
            (11, range(200, 601, 100), 'purple'),
            (16, [200 + 50 * i for i in range(8)], 'blue'),
        ]
        self.number = 2

levels = [LevelOne(), LevelTwo()]

