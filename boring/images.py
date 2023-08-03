import glob
import os
from boring.config import *
import pygame

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


# __________________________Imports___________________________________#

main_menu_bg = load("main_menu/bg.jpg", (WIDTH, HEIGHT))

