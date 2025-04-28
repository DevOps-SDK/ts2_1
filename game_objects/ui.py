# (Klasse für Anzeigen, z. B. Fuel oder Menü)
import pygame

class UI:
    def __init__(self):
        self.font_big = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 32)

    def draw_menu(self, screen, screen_width, screen_height, background_img):
        # Hintergrundbild zeichnen
        screen.blit(background_img, (0, 0))

        # Transparentes Rechteck als Overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(10)  # 0 = durchsichtig, 255 = undurchsichtig
        overlay.fill((0, 0, 0))  # Schwarz
        screen.blit(overlay, (0, 0))

        # Texte zeichnen
        start_text = self.font_medium.render("Drücke SPACE zum Starten", True, (255, 255, 255))
        pause_text = self.font_small.render("Drücke P zum Pausieren", True, (200, 200, 200))
        restart_text = self.font_small.render("Drücke R zum Neustarten", True, (200, 200, 200))

        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 200))
        screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, 300))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, 350))

    def draw_pause(self, screen, screen_width, screen_height):
        pause_text = self.font_big.render("PAUSIERT", True, (255, 255, 0))
        screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 2 - 30))


    def draw_fuel(self, screen, fuel, screen_height):
        font = pygame.font.SysFont(None, 24)
        fuel_text = font.render(f"Treibstoff: {fuel}%", True, (0, 0, 0))
        screen.blit(fuel_text, (10, screen_height - 30))

    def draw_erz(self, screen, quelle_erz, lkw_erz, ziel_erz):
        font = pygame.font.SysFont(None, 24)
        quelle_text = font.render(f"Quelle: {quelle_erz}", True, (0, 0, 0))
        lkw_text = font.render(f"LKW: {lkw_erz}", True, (0, 0, 0))
        ziel_text = font.render(f"Ziel: {ziel_erz}", True, (0, 0, 0))

        screen.blit(quelle_text, (20, 20))
        screen.blit(lkw_text, (20, 50))
        screen.blit(ziel_text, (20, 80))