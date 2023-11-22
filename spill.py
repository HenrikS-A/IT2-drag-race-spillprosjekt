import pygame

class Spillobjekt:
    def __init__(self, bildeurl: str, storrelse: float):
        self.originalt_bilde = pygame.image.load(bildeurl).convert_alpha()
        self.original_storrelse = self.originalt_bilde.get_size()
        self.bilde = pygame.transform.scale(self.originalt_bilde, (self.original_storrelse[0] * storrelse, self.original_storrelse[1] * storrelse))
        self.ramme = self.bilde.get_rect()

    def tegn(self, vindu):
        vindu.blit(self.bilde, self.ramme)

class Bakgrunn(Spillobjekt):
    def __init__(self, bildeurl: str, storrelse: float):
        super().__init__(bildeurl, storrelse)
        self.scroll_fart = 0.1

    # Tegner alltid to bakgrunner etter hverandre, overskriver Spillobjekt sin tegn-funksjon
    def tegn(self, vindu):
        vindu.blit(self.bilde, self.ramme)
        vindu.blit(self.bilde, (self.ramme.x + self.ramme.width, 0))

    def flytt_bakgrunn(self):
        self.ramme.x -= self.scroll_fart # Oppdaterer posisjonen til bagrunnen, flytter den til venstre
        self.scroll_fart += 0.05 # Øker farten som bakgrunnen flytter seg med

        # Når absoluttverdien av posisjonen til bakgrunnsrammen er større enn bakgrunnsbredden, setter jeg posisjonen tilbake til start. Den scroller for evig
        if abs(self.ramme.x) > self.ramme.width:
            self.ramme.x = 0

    def reset_bakgrunn(self):
        self.ramme.x = 0
        self.scroll_fart = 0.1

class Bil(Spillobjekt):
    def __init__(self, bildeurl: str, storrelse: float, y_verdi: int):
        super().__init__(bildeurl, storrelse)
        self.fart = 1 # Startfarten for begge bilene
        self.ramme.y = y_verdi
        self.startfartsvisning_verdi = 0
    
    def oke_fart(self, fartsokning):
        self.fart += fartsokning

    def flytt_bil(self):
        self.ramme.x += self.fart

    def hent_frontkoordinat(self, avstand_fra_sentrum_til_front):
        return self.ramme.centerx + avstand_fra_sentrum_til_front

    def startfartsvisning(self, vindu):
        # Lager en slags animasjon på starten slik at farten starter på 0 og øker gradvis til 20
        if self.fart <= 1 and self.startfartsvisning_verdi < 40:
            tekst_surface = font.render(f"Fart: {round(self.startfartsvisning_verdi * 0.5)} km/h", True, "black")
            vindu.blit(tekst_surface, ((SKJERM_BREDDE // 2) - (tekst_surface.get_width() // 2), 600)) 
            self.startfartsvisning_verdi += 1
        else:
            tekst_surface = font.render(f"Fart: {round(self.fart, 2) * 20} km/h", True, "black")
            vindu.blit(tekst_surface, ((SKJERM_BREDDE // 2) - (tekst_surface.get_width() // 2), 600)) 

    def reset_bil(self):
        self.ramme.x = 0
        self.fart = 1
        self.startfartsvisning_verdi = 0


class Knapp:
    def __init__(self, tekst: str, y_verdi: int):
        self.knapp_surface = pygame.Surface((300, 80))
        self.knapp_surface_skygge = pygame.Surface((300, 80))
        self.knapp_surface.fill((150, 150, 150))
        self.knapp_surface_skygge.fill((60, 64, 66))
        self.ramme = self.knapp_surface.get_rect()
        self.ramme.x = (SKJERM_BREDDE // 2) - (self.ramme.width // 2) # Plasserer knappen sentrert
        self.ramme.y = y_verdi

        self.tekst_surface = font.render(tekst, True, "black")

    def tegn(self, vindu):
        vindu.blit(self.knapp_surface_skygge, (self.ramme.x + 5, self.ramme.y + 5)) # Forskyver skyggen i forhold til knappen
        vindu.blit(self.knapp_surface, self.ramme)
        
        # Plasserer teksten midt på knappen
        self.knapp_surface.blit(self.tekst_surface, ((self.knapp_surface.get_width() // 2) - (self.tekst_surface.get_width() // 2), (self.knapp_surface.get_height() // 2) - (self.tekst_surface.get_height() // 2)))

    def knapp_trykk(self):
        mus_posisjon = pygame.mouse.get_pos()
        if self.ramme.collidepoint(mus_posisjon):  # sjekker om musen er i knapp-rammen når man trykker
            return True


def lukk_spill():
    pygame.quit()
    raise SystemExit

def reset_spill():
    bakgrunn.reset_bakgrunn()
    pcbil.reset_bil()
    spillerbil.reset_bil()

    game_over = False
    return game_over

def game_over_skjerm():
    # Overlay surface
    game_over_surface = pygame.Surface((SKJERM_BREDDE, SKJERM_HOYDE))
    game_over_surface.fill((32, 33, 36))
    game_over_surface.set_alpha(200)

    # Tegner bakgrunnen
    vindu.fill((150, 150, 150))
    bakgrunn.tegn(vindu)
    pcbil.tegn(vindu)
    spillerbil.tegn(vindu)
    vindu.blit(game_over_surface, (0, 0)) # Plassert slik at den dekker hele skjermen

    # Tegner knappene
    restart_knapp.tegn(vindu)
    lukk_knapp.tegn(vindu)

    # Tekst:
    tekst_surface_game_over = font_game_over.render("GAME OVER", True, (234, 128, 252))
    vindu.blit(tekst_surface_game_over, ((SKJERM_BREDDE // 2) - (tekst_surface_game_over.get_width() * 0.5), 130))

    if spillerbil.ramme.centerx > pcbil.ramme.centerx:
        vinner_tekst = "DU VANT!"
    else:
        vinner_tekst = "DU TAPTE"

    tekst_surface_vinner = font_vinner.render(vinner_tekst, True, (234, 128, 252))
    vindu.blit(tekst_surface_vinner, ((SKJERM_BREDDE // 2) - (tekst_surface_vinner.get_width() // 2), 250))



# 1. Oppsett
pygame.init()

SKJERM_BREDDE = 1280
SKJERM_HOYDE = 720
FPS = 60

vindu = pygame.display.set_mode((SKJERM_BREDDE, SKJERM_HOYDE))
klokke = pygame.time.Clock()
pygame.display.set_caption("Drag Race") 

# Ulike fonttyper
font = pygame.font.SysFont("Open Sans", 28)
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
            # Hopper over å sjekke eventene under, går til neste iterasjon på for-loopen

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spillerbil.oke_fart(0.05)


    # Hvis spillet er over vises game over skjermen
    if game_over:
        game_over_skjerm() 

        # Oppdaterer skjermen
        pygame.display.flip()
        klokke.tick(FPS)
        continue
        # Alt under vil bare kjøre hvis game_over = False.


    # 3. Oppdater spill
    bakgrunn.flytt_bakgrunn()
    spillerbil.flytt_bil()
    pcbil.flytt_bil()
    pcbil.oke_fart(0.005)

    # 4. Tegn
    vindu.fill((150, 150, 150))

    bakgrunn.tegn(vindu)
    pcbil.tegn(vindu)
    spillerbil.tegn(vindu)

    spillerbil.startfartsvisning(vindu)


    # Sjekker om en av bilene har kommet til målstreken:
    if spillerbil.hent_frontkoordinat(145) > SKJERM_BREDDE or pcbil.hent_frontkoordinat(150) > SKJERM_BREDDE:
        game_over = True


    pygame.display.flip()
    klokke.tick(FPS)
