import glob
import json
import os
import sys

import pygame

IMAGE_EXTENSIONS = ('.png', '.gif')
SOUND_EXTENSIONS = ('.wav', '.mid', '.midi')

def extract_base_no_ext(filename):
    """ e.g. 'c:/data/image.png' returns 'image' """
    return os.path.splitext(os.path.basename(filename))[0]


class AssetLoader(object):

    def __init__(self, folder=None):
        if folder is not None:
            self.root = folder
        else:
            self.root = os.path.dirname(os.path.realpath(__file__))
        self.images = self.load_images()
        self.sounds = self.load_sounds()

    def load_images(self):
        """ Load images from all sub-dirs in root. """
        folder = os.path.join(self.root, '..', 'images')
        attrib_data = self.load_attrs(folder)

        images = {}
        for f in os.listdir(folder):
            if f.lower().endswith(IMAGE_EXTENSIONS):
                f_full = os.path.join(folder, f)
                attrs = attrib_data.get(f_name, None)
                if attrs is not None:
                    kind = attrs.get('kind', 'sprite')
                    name = attrs.get('name', f_name)
                    coords = attrs.get('coords', None)
                if kind == 'sprite':
                    sprite = pygame.image.load(f_full).convert_alpha()
                    size = surface.get_size()  # (width, height)
                elif kind == 'spritesheet':
                    sheet = pygame.image.load(f_full).convert_alpha()
                    sprite = [sheet.subsurface(coord) for coord in coords]
                    size = sprites[0].get_size()

                key = extract_base_no_ext(f)
                if key in images:
                    print('Image asset name collision! {}'.format(key))
                images[key] = (sprite, size)
        return images


    def load_sounds(self):
        """ Load sounds from all sub-dirs in root. """
        folder = os.path.join(self.root, '..', 'sounds')
        attrib_data = self.load_attrs(folder)

        pygame.mixer.set_num_channels(12)

        sounds = {}
        for f in os.listdir(folder):
            if f.lower().endswith(SOUND_EXTENSIONS):
                f_name = extract_base_no_ext(f)
                f_full = os.path.join(folder, f)
                if f_name in sounds:
                    print('Sound asset name collision! {}'.format(f_name))
                attrs = attrib_data.get(f_name, None)
                if attrs is not None:
                    # Default is sound named after file w/ volume 1.0
                    kind = attrs.get('kind', 'sound')
                    name = attrs.get('name', f_name)
                    volume = attrs.get('volume', 1.0)
                    loops = attrs.get('loops', -1)
                    start = attrs.get('start', 0.0)

                if kind == 'sound':
                    sounds[name] = pygame.mixer.Sound(f_full)
                    sounds[name].set_volume(volume)
                elif kind == 'music':
                    # Save details as tuple for later streaming playblack.
                    sounds[name] = (f_full, loops, start)

        return sounds

    def load_attrs(self, folder):
        """ Load JSON attributes from the given folder. """
        f_name = os.path.join(folder, 'attrs.json')
        try:
            with open(f_name, 'r') as f:
                return json.load(f)
        except IOError:
            print('Attribute file not found: {}'.format(f_name))
        except AttributeError:
            print('Maybe bad JSON in attribs? {}'.format(f_name))
        return None

