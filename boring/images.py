import glob

import pygame

from config import *

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((500, 500))

cwd = os.path.dirname(__file__)


def load(path, size=None, vertical_size=None, horizontal_size=None, scale: float = 1):
    img = pygame.image.load(os.path.join(cwd, "../assets", path)).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    elif vertical_size:
        img = pygame.transform.scale(img, (img.get_width() * vertical_size // img.get_height(), vertical_size))
    elif horizontal_size:
        img = pygame.transform.scale(img, (horizontal_size, img.get_height() * horizontal_size // img.get_width()))
    return pygame.transform.scale_by(img, scale)


def load_multiple(path):
    l = []
    for p in glob.glob(os.path.join(cwd, "../..", "assets", path, "*.png")):
        l.append(pygame.image.load(p).convert_alpha())
    return l


def load_character_mood(name, mood) -> pygame.Surface:
    return load(os.path.join("..", "assets", "characters", name, mood + ".png"), scale=0.3)


def load_character(name) -> dict[str, pygame.Surface]:
    """
    Returns a dictionary of the character's images with the name of the image as the key, and the image as the value
    The keys are supposed to be the character's moods
    """
    d = {}
    for path in glob.glob(os.path.join(cwd, "..", "assets", "character", name, "*.png")):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale_by(img, 0.3)
        d[os.path.basename(path).split(".")[0]] = img
    return d


# __________________________Imports___________________________________#

main_menu_bg = load("main_menu/bg.jpg", (WIDTH, HEIGHT))
btn_quit = load("ui/quit.png")
text_contour = load("scenes/ui/text_contour.png")


class CharacterImageLoader:
    def __init__(self):
        self._images = {}

    def get_image(self, name, mood):
        if name not in self._images:
            self._images[name] = {}
        if mood not in self._images[name]:
            self._images[name][mood] = load_character_mood(name, mood)
        return self._images[name][mood]


loader = CharacterImageLoader()

mc = load("main_character/blank_female.png", scale=1.2)

btn_answer_hover = load("ui/ui_dialogue_1_1.png")
btn_answer = load("ui/ui_dialogue_1_2.png")
