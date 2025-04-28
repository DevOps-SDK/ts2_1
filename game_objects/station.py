# (Klasse für Quelle, Ziel, Tankstelle)
import pygame

class Station:
    def __init__(self, x, y, image_path, station_type):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (300, 200))
        self.x = x
        self.y = y
        self.type = station_type  # "quelle", "ziel" oder "tankstelle später umsetzen"
        self.rect = pygame.Rect(self.x, self.y, 300, 200)

        # Erzstände nur für Quelle und Ziel
        if self.type == "quelle":
            self.erz_vorrat = 100
        elif self.type == "ziel":
            self.erz_empfangen = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return self.rect        