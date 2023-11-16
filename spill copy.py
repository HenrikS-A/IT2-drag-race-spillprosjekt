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

    def flytt_bakgrunn(self):   # , scroll_fart: int | float
        self.ramme.x -= self.scroll_fart # Oppdaterer posisjonen til bagrunnen, flytter den til venstre
        self.scroll_fart += 0.05

        # Når posisjonen til bakgrunnsrammen er større enn abs. til bakgrunnsbredden, reseter jeg posisjonen tilbake, og den scroller evig
        if abs(self.ramme.x) > self.ramme.width:
            self.ramme.x = 0



class Bil(Spillobjekt):
    def __init__(self, bildeurl: str, storrelse: float):
        super().__init__(bildeurl, storrelse)

    def flytt_bil(self, bil_fart: int | float):
        self.ramme.x += bil_fart



class Spillerbil(Bil):
    def __init__(self, bildeurl: str, storrelse: float):
        super().__init__(bildeurl, storrelse)
        self.fart = 1

    def sjekk_input(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.fart += 0.05

    def flytt_bil(self):
        self.ramme.x += self.fart
    
    
    




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


pcbil = Bil("bilder/pcbil.png", 0.35)
spillerbil = Spillerbil("bilder/spillerbil.png", 1.1)

pcbil.ramme.y = 230
spillerbil.ramme.y = 340



while True:
    # 2. Håndter input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
        spillerbil.sjekk_input()
            
    
    # 3. Oppdater spill

    bakgrunn.flytt_bakgrunn()


    pcbil.flytt_bil(1)

    spillerbil.flytt_bil()


    # 4. Tegn
    vindu.fill("gray") # Fyller vinduet med hvit bakgrunn, for hver gang loopen kjører.



    bakgrunn.tegn(vindu)



    pcbil.tegn(vindu)
    spillerbil.tegn(vindu)

    
    tekst_surface = font.render(f"Fart: {round(spillerbil.fart, 2) * 20} km/h", True, "black")
    vindu.blit(tekst_surface, ((SKJERM_BREDDE // 2) - (tekst_surface.get_width() * 0.5), 600)) 


    pygame.display.flip()
    klokke.tick(FPS)
