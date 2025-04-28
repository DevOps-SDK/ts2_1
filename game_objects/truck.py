# (KlasseLKW)
import pygame
from config import Config

class Truck:
    WIDTH = 64
    HEIGHT = 64

    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        self.x = x
        self.y = y
        self.speed = Config.LKW_SPEED
        self.fuel = 100  # max = 100
        self.capacity = Config.LKW_CAPACITY
        self.erz = 0  # Erzladung des LKW
        self.fuel_usage_timer = 0  # Zeitmesser für Verbrauch

    def use_Fuel(self):
        self.fuel_usage_timer += 1
        if self.fuel_usage_timer >= Config.FUEL_CONSUMPTION_TIME:
            self.fuel -= 1
            self.fuel_usage_timer = 0
            if self.fuel < 0:
                self.fuel = 0   

    def move(self, keys):
        if self.fuel <= 0:
            return 

        if keys[pygame.K_w]:
            self.y -= self.speed
            self.use_Fuel()
        if keys[pygame.K_s]:
            self.y += self.speed
            self.use_Fuel()
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.use_Fuel()
        if keys[pygame.K_d]:
            self.x += self.speed 
            self.use_Fuel() 
        

        # Grenzen prüfen
        if self.x < 0:
           self.x = 0
        if self.x > 800 - self.WIDTH:
           self.x = 800 - self.WIDTH
        if self.y < 0:
           self.y = 0
        if self.y > 600 - self.HEIGHT:
           self.y = 600 - self.HEIGHT

        # Spritverbrauch steuern # Fuel verbrauchen alle 30 Frames (~0.5 Sek bei 60 FPS)
        

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 64, 64)

    def tanken(self):
        self.fuel = 100  # Tankstelle laden
