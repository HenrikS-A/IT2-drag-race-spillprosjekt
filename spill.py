import pygame

# Klasser
class Figur:
    def __init__(self, bildeurl: str, storrelse: float):
        self.originalt_bilde = pygame.image.load(bildeurl).convert_alpha()
        self.original_storrelse = self.originalt_bilde.get_size()
        self.bilde = pygame.transform.scale(self.originalt_bilde, (self.original_storrelse[0] * storrelse, self.original_storrelse[1] * storrelse))
        self.ramme = self.bilde.get_rect()

    def tegn(self, vindu):
        vindu.blit(self.bilde, self.ramme)



class Bakgrunn(Figur):
    def __init__(self, bildeurl: str, storrelse: float):
        super().__init__(bildeurl, storrelse)

    # Tegner alltid to bakgrunner etter hverandre
    def tegn(self, vindu):
        vindu.blit(self.bilde, self.ramme)
        vindu.blit(self.bilde, (self.ramme.x + self.ramme.width, 0))

    def flytt_bakgrunn(self, scroll_fart: int | float):
        bakgrunn.ramme.x += scroll_fart # Oppdaterer posisjonen til bagrunnen, flytter den til venstre

        # Når posisjonen til bakgrunnsrammen er større enn abs. til bakgrunnsbredden, reseter jeg posisjonen tilbake, og den scroller evig
        if abs(bakgrunn.ramme.x) > self.ramme.width:
            self.ramme.x = 0



class Bil(Figur):
    def __init__(self, bildeurl: str, storrelse: float):
        super().__init__(bildeurl, storrelse)
        self.fart = 0

    # def tegn(self, vindu, x, y):
    #     super().tegn(vindu, x, y)

    def flytt_bil():
        pass





# 1. Oppsett
pygame.init()

SKJERM_BREDDE = 1280
SKJERM_HOYDE = 720
FPS = 60

vindu = pygame.display.set_mode((SKJERM_BREDDE, SKJERM_HOYDE))
klokke = pygame.time.Clock()
pygame.display.set_caption("Drag Race") 
font = pygame.font.SysFont("Open Sans", 24) # Skrifttype



bakgrunn = Bakgrunn("bilder/bakgrunn.jpg", 1.5)

spillerbil = Bil("bilder/spillerbil.png", 1.1)
pcbil = Bil("bilder/pcbil.png", 0.35)



while True:
    # 2. Håndter input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    
    # 3. Oppdater spill
    # 4. Tegn
    vindu.fill("gray") # Fyller vinduet med hvit bakgrunn, for hver gang loopen kjører.

    
    
    bakgrunn.tegn(vindu)
    bakgrunn.flytt_bakgrunn(-10)
    
    





    spillerbil.ramme.x = 100
    spillerbil.ramme.y = 345

    pcbil.ramme.x = 100
    pcbil.ramme.y = 230

    pcbil.tegn(vindu)
    spillerbil.tegn(vindu)



    pygame.display.flip()
    klokke.tick(FPS)
