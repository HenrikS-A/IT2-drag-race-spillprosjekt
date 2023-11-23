import pygame
from konstanter import FARGER, SKJERM_BREDDE

class Knapp:
    def __init__(self, tekst: str, y_verdi: int):
        self.knapp_surface = pygame.Surface((300, 80))
        self.knapp_surface_skygge = pygame.Surface((300, 80))
        self.knapp_surface.fill(FARGER["GRA"])
        self.knapp_surface_skygge.fill(FARGER["SKYGGE_GRA"])
        self.ramme = self.knapp_surface.get_rect()
        self.ramme.x = (SKJERM_BREDDE // 2) - (self.ramme.width // 2) # Plasserer knappen sentrert
        self.ramme.y = y_verdi
        self.font = pygame.font.SysFont("Open Sans", 28)

        self.tekst_surface = self.font.render(tekst, True, "black")

    def tegn(self, vindu: pygame.Surface):
        vindu.blit(self.knapp_surface_skygge, (self.ramme.x + 5, self.ramme.y + 5)) # Forskyver skyggen i forhold til knappen
        vindu.blit(self.knapp_surface, self.ramme)
        
        # Plasserer teksten midt på knappen
        self.knapp_surface.blit(self.tekst_surface, ((self.knapp_surface.get_width() // 2) - (self.tekst_surface.get_width() // 2), (self.knapp_surface.get_height() // 2) - (self.tekst_surface.get_height() // 2)))

    def knapp_trykk(self):
        mus_posisjon = pygame.mouse.get_pos()
        if self.ramme.collidepoint(mus_posisjon):  # sjekker om musen er i knapp-rammen når man trykker
            return True
        return False
