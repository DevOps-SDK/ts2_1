# (Klasse für Quelle, Ziel, Tankstelle)
import pygame

class Station:
    def __init__(self, x, y, image_path, station_type):
        self.image = pygame.image.load(image_path)
        if station_type == "tankstelle":
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.rect = pygame.Rect(x, y, 64, 64)
        else:
            self.image = pygame.transform.scale(self.image, (300, 200))  # Groß für Quelle und Ziel
            self.rect = pygame.Rect(x, y, 300, 200)   

        self.x = x
        self.y = y
        self.type = station_type  # "quelle", "ziel"

        # Erzstände nur für Quelle und Ziel
        if self.type == "quelle":
            self.erz_vorrat = 100
        elif self.type == "ziel":
            self.erz_empfangen = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return self.rect        