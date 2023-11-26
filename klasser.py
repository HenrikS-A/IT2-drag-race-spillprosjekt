import pygame
from konstanter import SKJERM_BREDDE


class Spillobjekt:
    def __init__(self, bildeurl: str, storrelse: float):
        self.originalt_bilde = pygame.image.load(bildeurl).convert_alpha()
        self.original_storrelse = self.originalt_bilde.get_size()
        self.bilde = pygame.transform.scale(self.originalt_bilde, (self.original_storrelse[0] * storrelse, self.original_storrelse[1] * storrelse))
        self.ramme = self.bilde.get_rect()
        self.font = pygame.font.SysFont("Open Sans", 28)
        self.font_hint = pygame.font.SysFont("Open Sans", 18)

    def tegn(self, vindu: pygame.Surface):
        vindu.blit(self.bilde, self.ramme)

class Bakgrunn(Spillobjekt):
    def __init__(self, bildeurl, storrelse):
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
    def __init__(self, bildeurl, storrelse, y_verdi: int):
        super().__init__(bildeurl, storrelse)
        self.fart = 1 # Startfarten for begge bilene
        self.ramme.y = y_verdi
        self.startfartsvisning_verdi = 0
    
    def oke_fart(self, fartsokning: float):
        self.fart += fartsokning

    def flytt_bil(self):
        self.ramme.x += self.fart

    def hent_frontkoordinat(self, sentrum_til_front: int) -> int:
        return self.ramme.centerx + sentrum_til_front

    def fartsvisning(self, vindu: pygame.Surface):
        # Lager en slags animasjon på starten slik at farten starter på 0 og øker gradvis til 20
        if self.fart <= 1 and self.startfartsvisning_verdi < 40:
            tekst_surface = self.font.render(f"Fart: {round(self.startfartsvisning_verdi * 0.5)} km/h", True, "black")
            vindu.blit(tekst_surface, ((SKJERM_BREDDE // 2) - (tekst_surface.get_width() // 2), 600)) 
            self.startfartsvisning_verdi += 1
        else:
            # Ellers viser den farten
            tekst_surface = self.font.render(f"Fart: {round(self.fart, 2) * 20} km/h", True, "black")
            vindu.blit(tekst_surface, ((SKJERM_BREDDE // 2) - (tekst_surface.get_width() // 2), 600)) 
        
        # Tips for å forstå hva man må gjøre
        tips_surface = self.font_hint.render("Trykk raskt på mellomrom for å øke farten", True, "black")
        vindu.blit(tips_surface, ((SKJERM_BREDDE // 2) - (tips_surface.get_width() // 2), 680)) 

    def reset_bil(self):
        self.ramme.x = 0
        self.fart = 1
        self.startfartsvisning_verdi = 0
