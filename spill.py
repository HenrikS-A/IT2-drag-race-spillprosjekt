import pygame
from konstanter import *
from klasser import Bakgrunn, Bil
from ui import Knapp


def lukk_spill():
    pygame.quit()
    raise SystemExit

def reset_spill():
    bakgrunn.reset_bakgrunn()
    pcbil.reset_bil()
    spillerbil.reset_bil()

    game_over = False
    return game_over

# Egen game-loop for game over skjermen
def game_over_skjerm():
    # Overlay surface
    game_over_surface = pygame.Surface((SKJERM_BREDDE, SKJERM_HOYDE))
    game_over_surface.fill(FARGER["MORK_GRA"])
    game_over_surface.set_alpha(200)

    # Tegner bakgrunnen
    vindu.fill(FARGER["GRA"])
    bakgrunn.tegn(vindu)
    pcbil.tegn(vindu)
    spillerbil.tegn(vindu)
    vindu.blit(game_over_surface, (0, 0)) # Plassert slik at den dekker hele skjermen

    # Tegner knappene
    restart_knapp.tegn(vindu)
    lukk_knapp.tegn(vindu)

    # Tekst:
    tekst_surface_game_over = font_game_over.render("GAME OVER", True, FARGER["LILLA"])
    vindu.blit(tekst_surface_game_over, ((SKJERM_BREDDE // 2) - (tekst_surface_game_over.get_width() * 0.5), 130))

    if spillerbil.ramme.centerx > pcbil.ramme.centerx:
        vinner_tekst = "DU VANT!"
    else:
        vinner_tekst = "DU TAPTE"

    tekst_surface_vinner = font_vinner.render(vinner_tekst, True, FARGER["LILLA"])
    vindu.blit(tekst_surface_vinner, ((SKJERM_BREDDE // 2) - (tekst_surface_vinner.get_width() // 2), 250))

    # Oppdaterer skjermen
    pygame.display.flip()
    klokke.tick(FPS)


# 1. Oppsett
pygame.init()

vindu = pygame.display.set_mode((SKJERM_BREDDE, SKJERM_HOYDE))
klokke = pygame.time.Clock()
pygame.display.set_caption("Drag Race") 

# Ulike fonttyper
font_game_over = pygame.font.SysFont("Open Sans", 85)
font_vinner = pygame.font.SysFont("Open Sans", 30)

# Lager klasse-instanser
bakgrunn = Bakgrunn("bilder/bakgrunn.jpg", 1.5)
pcbil = Bil("bilder/pcbil.png", 0.35, 230)
spillerbil = Bil("bilder/spillerbil.png", 1.1, 340)
restart_knapp = Knapp("RESTART", 300)
lukk_knapp = Knapp("LUKK SPILL", 400)

# Normalverdier
game_over = False


while True:
    # 2. Håndter input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lukk_spill()
        
        if game_over:
            if event.type == pygame.MOUSEBUTTONUP:
                if restart_knapp.knapp_trykk():
                    game_over = reset_spill()
                if lukk_knapp.knapp_trykk():
                    lukk_spill()
            continue
            # Hopper over å sjekke eventene under hvis spillet er over, går til neste iterasjon på for-loopen

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spillerbil.oke_fart(SPILLER_FARTSOKNING)

    # Hvis spillet er over starter egen game-loop for game over skjermen
    if game_over:
        game_over_skjerm() 
        continue
        # Alt under vil bare kjøre hvis game_over = False.


    # 3. Oppdater spill
    bakgrunn.flytt_bakgrunn()
    spillerbil.flytt_bil()
    pcbil.flytt_bil()
    pcbil.oke_fart(PC_FARTSOKNING)

    # 4. Tegn
    vindu.fill(FARGER["GRA"])

    bakgrunn.tegn(vindu)
    pcbil.tegn(vindu)
    spillerbil.tegn(vindu)
    spillerbil.fartsvisning(vindu)


    # Sjekker om en av bilene har kommet til målstreken:
    if spillerbil.hent_frontkoordinat(SPILLER_AVSTAND_TIL_FRONT) > SKJERM_BREDDE or pcbil.hent_frontkoordinat(PC_AVSTAND_TIL_FRONT) > SKJERM_BREDDE:
        game_over = True

    pygame.display.flip()
    klokke.tick(FPS)
