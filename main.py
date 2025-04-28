import pygame
import sys
from config import Config
from game_objects.truck import Truck
from game_objects.station import Station
from game_objects.helicopter import Helicopter
from game_objects.ui import UI

# Initialisiere Pygame
pygame.init()

# Fenstergröße
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Fenster erstellen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TS2")

# Farben (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
#BLUE = (0, 100, 255)

# Clock für FPS
clock = pygame.time.Clock()

# Schriftart
font = pygame.font.SysFont(None, 60)

# lkw speed
speed = Config.LKW_SPEED

# LKW, Stationen, Heli, UI erstellen
lkw = Truck(300, 300, "assets/bilder/lkw.png")
quelle = Station(0, 0, "assets/bilder/quelle.png", "quelle")
ziel = Station(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 200, "assets/bilder/ziel.png", "ziel")
heli = Helicopter(700, 50, "assets/bilder/heli.png")
ui = UI()



# Tankstelle laden
tankstelle_img = pygame.image.load("assets/bilder/tankstelle.png")
tankstelle_img = pygame.transform.scale(tankstelle_img, (64, 64))

# Position Tankstelle
tankstelle_x = 700  # X-Position der Tankstelle
tankstelle_y = 500  # Y-Position der Tankstelle



# Hintergrundbild laden
startscreen_img = pygame.image.load("assets/bilder/deckblatt.png")
startscreen_img = pygame.transform.scale(startscreen_img, (SCREEN_WIDTH, SCREEN_HEIGHT))



# Menü-Status
game_state = "menu"  # mögliche Zustände: menu, running, paused, lost, win
#game_running = False

def draw_menu():
    screen.fill(WHITE)
    screen.blit(startscreen_img, (0, 0))

    # Menü-Buttons
    start_text = font.render("START", True, WHITE)
    pause_text = font.render("PAUSE", True, WHITE)
    restart_text = font.render("RESTART", True, WHITE)

    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 200))
    screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 300))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))

def main_game():
    # Hintergrund weiß füllen
    screen.fill(WHITE)

    # Quelle zeichnen
    quelle.draw(screen)

    # Ziel zeichnen
    ziel.draw(screen)

    # Tankstelle anzeigen
    screen.blit(tankstelle_img, (tankstelle_x, tankstelle_y))

    # Tastaturabfrage für LKW-Bewegung
    keys = pygame.key.get_pressed()
    lkw.move(keys)

    #heli bewegen und Kollision prüfen
    heli.move(lkw)
    heli.check_collision(lkw)
    heli.draw(screen)

    # LKW zeichnen
    lkw.draw(screen)
     
    # Truck bei Quelle laden

    if lkw.get_rect().colliderect(quelle.get_rect()) and lkw.erz == 0 and quelle.erz_vorrat >= lkw.capacity:
        lkw.erz = lkw.capacity
        quelle.erz_vorrat -= lkw.capacity
    

    # Truck bei Ziel abladen
    if lkw.get_rect().colliderect(ziel.get_rect()) and lkw.erz > 0:
        ziel.erz_empfangen += lkw.erz
        lkw.erz = 0

    # Tanken, wenn LKW Tankstelle berührt
    if lkw.get_rect().colliderect(pygame.Rect(tankstelle_x, tankstelle_y, 64, 64)):
        lkw.tanken()
    
    
    # Fuel-Anzeige unten links
    font_small = pygame.font.SysFont(None, 24)

    fuel_text = font_small.render(f"Treibstoff: {lkw.fuel}%", True, BLACK)
    screen.blit(fuel_text, (10, SCREEN_HEIGHT - 30))

    quelle_text = font_small.render(f"Quelle: {quelle.erz_vorrat}", True, BLACK)
    #quelle_text = font_small.render(f"Quelle: {quelle.erz_vorrat}", True, BLACK)
    lkw_text = font_small.render(f"LKW: {lkw.erz}", True, BLACK)
    ziel_text = font_small.render(f"Ziel: {ziel.erz_empfangen}", True, BLACK)


    screen.blit(quelle_text, (20, 60))
    screen.blit(lkw_text, (20, 90))
    screen.blit(ziel_text, (370, 450))
    
    # Sieg-/Verlustbedingungen prüfen
    ziel_erforderlich = (Config.WIN_THRESHOLD_PERCENT / 100) * Config.TOTAL_ERZ

    if ziel.erz_empfangen >= ziel_erforderlich:
        screen.fill((0, 0, 0))  # Bildschirm schwarz (oder leicht transparent Overlay)
        font_small = pygame.font.SysFont(None, 72)
        win_text = font_small.render("Sieg! Genügend Erz geliefert! drück 'R' für Restart", True, (0, 255, 0))
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
        pygame.display.flip()

    if quelle.erz_vorrat == 0 and lkw.erz == 0 and ziel.erz_empfangen < ziel_erforderlich:
        screen.fill((0, 0, 0))
        font_small = pygame.font.SysFont(None, 72)
        lose_text = font_small.render("Niederlage! Erz verloren! drück 'R' für Restart", True, (255, 0, 0))
        screen.blit(lose_text, (SCREEN_WIDTH // 2 - lose_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
        pygame.display.flip() 
    
    # --- Fuel leer prüfen ---
    if lkw.fuel <= 0:
        screen.fill((0, 0, 0))
        font_big = pygame.font.SysFont(None, 50)
        fuel_empty_text = font_big.render("Niederlage! Treibstoff ist 0! Drück 'R' für Restart", True, (255, 0, 0))
        screen.blit(fuel_empty_text, (SCREEN_WIDTH // 2 - fuel_empty_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
        pygame.display.flip()

        # Spielstatus auf "lost" setzen, damit nichts mehr weiter läuft
        return "lost" 

# Hauptspiel-Schleife
running = True
while running:
    # Events prüfen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Tasteneingabe prüfen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state in ["menu", "paused"]:
                game_state = "running"
                #pygame.mixer.music.unpause()  # (optional) Musik wieder abspielen

            if event.key == pygame.K_p and game_state == "running":
                game_state = "paused"
                #pygame.mixer.music.pause()  # (wenn du Musik hast)

            if event.key == pygame.K_r:
                # Neustart: Reset aller Werte
                lkw.x, lkw.y = 300, 300
                lkw.fuel = 100
                lkw.erz = 0
                quelle.erz_vorrat = Config.TOTAL_ERZ
                ziel.erz_empfangen = 0
                heli.x, heli.y = heli.start_x, heli.start_y
                heli.stealing = False
                heli.drop_timer = 0
                game_state = "menu"
                #pygame.mixer.music.rewind()  # Musik neu starten (optional)

    # Je nach Spielstatus rendern
    if game_state == "menu":
        ui.draw_menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT, startscreen_img)

    elif game_state == "running":
        result = main_game()
        if result == "lost":
            game_state = "lost"
    
    elif game_state == "paused":
        ui.draw_pause(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

    elif game_state == "lost":
        # Hintergrund bleibt schwarz, Text bleibt stehen
        pass
    
    # Fenster aktualisieren
    pygame.display.flip()

    # FPS festlegen (60 Frames pro Sekunde)
    clock.tick(60)

    
# Pygame beenden
pygame.quit()
sys.exit() 
 