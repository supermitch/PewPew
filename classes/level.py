class Level(object):
    """ Level base class. """
    def __init__(self):
        self.number = None
        self.waves = []

    def total_monsters(self):
        """ Return the total number of monsters in this level. """
        return sum(1 for wave in self.waves for x in wave[1])

    def end_time(self):
        """ Return the time at which the level should be complete. """
        # Time of last wave plus 5 seconds
        return max(wave[0] for wave in self.waves) + 10

class LevelOne(Level):
    def __init__(self):
        self.number = 1
        self.waves = [
            #(time, x-pos, type),
            (5, range(300, 481, 40), 'green'),
            (6, range(300, 481, 40), 'green'),
            (7, range(300, 481, 40), 'green'),
            (8, range(300, 481, 40), 'green'),
        ]

class LevelTwo(Level):
    def __init__(self):
        self.number = 2
        self.waves = [
            #(time, x-pos, type),
            (5, range(300, 481, 40), 'green'),
            (8, range(300, 421, 40), 'red'),
            (11, range(200, 601, 100), 'purple'),
            (16, [200 + 50 * i for i in range(8)], 'blue'),
        ]

class LevelThree(Level):
    def __init__(self):
        self.number = 3
        self.waves = [
            #(time, x-pos, type),
            (4, range(300, 481, 40), 'purple'),
            (5, range(300, 421, 40), 'red'),
            (6, range(200, 601, 100), 'purple'),
            (7, range(300, 421, 40), 'red'),
            (8, range(200, 601, 100), 'purple'),
            (9, range(300, 421, 40), 'red'),
            (10, [200 + 50 * i for i in range(8)], 'blue'),
        ]

class LevelFour(Level):
    def __init__(self):
        self.number = 4
        self.waves = [
            #(time, x-pos, type),
            (4, range(300, 481, 20), 'purple'),
            (5, range(320, 501, 20), 'purple'),
            (6, range(200, 601, 50), 'boulder'),
            (7, range(300, 481, 20), 'purple'),
            (8, range(320, 501, 20), 'purple'),
            (9, range(200, 601, 50), 'boulder'),
            (10, range(200, 601, 50), 'red'),
        ]

class LevelFive(Level):
    def __init__(self):
        self.number = 5
        self.waves = [
            #(time, x-pos, type),
            (4, range(300, 481, 40), 'purple'),
            (5, range(300, 421, 40), 'red'),
            (6, range(200, 601, 100), 'purple'),
            (7, range(300, 421, 40), 'red'),
            (8, range(200, 601, 100), 'purple'),
            (9, range(300, 421, 40), 'red'),
            (10, [200 + 50 * i for i in range(8)], 'blue'),
        ]

class LevelSix(Level):
    def __init__(self):
        self.number = 6
        self.waves = [
            #(time, x-pos, type),
            (4, range(300, 481, 40), 'purple'),
            (5, range(300, 421, 40), 'red'),
            (6, range(200, 601, 100), 'purple'),
            (7, range(300, 421, 40), 'red'),
            (8, range(200, 601, 100), 'purple'),
            (9, range(300, 421, 40), 'red'),
            (10, [200 + 50 * i for i in range(8)], 'blue'),
        ]

def get_levels():
    return [
        LevelOne(),
        LevelTwo(),
        LevelThree(),
        LevelFour(),
        LevelFive(),
        LevelSix(),
    ]

