import pygame

# Klasser
class Figur:
    def __init__(self, bildeurl: str, storrelse: float):
        self.originalt_bilde = pygame.image.load(bildeurl).convert_alpha()
        self.original_storrelse = self.originalt_bilde.get_size()
        self.bilde = pygame.transform.scale(self.originalt_bilde, (self.original_storrelse[0] * storrelse, self.original_storrelse[1] * storrelse))
        self.ramme = self.bilde.get_rect()

    def tegn(self, vindu, x, y):
        vindu.blit(self.bilde, (x, y))



class Bakgrunn(Figur):
    def __init__(self, bildeurl: str, storrelse: float):
        super().__init__(bildeurl, storrelse)

    def tegn(self, vindu, x, y):
        super().tegn(vindu, x, y)


    def flytt_bakgrunn():
        for i in range(2):
            bakgrunn.tegn(vindu, i * bakgrunn.ramme.width + scroll, 0) # Tegner den første bg i (0,0) og den andre bg ved siden av den første. De flytter seg med scroll



class Bil(Figur):
    def __init__(self, bildeurl: str, storrelse: float):
        super().__init__(bildeurl, storrelse)
        self.fart = 0

    def tegn(self, vindu, x, y):
        super().tegn(vindu, x, y)

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



scroll = 0


while True:
    # 2. Håndter input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    
    # 3. Oppdater spill
    # 4. Tegn
    vindu.fill("gray") # Fyller vinduet med hvit bakgrunn, for hver gang loopen kjører.

    
    Bakgrunn.flytt_bakgrunn()
    scroll -= 4.321

    if abs(scroll) > bakgrunn.ramme.width: # absoluttverdien av scoll, siden den blir mer og mer negativ. Gir mer mening sånn
        scroll = 0



    pcbil.tegn(vindu, 100, 230)
    spillerbil.tegn(vindu, 100, 345)



    pygame.display.flip()
    klokke.tick(FPS)
