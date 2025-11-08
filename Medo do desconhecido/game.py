import pygame
from sounds import *
from estado import EstadoJogo
from pygame.locals import *
from sys import exit
from movimento import *

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
fundo_recep = pygame.image.load("background/recepção-pixilart.png").convert()
fundo_corredor = pygame.image.load("background/corredor-pixilart.png").convert()


fundo_menu = pygame.transform.scale(fundo_menu, (largura, altura))
fundo_jogo = pygame.transform.scale(fundo_jogo, (largura, altura))
fundo_hotel = pygame.transform.scale(fundo_hotel, (largura, altura))
fundo_recep = pygame.transform.scale(fundo_recep, (largura, altura))
fundo_corredor = pygame.transform.scale(fundo_corredor, (largura, altura))

fonte = pygame.font.Font(None, 36)
tema = Tema()
som_iniciado = False
som_tocado = False

class Menu:
    def mostrar(self, tela):
        tela.blit(fundo_menu, (0, 0))

estado = EstadoJogo.menu
menu = Menu()
pos_x = -800
velocidade = 6

porta_rect = pygame.Rect(300, 120, 220 , 120)
perto_da_porta = False
colidindo_com_carro = False



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if estado == EstadoJogo.menu:
                if not som_iniciado:
                    tema.som_tema()
                    som_iniciado = True
                estado = EstadoJogo.jogando
                pos_x = -800

            if estado == EstadoJogo.transicao_hotel and event.key == K_f and perto_da_porta:
                Porta.som_porta()
                estado = EstadoJogo.recep
                perto_da_porta = False
    
    if estado == EstadoJogo.jogando:
        pos_x += velocidade
        tela.blit(fundo_jogo, (0, 0))
        tela.blit(van_maior, (pos_x, 150))

        if not som_tocado:
            Carro.som_carro()
            som_tocado = True
        if pos_x > largura:
            estado = EstadoJogo.transicao_hotel



    if estado == EstadoJogo.menu:
        menu.mostrar(tela)

    if estado == EstadoJogo.transicao_hotel:
        tela.blit(fundo_hotel, (0, 0))
        tela.blit(van_maior, (10, 60))
        colisao_carro = pygame.Rect(140, 0, 115, 2000)
        colisao_cima = pygame.Rect(0, 200 , 2000, 20)
        colisao_baixo = pygame.Rect(0, 365, 2000, 20)
        colisao_direita = pygame.Rect(830, 0, 20, 800)
        pos_anterior_x = personagem.rect.x
        pos_anterior_y = personagem.rect.y
        
        Movimento.mover()

        colidindo_com_carro = personagem.rect.colliderect(colisao_carro)
        colidindo_cima = personagem.rect.colliderect(colisao_cima)
        colidindo_baixo = personagem.rect.colliderect(colisao_baixo)
        colidindo_direita = personagem.rect.colliderect(colisao_direita)

        if colidindo_com_carro or colidindo_cima or colidindo_baixo or colidindo_direita:
            
            personagem.rect.x = pos_anterior_x
            personagem.rect.y = pos_anterior_y
           

        todos_sprites.draw(tela)
        todos_sprites.update()

        if personagem.rect.colliderect(porta_rect):
            perto_da_porta = True
        else:
            perto_da_porta = False

        if perto_da_porta:
            texto = fonte.render("Aperte F para entrar", True, (255, 255, 255))
            texto_rect = texto.get_rect(center=(largura // 2, altura - 80))  
        
      
            fundo_texto = pygame.Surface((texto.get_width() + 40, texto.get_height() + 20), pygame.SRCALPHA)
            pygame.draw.rect(fundo_texto, (0, 0, 0, 128),  
                         (0, 0, texto.get_width() + 40, texto.get_height() + 20), 
                         border_radius=10) 
            tela.blit(fundo_texto, (texto_rect.x - 20, texto_rect.y - 10))
        
            tela.blit(texto, texto_rect)
    if estado == EstadoJogo.recep:
        tela.blit(fundo_recep, (0, 0))
        recep = pygame.Rect(400,300, 50, 50)
        co_recep = personagem.rect.colliderect(recep)
        pos_anterior_x = personagem.rect.x
        pos_anterior_y = personagem.rect.y
        
        
        colisao_esquerda = pygame.Rect(-10, 0, 2, 600)
        colisao_direita = pygame.Rect(830, 0, 2, 600)
        colisao_cima = pygame.Rect(0, 0, 800, 20)
        colisao_baixo = pygame.Rect(0, 580, 800, 20) 
        
        Movimento.mover()
        
        colidindo_esquerda = personagem.rect.colliderect(colisao_esquerda)
        colidindo_direita = personagem.rect.colliderect(colisao_direita)
        colidindo_cima = personagem.rect.colliderect(colisao_cima)
        colidindo_baixo = personagem.rect.colliderect(colisao_baixo)
        
        if colidindo_esquerda or colidindo_direita or colidindo_cima or colidindo_baixo:
            personagem.rect.x = pos_anterior_x
            personagem.rect.y = pos_anterior_y

        todos_sprites.draw(tela)
        todos_sprites.update()
        if co_recep:
            #implementar dialogos
            texto = fonte.render("Pressione F para conversar", True, (255, 255, 255))

            texto_rect = texto.get_rect(center=(largura // 2, altura - 80))  
            fundo_texto = pygame.Surface((texto.get_width() + 40, texto.get_height() + 20), pygame.SRCALPHA)
            pygame.draw.rect(fundo_texto, (0, 0, 0, 128),  
                            (0, 0, texto.get_width() + 40, texto.get_height() + 20), 
                            border_radius=10) 
            tela.blit(fundo_texto, (texto_rect.x - 20, texto_rect.y - 10))
            tela.blit(texto, texto_rect)

            #teste
            keys = pygame.key.get_pressed()
            if keys[K_f]:
             exit()
 
    pygame.display.flip()
    tempo.tick(60)
