import pygame
import random
pygame.init()
#immagini gioco (costanti)

tubo_basso = pygame.image.load('FlappyBird.assets/tubo.png')
sfondo = pygame.image.load('FlappyBird.assets/sfondo.png')
bird = pygame.image.load('FlappyBird.assets/uccello.png')
gameover = pygame.image.load('FlappyBird.assets/gameover.png')
terreno = pygame.image.load('FlappyBird.assets/base.png')
tubo_alto = pygame.transform.flip(tubo_basso,False,True)

SCHERMO = pygame.display.set_mode((288,512))
 
#costanti gioco

FPS=80
VEL_SFONDO=3
FONT = pygame.font.SysFont('Comic Sans MS',50,bold=True)

class tubi_classe:
    def __init__(self):
        self.x =300
        self.y = random.randint (-75,150)
    def avanza_e_disegna(self):
        self.x-=VEL_SFONDO
        SCHERMO.blit(tubo_basso, (self.x,self.y+210))
        SCHERMO.blit(tubo_alto, (self.x,self.y-210))
    def collisione (self,bird,birdX,birdY):
        tolleranza=8
        bird_lato_dx = birdX+bird.get_width()-tolleranza
        bird_lato_sx = birdX+tolleranza
        tubi_lato_sx=self.x+tubo_basso.get_width()
        tubi_lato_dx = self.x
        bird_lato_su=birdY + tolleranza
        bird_lato_giu = birdY + bird.get_height()-tolleranza
        tubi_lato_su = self.y + 110
        tubi_lato_giu = self.y + 210

        if bird_lato_dx > tubi_lato_dx and bird_lato_sx < tubi_lato_sx:
            if bird_lato_su < tubi_lato_su or bird_lato_giu > tubi_lato_giu:
                haiperso()
    def fra_i_tubi(self,bird,birdX):
        tolleranza=5
        bird_lato_dx = birdX+bird.get_width()-tolleranza
        bird_lato_sx = birdX+tolleranza
        tubi_lato_sx=self.x+tubo_basso.get_width()
        tubi_lato_dx = self.x
        if bird_lato_dx > tubi_lato_dx and bird_lato_sx < tubi_lato_sx:
            return True

def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)
def inizio():
    global birdX, birdY, bird_velY
    global basex
    global tubi
    global punti
    global fra_i_tubi
    birdX,birdY=60,150
    bird_velY=0
    basex=0
    punti=0
    tubi=[]
    tubi.append(tubi_classe())
    fra_i_tubi = False
    


def haiperso():
    SCHERMO.blit(gameover,(50,100))
    aggiorna()

    dead = True
    while dead:
        inizio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                inizio()
                dead = False

def disegna_oggetti():
    ball = pygame.Rect(20,30,30,50)
    SCHERMO.blit(sfondo,(0,0))
    for t in tubi:
        t.avanza_e_disegna()
    SCHERMO.blit(bird, (birdX,birdY))
    SCHERMO.blit(terreno,(basex,400))
    if punti>=10:
        ball = pygame.Rect(20,30,60,50)
        pygame.draw.rect(SCHERMO,(140,225,160),ball)
    else:
        pygame.draw.rect(SCHERMO,(140,225,160),ball)
    punti_render = FONT.render(str(punti),1,(0,0,0))
    SCHERMO.blit(punti_render,(20,20))
    

#CODICE DI GIOCO

inizio()
while True:
    
    #avanzamento base
    basex -= VEL_SFONDO
    if basex<-45:
        basex=0
    #gravità
    bird_velY += 0.26
    birdY+= bird_velY

    #salto
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP ):
            bird_velY=-5
        if event.type == pygame.QUIT:
            pygame.quit()
    #gestione tubi e collisione con essi
    if tubi[-1].x < 50:
        tubi.append(tubi_classe())
    for t in tubi:
        t.collisione(bird,birdX,birdY)
    if not fra_i_tubi:
        for t in tubi:
            if t.fra_i_tubi(bird,birdX):
                fra_i_tubi = True
                break
    if fra_i_tubi:
        fra_i_tubi = False
        for t in tubi:
            if t.fra_i_tubi(bird,birdX):
                fra_i_tubi = True
                break
        if not fra_i_tubi:
            punti+=1

    #collisione con la base
    if (birdY>380):
        haiperso()

    disegna_oggetti()
    aggiorna()
