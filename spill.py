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
        self.knapp_surface = pygame.Surface((300, 80))
        self.knapp_surface_skygge = pygame.Surface((300, 80))
        self.knapp_surface.fill((150, 150, 150))
        self.knapp_surface_skygge.fill((60, 64, 66))
        self.ramme = self.knapp_surface.get_rect()
        self.ramme.x = (SKJERM_BREDDE // 2) - (self.ramme.width // 2) # Plasserer knappen sentrert

        self.tekst_surface = font.render(tekst, True, "black")

    def tegn(self, vindu):
        vindu.blit(self.knapp_surface_skygge, (self.ramme.x + 5, self.ramme.y + 5)) # Forskyver skyggen i forhold til knappen
        vindu.blit(self.knapp_surface, self.ramme)
        
        # Plasserer teksten midt på knappen
        self.knapp_surface.blit(self.tekst_surface, ((self.knapp_surface.get_width() // 2) - (self.tekst_surface.get_width() // 2), (self.knapp_surface.get_height() // 2) - (self.tekst_surface.get_height() // 2)))


    ## SPØRRE MARTIN OM DENNE!
    def knapp_trykk(self): #func
        mus_posisjon = pygame.mouse.get_pos()
        if self.ramme.collidepoint(mus_posisjon):  # sjekker om musen er i knapp-rammen når man trykker
            # returnverdi = func()
            return True



def reset_spill():
    bakgrunn.reset_bakgrunn()
    pcbil.reset_bil()
    spillerbil.reset_bil()

    game_over = False
    return game_over


## GJØRE OM DETTE TIL KLASSE ???
def game_over_skjerm():
    game_over_surface = pygame.Surface((SKJERM_BREDDE, SKJERM_HOYDE))
    game_over_surface.fill((32, 33, 36))
    game_over_surface.set_alpha(200)
    vindu.blit(game_over_surface, (0, 0)) # Plassert slik at den dekker hele skjermen
    

    # spillerbil.fart = 1
    # bakgrunn.scroll_fart = 


    # tegne_tekst(game_over_surface, "Open Sans", 50, "GAME OVER", (234, 128, 252), ((SKJERM_BREDDE // 2) - (tekst_surface.get_width() * 0.5), 300))

    tekst_surface_game_over = font_game_over.render("GAME OVER", True, (234, 128, 252))
    vindu.blit(tekst_surface_game_over, ((SKJERM_BREDDE // 2) - (tekst_surface_game_over.get_width() * 0.5), 130))

    if spillerbil.ramme.centerx > pcbil.ramme.centerx:
        vinner_tekst = "DU VANT!"
    else:
        vinner_tekst = "DU TAPTE"

    tekst_surface_vinner = font_vinner.render(vinner_tekst, True, (234, 128, 252))
    vindu.blit(tekst_surface_vinner, ((SKJERM_BREDDE // 2) - (tekst_surface_vinner.get_width() * 0.5), 250))

    restart_knapp.tegn(vindu)
    lukk_knapp.tegn(vindu)





def lukk_spill():
    pygame.quit()
    raise SystemExit


# def tegne_tekst(vindu, fonttype: str, skriftstorrelse: int, tekst: str, farge: str | tuple, plassering: tuple):
#     font = pygame.font.SysFont(fonttype, skriftstorrelse)
    
#     tekst_surface = font.render(tekst, True, farge)
#     vindu.blit(tekst_surface, plassering)






# 1. Oppsett
pygame.init()

SKJERM_BREDDE = 1280
SKJERM_HOYDE = 720
FPS = 60

vindu = pygame.display.set_mode((SKJERM_BREDDE, SKJERM_HOYDE))
klokke = pygame.time.Clock()
pygame.display.set_caption("Drag Race") 

## FIKSE !!!
font = pygame.font.SysFont("Open Sans", 28) # Skrifttype
font_game_over = pygame.font.SysFont("Open Sans", 85)
font_vinner = pygame.font.SysFont("Open Sans", 30)


# Lager klasse-instanser
bakgrunn = Bakgrunn("bilder/bakgrunn.jpg", 1.5)
pcbil = Bil("bilder/pcbil.png", 0.35)
spillerbil = Bil("bilder/spillerbil.png", 1.1)
restart_knapp = Knapp("RESTART")
lukk_knapp = Knapp("LUKK SPILL")

# Normalverdier
pcbil.ramme.y = 230
spillerbil.ramme.y = 340
game_over = False
restart_knapp.ramme.y = 300
lukk_knapp.ramme.y = 400
startfartsvisning = 0.0 





while True:
    # 2. Håndter input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lukk_spill()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spillerbil.fart += spillerbil.spiller_fartsokning

        if event.type == pygame.MOUSEBUTTONUP:
            if restart_knapp.knapp_trykk():
                game_over = reset_spill()
            if lukk_knapp.knapp_trykk():
                lukk_spill()
            #game_over = restart_knapp.knapp_trykk(reset_spill)
        
            
    # 3. Oppdater spill
    if not game_over:
        bakgrunn.flytt_bakgrunn()
        pcbil.flytt_bil()
        spillerbil.flytt_bil()


    # 4. Tegn
    vindu.fill((150, 150, 150))

    # Tegner spillobjektene
    bakgrunn.tegn(vindu)
    pcbil.tegn(vindu)
    spillerbil.tegn(vindu)

    # Tegner tekst, så lenge game_over ikke er True
    if not game_over:

        # Gjør at farten som blir skrevet ikke starter på 20, men at det er en liten slags animasjon fra 0-20.
        if spillerbil.fart <= 1 and startfartsvisning < 40:
            tekst_surface = font.render(f"Fart: {round(startfartsvisning * 0.5, 2)} km/h", True, "black")
            vindu.blit(tekst_surface, ((SKJERM_BREDDE // 2) - (tekst_surface.get_width() * 0.5), 600)) 
            startfartsvisning += 1

        else:
            tekst_surface = font.render(f"Fart: {round(spillerbil.fart, 2) * 20} km/h", True, "black")
            vindu.blit(tekst_surface, ((SKJERM_BREDDE // 2) - (tekst_surface.get_width() * 0.5), 600)) 

    # Game Over:
    if spillerbil.ramme.centerx + 150 > SKJERM_BREDDE or pcbil.ramme.centerx + 145 > SKJERM_BREDDE:
        game_over = True

    if game_over:
        game_over_skjerm()
        


    pygame.display.flip()
    klokke.tick(FPS)
