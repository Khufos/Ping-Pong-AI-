import pygame
import random
from pesos import *

PRETO=0,0,0
BRANCO=255,255,255
VERDE=0,255,0
VERMELHO=255,0,0

fim=False
tamanho=800,600
tela=pygame.display.set_mode(tamanho)
tela_retangulo=tela.get_rect()
tempo=pygame.time.Clock()
pygame.display.set_caption("Jogo Pong")
Yraquete = 0
Xbola = 0
Ybola = 0

class Raquete:
    def __init__(self, tamanho):
        self.imagem=pygame.Surface(tamanho)
        self.imagem.fill(VERDE)
        self.imagem_retangulo=self.imagem.get_rect()
        self.velocidade = 20
        self.imagem_retangulo[0] = 20

    def move(self,  y):
        self.imagem_retangulo[1] += y * self.velocidade
        # Aqui ele pega o Y da raquete
        global Yraquete
        Yraquete = self.imagem_retangulo.centery

    def atualiza(self, tecla):
        if tecla > 0.5:
            self.move(-1)
        if tecla < 0.5:
            self.move(1)
        self.imagem_retangulo.clamp_ip(tela_retangulo)

    def realiza(self):
        tela.blit(self.imagem, self.imagem_retangulo)
Ybola = 0
xbola = 0
erro = 0

class Bola:
    def __init__(self, tamanho):
        self.altura, self.largura = tamanho
        self.imagem=pygame.Surface(tamanho)
        self.imagem.fill(VERMELHO)
        self.imagem_retangulo=self.imagem.get_rect()
        self.velocidade = 10
        self.flag = False               
        self.set_bola()

    def aleatorio(self):
        while True:
            num=random.uniform(-1.0, 1.0)
            if num > -.5 and num < 0.5:
                continue
            else:
                return num

    def set_bola(self):
        x=self.aleatorio()
        y=self.aleatorio()
        self.imagem_retangulo.x = tela_retangulo.centerx
        self.imagem_retangulo.y = tela_retangulo.centery
        self.velo=[x, y]
        self.pos = list(tela_retangulo.center)

    def colide_parede(self):
        if self.imagem_retangulo.y < 0 or self.imagem_retangulo.y > tela_retangulo.bottom - self.altura:
            self.velo[1] *= -1
            self.flag = False

        if self.imagem_retangulo.x < 0 or self.imagem_retangulo.x > tela_retangulo.right - self.largura:
            self.velo[0] *= -1
            if self.imagem_retangulo.x < 0 and self.flag == False:
                placar1.pontos -= 1
                print("Bateu na parede !")
                self.flag = True

    def colide_raquete(self, raquete_rect):
        if self.imagem_retangulo.colliderect(raquete_rect):
            self.velo[0] *= -1
            self.velocidade = 10
            placar1.pontos += 1
            print("Boa voce defendeu !")
            global erro 
            erro = 0       

    def move(self):
        self.pos[0] += self.velo[0] * self.velocidade
        self.pos[1] += self.velo[1] * self.velocidade
        self.imagem_retangulo.center = self.pos

    def atualiza(self, raquete_rect):
        self.colide_parede()
        global Ybola, Xbola
        Ybola = self.imagem_retangulo.y
        Xbola = self.imagem_retangulo.x
        
        self.colide_raquete(raquete_rect)
        self.move()

    def realiza(self):
        tela.blit(self.imagem, self.imagem_retangulo)

class Placar:
    def __init__(self):
        pygame.font.init()
        self.fonte=pygame.font.Font(None, 36)
        self.pontos=10 

    def contagem(self):
        self.text=self.fonte.render("Pontos = " + str(self.pontos), 1, (PRETO))
        self.textpos=self.text.get_rect()
        self.textpos.centerx=tela.get_width() / 2
        tela.blit(self.text, self.textpos)
        tela.blit(tela, (0, 0))
        global erro
        erro = 0
        

raquete=Raquete((10, 50))
bola=Bola((15, 15))
placar1=Placar()


peso1= pesos_4() # peso_4 significa que retorna 4 pesos para fazer a multiplicação  (1) camada de entrada 
peso2= pesos_4() # peso_4 significa que retorna 4 pesos para fazer a multiplicação  (1) camada de entrada 
peso3 = pesos_2() # peso_2 significa que retorna 2 pesos para fazer a multiplicação na (2) camada oculta 
peso4 = pesos_2() # peso_2 significa que retorna 2 pesos para fazer a multiplicação na (2) camada oculta 
peso_fim = peso_final() # O peso final da camada de saida 

class RedeNeural:
    def __init__(self,Yraquete ,Xbola, Ybola , bias = -1):
        self.entradas = np.array([Yraquete,Xbola,Ybola,bias])
        global peso1, peso2, peso3, peso4, peso_fim
        self. peso1 = peso1
        self.peso2 = peso2
        self.peso3 = peso3
        self.peso4 = peso4
        self.peso_fim = peso_fim
        

    def feedforward(self):
        self.peso1 = round(self.tangenteHiperbolica(np.sum(self.entradas * self.peso1)),6)
        self.peso2 = round(self.tangenteHiperbolica(np.sum(self.entradas * self.peso2)),6)
        self.peso3 = round(self.tangenteHiperbolica(np.sum(np.array([self.peso1, self.peso1]) * self.peso3)),6)
        self.peso4 = round(self.tangenteHiperbolica(np.sum(np.array([self.peso2, self.peso2]) * peso4)),6)
        self.resultado = round(self.sigmoid(np.sum(np.array([self.peso3, self.peso4])* self.peso_fim)),6)
        print(self.resultado)
        return self.resultado
        
    def tangenteHiperbolica(self, x):
        th = (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))
        return th
    
    def sigmoid(self,x):
        return 1 / (1 + np.exp(-x))

    def atualizaPesos(self, erro, alpha=0.01):
        
        for i in range(len(peso_fim)):
            if i == 0:
                entrada = self.peso3
            elif i ==1:
                entrada = self.peso4

            peso_fim[i] = peso_fim[i] + (alpha * entrada * erro)        
        
        for i in range(len(peso3)):
            if i == 0:
                entrada1 = self.peso1
            
            if i == 1:
                entrada1 = self.peso2
            
            peso3[i] = peso3[i] + (alpha * entrada1 * erro)
            
            
        for i in range(len(peso4)):
            
            if i == 0:
                entrada2 = self.peso1
            
            if i == 1:
                entrada2 = self.peso2
                
            peso4[i] = peso4[i] = (alpha * entrada2 * erro)
            
        for i in range(len(peso1)):
            peso1[i] = peso1[i] = (alpha * self.entradas[i] * erro)
        
        for i in range(len(peso2)):
            peso2[i] = peso2[i] = (alpha * self.entradas[i]  * erro)
            
        self.resultado

    

while not fim:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim=True
            
    erro = (Yraquete - Ybola) / 100        
    rede = RedeNeural(Yraquete/600, Xbola/800, Ybola/600)
    tecla = rede.feedforward()
    
    with open('dadosTreinamento.txt', 'a') as arquivo:
        arquivo.write(str(Yraquete) + " " + str(Xbola) + " " + str(Ybola) + " " + str(tecla) + "\n")
 

       
       
    
    tela.fill(BRANCO)
    raquete.realiza()
    
    
    bola.realiza()
    raquete.atualiza(tecla)
    bola.atualiza(raquete.imagem_retangulo)
    
    erro = (Yraquete - Ybola) / 100    
    tempo.tick(30)
    rede.atualizaPesos(erro)
    placar1.contagem()
    pygame.display.update()