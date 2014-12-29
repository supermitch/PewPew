class Level(object):
    def __init__(self):
        self.waves = []

    def total_monsters(self):
        return sum(1 for wave in self.waves for x in wave[1])

class LevelOne(Level):
    def __init__(self):
        self.waves = [
            #(time, x-pos, type),
            (5, range(300, 481, 40), 'green'),
            (6, range(300, 481, 40), 'green'),
            (7, range(300, 481, 40), 'green'),
            (8, range(300, 481, 40), 'green'),
        ]

class LevelTwo(Level):
    def __init__(self):
        self.waves = [
            #(time, x-pos, type),
            (5, range(300, 481, 40), 'green'),
            (8, range(300, 421, 40), 'red'),
            (11, range(200, 601, 100), 'purple'),
            (16, [200 + 50 * i for i in range(8)], 'blue'),
        ]

levels = [LevelOne(), LevelTwo()]

