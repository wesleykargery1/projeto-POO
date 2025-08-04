import pygame
from carro import Carro
from pygame.locals import *
from lucca import Lucca
from sys import exit

pygame.init()
pygame.mixer.init()

largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Medo do desconhecido")
tempo = pygame.time.Clock()

van = pygame.image.load("images/van.png")
van_maior = pygame.transform.scale(van, (400, 400))
fundo_jogo = pygame.image.load("background/pixil-frame-0.png").convert()
fundo_menu = pygame.image.load("background/menu.png").convert()
fundo_hotel = pygame.image.load("background/Hotel.png").convert()

fundo_menu = pygame.transform.scale(fundo_menu, (largura, altura))
fundo_jogo = pygame.transform.scale(fundo_jogo, (largura, altura))
fundo_hotel = pygame.transform.scale(fundo_hotel, (largura, altura))

som_tocado = False

class EstadoJogo:
    menu = 0
    jogando = 1
    transicao_hotel = 2

class Menu:
    def mostrar(self, tela):
        tela.blit(fundo_menu, (0, 0))

estado = EstadoJogo.menu
menu = Menu()
pos_x = -800
velocidade = 6

personagem = Lucca()
todos_sprites = pygame.sprite.Group(personagem)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if estado == EstadoJogo.menu:
                estado = EstadoJogo.jogando
                pos_x = -800
    
    if estado == EstadoJogo.transicao_hotel:
        teclas = pygame.key.get_pressed()
        if teclas[K_UP] or teclas[K_w]:
            personagem.mover('cima')
        elif teclas[K_DOWN] or teclas[K_s]:
            personagem.mover('baixo')
        elif teclas[K_LEFT] or teclas[K_a]:
            personagem.mover('esquerda')
        elif teclas[K_RIGHT] or teclas[K_d]:
            personagem.mover('direita')
        else:
            personagem.parar()

    if estado == EstadoJogo.jogando:
        pos_x += velocidade
        if pos_x > largura:
            estado = EstadoJogo.transicao_hotel

    if estado == EstadoJogo.menu:
        menu.mostrar(tela)
    
    elif estado == EstadoJogo.jogando:
        
        tela.blit(fundo_jogo, (0, 0))
        tela.blit(van_maior, (pos_x, 150))

        if not som_tocado:
            Carro.som_carro()
            som_tocado = True
    
    elif estado == EstadoJogo.transicao_hotel:
        tela.blit(fundo_hotel, (0, 0))
        todos_sprites.draw(tela)
        todos_sprites.update()

    pygame.display.flip()
    tempo.tick(60)