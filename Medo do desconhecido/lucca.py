import pygame
from pygame.locals import *


pygame.init()

class Lucca(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.aumentar = 2.0
        self.no_hotel = False
        
        self.sprites_movimento = {
            'cima': [pygame.transform.scale(pygame.image.load('sprites/lucca-de-costa-andando-1-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar)),
                     pygame.transform.scale(pygame.image.load('sprites/lucca-de-costa-andando-2-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar))],

            'direita': [pygame.transform.scale(pygame.image.load('sprites/lucca-lado-direito-1-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar)),
                        pygame.transform.scale(pygame.image.load('sprites/lucca-lado-direito-2-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar)),
                        pygame.transform.scale(pygame.image.load('sprites/lucca-lado-direito-3-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar)),
                        pygame.transform.scale(pygame.image.load('sprites/lucca-lado-direito-4-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar))],

            'esquerda': [pygame.transform.scale(pygame.image.load('sprites/lucca-andando-esquerdo-1-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar)),
                          pygame.transform.scale(pygame.image.load('sprites/lucca-andando-esquerdo-2-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar)),
                          pygame.transform.scale(pygame.image.load('sprites/lucca-andando-esquerdo-3-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar)),
                          pygame.transform.scale(pygame.image.load('sprites/lucca-andando-esquerdo-4-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar))],

            'baixo': [pygame.transform.scale(pygame.image.load('sprites/lucca-baixo-1-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar)),
                      pygame.transform.scale(pygame.image.load('sprites/lucca-baixo-2-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar))]
        }

        self.sprites_idle = {
            'cima': [pygame.transform.scale(pygame.image.load('sprites/lucca-de-costa-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar))],
            'direita': [pygame.transform.scale(pygame.image.load('sprites/lucca-direito-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar))],
            'esquerda': [pygame.transform.scale(pygame.image.load('sprites/lucca-esquerdo-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar))],
            'baixo': [pygame.transform.scale(pygame.image.load('sprites/lucca-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar)),
                      pygame.transform.scale(pygame.image.load('sprites/lucca-2-pixilart.png'), (32 * self.aumentar, 32 * self.aumentar))]
        }

        self.image = self.sprites_idle['baixo'][0]
        self.rect = self.image.get_rect()
        self.frame = 0
        self.direcao = 'baixo'
        self.estado = 'movendo'
        self.rect.topleft = (800 / 2, 600 / 2)
    

    def ajustar_tamanho(self, no_hotel):
        self.no_hotel = no_hotel
        novo_aumentar = 3.0 if no_hotel else 2.0 
        
        if novo_aumentar != self.aumentar:
            self.aumentar = novo_aumentar

            for direcao in self.sprites_movimento:
                self.sprites_movimento[direcao] = [
                    pygame.transform.scale(img, (32 * self.aumentar, 32 * self.aumentar))
                    for img in self.sprites_movimento[direcao]
                ]
            for direcao in self.sprites_idle:
                self.sprites_idle[direcao] = [
                    pygame.transform.scale(img, (32 * self.aumentar, 32 * self.aumentar))
                    for img in self.sprites_idle[direcao]
                ]
            
            centro_x, centro_y = self.rect.center
            self.rect = self.image.get_rect(center=(centro_x, centro_y))
    def update(self):
        if self.estado == 'movendo':
            self.frame += 0.10
            if self.frame >= len(self.sprites_movimento[self.direcao]):
                self.frame = 0
            self.image = self.sprites_movimento[self.direcao][int(self.frame)]
        elif self.estado == 'idle':
            self.frame += 0.05
            if self.frame >= len(self.sprites_idle[self.direcao]):
                self.frame = 0
            self.image = self.sprites_idle[self.direcao][int(self.frame)]

    def mover(self, direcao):
        self.direcao = direcao
        self.estado = 'movendo'
        if direcao == 'cima':
            self.rect.y -= 5
        elif direcao == 'baixo':
            self.rect.y += 5
        elif direcao == 'esquerda':
            self.rect.x -= 5
        elif direcao == 'direita':
            self.rect.x += 5
    def parar(self):
        self.estado = 'idle'
        self.frame = 0


