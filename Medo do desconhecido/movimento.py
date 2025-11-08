import pygame
from lucca import *


personagem = Lucca()
todos_sprites = pygame.sprite.Group(personagem)
class Movimento():
    def mover():              
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