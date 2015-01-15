"""
This module loads our basic fonts and styles for easy use
in other code.

"""
from collections import namedtuple

import pygame

pygame.font.init()

# Fonts
small = pygame.font.Font(None, 15)
medium = pygame.font.Font(None, 30)
large = pygame.font.Font(None, 60)

# Colors

COLORS = {
    'plain': pygame.Color('ivory'),
    'bright': pygame.Color('white'),
    'bg': pygame.Color('black'),
    'fail': pygame.Color('firebrick'),
    'success': pygame.Color('cornflowerblue'),
}

Colors = namedtuple('Colors', COLORS.keys())
colors = Colors(**COLORS)


