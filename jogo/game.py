import pygame
from sys import exit

pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((800,600))
pygame.display.set_caption("Medo do desconhecido")
tempo = pygame.time.Clock()
van = pygame.image.load("van.png")
van_maior = pygame.transform.scale(van, (400,400))
pos_x = -800
velocidade = 6

fundo = pygame.image.load("pixil-frame-0.png")

pygame.mixer.music.load('SOM DE CARRO PASSANDO(MP3_160K).mp3')
pygame.mixer.music.set_volume(5)
pygame.mixer.music.play(1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pos_x += velocidade

    tela.blit(fundo, (0, 0))
    tela.blit(van_maior, (pos_x, 150))

    pygame.display.flip()

    pygame.display.update()
    tempo.tick(60)