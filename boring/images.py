import glob
import os

import pygame

from boring.config import *

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((500, 500))

cwd = os.path.dirname(__file__)


def load(path, size=None, vertical_size=None, horizontal_size=None):
    img = pygame.image.load(os.path.join(cwd, "../assets", path)).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    elif vertical_size:
        img = pygame.transform.scale(img, (img.get_width() * vertical_size // img.get_height(), vertical_size))
    elif horizontal_size:
        img = pygame.transform.scale(img, (horizontal_size, img.get_height() * horizontal_size // img.get_width()))
    return img


def load_multiple(path):
    l = []
    for p in glob.glob(os.path.join(cwd, "../..", "assets", path, "*.png")):
        l.append(pygame.image.load(p).convert_alpha())
    return l


def load_character(dir_path) -> dict[str, pygame.Surface]:
    """
    Returns a dictionary of the character's images with the name of the image as the key, and the image as the value
    The keys are supposed to be the character's moods
    """
    d = {}
    for path in glob.glob(os.path.join(cwd, "..", "assets", dir_path, "*.png")):
        d[os.path.basename(path).split(".")[0]] = pygame.image.load(path).convert_alpha()
    return d


# __________________________Imports___________________________________#

main_menu_bg = load("main_menu/bg.jpg", (WIDTH, HEIGHT))

characters_images = {}

for character in os.listdir(os.path.join(cwd, "..", "assets", "characters")):
    characters_images[character] = load_character(os.path.join("characters", character))

print(characters_images)
