import os

import pygame.font


def get_font(name: str, size: int):
    return pygame.font.Font(os.path.join("assets", "fonts", name), size)
