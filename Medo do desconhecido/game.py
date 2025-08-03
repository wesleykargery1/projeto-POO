import pygame
from pygame.locals import *
from carro import Carro
from sys import exit

pygame.mixer.init()

tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Medo do desconhecido")
tempo = pygame.time.Clock()

van = pygame.image.load("images/van.png")
van_maior = pygame.transform.scale(van, (400, 400))
fundo = pygame.image.load("background/pixil-frame-0.png")
menu_img = pygame.image.load("background/menu.png")
menu_img = pygame.transform.scale(menu_img, (800, 600))

class EstadoJogo:
    menu = 0
    jogando = 1


class Menu:
    def __init__(self):
        self.fundo_menu = menu_img
    
    def mostrar(self, tela):
        tela.blit(self.fundo_menu, (0, 0))
        
        s = pygame.Surface((800, 600), pygame.SRCALPHA)
        tela.blit(s, (0, 0))


estado = EstadoJogo.menu
menu = Menu()
pos_x = -800
velocidade = 6


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if estado == EstadoJogo.menu:
                estado = EstadoJogo.jogando
                Carro.som_carro() 
                pos_x = -800

    if estado == EstadoJogo.jogando:
        pos_x += velocidade


    tela.blit(fundo, (0, 0))
    
    if estado == EstadoJogo.jogando:
        tela.blit(van_maior, (pos_x, 150))
    else:
        menu.mostrar(tela)

    pygame.display.flip()
    tempo.tick(60)