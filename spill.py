import pygame

# Klasser
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
    def __init__(self, bildeurl: str, storrelse: float):
        super().__init__(bildeurl, storrelse)
        self.fart = 1 # Startfarten for begge bilene
        self.spiller_fartsokning = 0.05

    def flytt_bil(self):
        self.ramme.x += self.fart

    def reset_bil(self):
        self.ramme.x = 0
        self.fart = 1
    

class Knapp:
    def __init__(self, tekst: str):
        self.surface = pygame.Surface((300, 80))
        self.surface_skygge = pygame.Surface((300, 80))
        self.surface.fill((150, 150, 150))
        self.surface_skygge.fill((60, 64, 66))
        self.ramme = self.surface.get_rect()

        self.tekst_surface = font.render(tekst, True, "black")

    def tegn(self, vindu):
        vindu.blit(self.surface_skygge, (self.ramme.x + 5, self.ramme.y + 5)) # Forskyver skyggen i forhold til knappen
        vindu.blit(self.surface, self.ramme)
        
        # Plasserer teksten midt på knappen
        self.surface.blit(self.tekst_surface, ((self.surface.get_width() // 2) - (self.tekst_surface.get_width() // 2), (self.surface.get_height() // 2) - (self.tekst_surface.get_height() // 2)))


    ## SPØRRE MARTIN OM DENNE!
    def knapp_trykk(self, func):
        mus_posisjon = pygame.mouse.get_pos()
        if self.ramme.collidepoint(mus_posisjon):  # sjekker om musen er i knapp-rammen når man trykker
            returnverdi = func()
            return returnverdi



def reset_spill():
    bakgrunn.reset_bakgrunn()
    pcbil.reset_bil()
    spillerbil.reset_bil()

    game_over = False
    return game_over


def game_over_skjerm():
    vindu.fill((32, 33, 36, 50))
    tekst_surface = font.render(f"GAME OVER!", True, (234, 128, 252))
    vindu.blit(tekst_surface, ((SKJERM_BREDDE // 2) - (tekst_surface.get_width() * 0.5), 300))

    restart_knapp.tegn(vindu)





# 1. Oppsett
pygame.init()

SKJERM_BREDDE = 1280
SKJERM_HOYDE = 720
FPS = 60

vindu = pygame.display.set_mode((SKJERM_BREDDE, SKJERM_HOYDE))
klokke = pygame.time.Clock()
pygame.display.set_caption("Drag Race") 
font = pygame.font.SysFont("Open Sans", 24) # Skrifttype


# Lager klasse-instanser
bakgrunn = Bakgrunn("bilder/bakgrunn.jpg", 1.5)
pcbil = Bil("bilder/pcbil.png", 0.35)
spillerbil = Bil("bilder/spillerbil.png", 1.1)
restart_knapp = Knapp("RESTART")

# Normalverdier
pcbil.ramme.y = 230
spillerbil.ramme.y = 340
game_over = False



restart_knapp.ramme.x = 300
restart_knapp.ramme.y = 400





while True:
    # 2. Håndter input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spillerbil.fart += spillerbil.spiller_fartsokning

        if event.type == pygame.MOUSEBUTTONUP:
            game_over = restart_knapp.knapp_trykk(reset_spill)
        
            
    # 3. Oppdater spill
    bakgrunn.flytt_bakgrunn()
    pcbil.flytt_bil()
    spillerbil.flytt_bil()


    # 4. Tegn
    vindu.fill("gray")

    # Tegner spillobjektene
    bakgrunn.tegn(vindu)
    pcbil.tegn(vindu)
    spillerbil.tegn(vindu)

    # Tegner tekst
    tekst_surface = font.render(f"Fart: {round(spillerbil.fart, 2) * 20} km/h", True, "black")
    vindu.blit(tekst_surface, ((SKJERM_BREDDE // 2) - (tekst_surface.get_width() * 0.5), 600)) 

    # Game Over:
    if spillerbil.ramme.centerx + 150 > SKJERM_BREDDE or pcbil.ramme.centerx + 145 > SKJERM_BREDDE:
        game_over = True

    if game_over:
        game_over_skjerm()
        


    pygame.display.flip()
    klokke.tick(FPS)
