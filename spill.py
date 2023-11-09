import pygame

# Klasser
class Matbit:
    def __init__(self):
        self.bilde = pygame.image.load("bilder/stemme.png").convert_alpha()
        self.ramme



# 1. Oppsett
pygame.init()

BREDDE = 1280
HOYDE = 720
FPS = 60

vindu = pygame.display.set_mode((BREDDE, HOYDE))
klokke = pygame.time.Clock()

pygame.display.set_caption("Parti Agario") # Navn på vinduet
font = pygame.font.SysFont("Open Sans", 24) # Skrifttype

while True:
    # 2. Håndter input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    
    # 3. Oppdater spill
    # 4. Tegn

    vindu.fill("white") # Fyller vinduet med hvit bakgrunn, for hver gang loopen kjører.


    pygame.draw.circle(vindu, "green", (100, 100), 40) # Tegner en sirkel
    pygame.draw.rect(vindu, "red", (300, 300, 200, 100)) # Tegner et rektangel


    tekst_hallo = font.render("Hallo på deg!", True, "black") # Oppretter tekst
    vindu.blit(tekst_hallo, (BREDDE//2 - tekst_hallo.get_width()//2, HOYDE * 10/100)) # Tegner teksten i midten av x-posisjon og 10% ned fra toppen




    pygame.display.flip() # Oppdaterer skjermen
    klokke.tick(FPS)
