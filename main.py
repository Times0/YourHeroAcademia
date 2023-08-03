import pygame
from boring.config import *
import ctypes

ctypes.windll.user32.SetProcessDPIAware()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Your Hero Academia")
    win = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
    from game import Game
    from menu import MainMenu
    MainMenu(win,Game).run()
    pygame.quit()
