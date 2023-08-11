from typing import Tuple

from boring import images


class Character:
    def __init__(self, name: str, position: Tuple[int, int]):
        self.name = name
        self.position = position
        self.humeur = "neutral"

        self.image = images.loader.get_image(self.name, self.humeur)
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, screen):
        img = images.loader.get_image(self.name, self.humeur)
        self.rect = img.get_rect(center=self.position)
        screen.blit(img, self.rect)

    def __repr__(self):
        return f"Character({self.name}, {self.position})"
