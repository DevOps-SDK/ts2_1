import pygame
from config import Config

class Helicopter:
    WIDTH = 64
    HEIGHT = 64

    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.speed = Config.HELI_SPEED
        self.stealing = False
        self.drop_timer = 0

    def move(self, truck):
        if self.stealing:
            # Rückflug zur Home-Position
            if self.x < self.start_x:
                self.x += self.speed
            if self.x > self.start_x:
                self.x -= self.speed
            if self.y < self.start_y:
                self.y += self.speed
            if self.y > self.start_y:
                self.y -= self.speed    

            # Wenn angekommen, 7 Sekunden warten und neu starten
            if abs(self.x - self.start_x) < 5 and abs(self.y - self.start_y) < 5:
                self.drop_timer += 1
                if self.drop_timer > Config.DROP_TIME * 60:  # 7 Sekunden bei 60 FPS
                    self.stealing = False
                    self.drop_timer = 0
        else:
            # Verfolgen des Trucks
            if truck.x > self.x:
                self.x += self.speed
            if truck.x < self.x:
                self.x -= self.speed
            if truck.y > self.y:
                self.y += self.speed
            if truck.y < self.y:
                self.y -= self.speed

    def check_collision(self, truck):
        heli_rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
        if heli_rect.colliderect(truck.get_rect()) and not self.stealing:
            if truck.erz >= Config.STEAL_AMOUNT:
                truck.erz -= Config.STEAL_AMOUNT
            else:
                truck.erz = 0
            self.stealing = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))        