import pygame
from sounds import *
from estado import EstadoJogo
from pygame.locals import *
from sys import exit
from movimento import *
from dialogo import *

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
fundo_floresta = pygame.image.load("background/floresta1.png").convert()
fundo_floresta2 = pygame.image.load("background/floresta2.png").convert()
fundo_floresta3 = pygame.image.load("background/floresta3.png").convert()

fundo_menu = pygame.transform.scale(fundo_menu, (largura, altura))
fundo_jogo = pygame.transform.scale(fundo_jogo, (largura, altura))
fundo_hotel = pygame.transform.scale(fundo_hotel, (largura, altura))
fundo_recep = pygame.transform.scale(fundo_recep, (largura, altura))
fundo_corredor = pygame.transform.scale(fundo_corredor, (largura, altura))
fundo_floresta = pygame.transform.scale(fundo_floresta, (largura, altura))  
fundo_floresta2 = pygame.transform.scale(fundo_floresta2, (largura, altura))
fundo_floresta3 = pygame.transform.scale(fundo_floresta3, (largura, altura))

fonte = pygame.font.Font(None, 36)

dialogo_recep = Dialogo([
    "Recepcionista: Você não é bem vindo aqui",
    "Lucca: Como assim?",
    "Recepcionista: Eles não te querem aqui",
    "Lucca: Eles?",
    "Recepcionista: Os seres da floresta",
    "Recepcionista: Eles não gostam de cientistas",
    "Lucca: Eu vim aqui apenas para investigar",
    "Repecionista: Tome cuidado garoto",
    "Recepcionista: As coisas não acabaram bem",
    "Recepcionista: Para o ultimo que tentou",
    "Lucca: O nome dele era George?",
    "Recepcionista: Como você sabe?",
    "Lucca: É o nome do meu pai que desapareceu",
    "Recepcionista: Mais um motivo para desistir",
    "Lucca: Eu não posso desistir",
    "Lucca: Eu preciso descobrir o que aconteceu com ele",
    "Recepcionista: Tudo bem",
    "Recepcionista: Vá para o primeiro quarto seguindo a direita",
    "Lucca: Obrigado"
])

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

porta_rect = pygame.Rect(300, 120, 220, 120)
porta_floresta_rect = pygame.Rect(120, 180, 140, 200)  
perto_da_porta = False

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
                tapete_rect = pygame.Rect(150, 380, 500, 50)
                personagem.rect.midbottom = tapete_rect.midbottom
                perto_da_porta = False

    if estado == EstadoJogo.menu:
        menu.mostrar(tela)

    if estado == EstadoJogo.jogando:
        pos_x += velocidade
        tela.blit(fundo_jogo, (0, 0))
        tela.blit(van_maior, (pos_x, 150))
        if not som_tocado:
            Carro.som_carro()
            som_tocado = True
        if pos_x > largura:
            estado = EstadoJogo.transicao_hotel

    if estado == EstadoJogo.transicao_hotel:
        tela.blit(fundo_hotel, (0, 0))
        tela.blit(van_maior, (10, 60))

        colisao_carro = pygame.Rect(140, 0, 115, 2000)
        colisao_cima = pygame.Rect(0, 200, 2000, 20)
        colisao_baixo = pygame.Rect(0, 365, 2000, 20)
        colisao_direita = pygame.Rect(830, 0, 20, 800)

        pos_anterior_x = personagem.rect.x
        pos_anterior_y = personagem.rect.y

        Movimento.mover()

        if (personagem.rect.colliderect(colisao_carro) or
            personagem.rect.colliderect(colisao_cima) or
            personagem.rect.colliderect(colisao_baixo) or
            personagem.rect.colliderect(colisao_direita)):
            personagem.rect.x = pos_anterior_x
            personagem.rect.y = pos_anterior_y

        todos_sprites.draw(tela)
        todos_sprites.update()

        perto_da_porta = personagem.rect.colliderect(porta_rect)

        if perto_da_porta:
            texto = fonte.render("Aperte F para entrar", True, (255, 255, 255))
            texto_rect = texto.get_rect(center=(largura // 2, altura - 80))
            fundo_texto = pygame.Surface((texto.get_width() + 40, texto.get_height() + 20), pygame.SRCALPHA)
            pygame.draw.rect(fundo_texto, (0, 0, 0, 128), fundo_texto.get_rect(), border_radius=10)
            tela.blit(fundo_texto, (texto_rect.x - 20, texto_rect.y - 10))
            tela.blit(texto, texto_rect)

    if estado == EstadoJogo.recep:
        personagem.ajustar_tamanho(True)
        tela.blit(fundo_recep, (0, 0))

        pos_anterior_x = personagem.rect.x
        pos_anterior_y = personagem.rect.y

        colisao_esquerda = pygame.Rect(-10, 0, 2, 600)
        colisao_direita = pygame.Rect(830, 0, 2, 600)
        colisao_cima = pygame.Rect(0, 0, 800, 20)
        colisao_baixo = pygame.Rect(0, 580, 800, 20)

        Movimento.mover()

        if personagem.rect.colliderect(colisao_direita):
            estado = EstadoJogo.corredor
            personagem.rect.left = 10

        elif (personagem.rect.colliderect(colisao_esquerda) or
              personagem.rect.colliderect(colisao_cima) or
              personagem.rect.colliderect(colisao_baixo)):
            personagem.rect.x = pos_anterior_x
            personagem.rect.y = pos_anterior_y

        recep_rect = pygame.Rect(360, 260, 80, 100)
        co_recep = personagem.rect.colliderect(recep_rect)

        todos_sprites.draw(tela)
        todos_sprites.update()

        if co_recep:
            texto = fonte.render("Pressione F para conversar", True, (255, 255, 255))
            texto_rect = texto.get_rect(center=(largura // 2, altura - 80))
            fundo_texto = pygame.Surface((texto.get_width() + 40, texto.get_height() + 20), pygame.SRCALPHA)
            pygame.draw.rect(fundo_texto, (0, 0, 0, 128), fundo_texto.get_rect(), border_radius=10)
            tela.blit(fundo_texto, (texto_rect.x - 20, texto_rect.y - 10))
            tela.blit(texto, texto_rect)

            if pygame.key.get_pressed()[K_f]:
                dialogo_recep.iniciar()
                estado = EstadoJogo.dialogo

    if estado == EstadoJogo.corredor:
        tela.blit(fundo_corredor, (0, 0))

        colisao_porta = pygame.Rect(0, 250, 800, 10)
        colisao_esquerda = pygame.Rect(-10, 0, 2, 600)
        colisao_direita = pygame.Rect(830, 0, 2, 600)
        colisao_baixo = pygame.Rect(0, 580, 800, 20)


        pos_anterior_x = personagem.rect.x
        pos_anterior_y = personagem.rect.y

        Movimento.mover()

 
        if (personagem.rect.colliderect(colisao_porta) or
            personagem.rect.colliderect(colisao_esquerda) or
            personagem.rect.colliderect(colisao_direita) or
            personagem.rect.colliderect(colisao_baixo)):
            personagem.rect.x = pos_anterior_x
            personagem.rect.y = pos_anterior_y

        todos_sprites.draw(tela)
        todos_sprites.update()

        perto_porta_floresta = personagem.rect.colliderect(porta_floresta_rect)

        if perto_porta_floresta:
            texto = fonte.render("Pressione F para entrar", True, (255, 255, 255))
            texto_rect = texto.get_rect(center=(largura // 2, altura - 80))
            fundo_texto = pygame.Surface((texto.get_width() + 40, texto.get_height() + 20), pygame.SRCALPHA)
            pygame.draw.rect(fundo_texto, (0, 0, 0, 128), fundo_texto.get_rect(), border_radius=10)
            tela.blit(fundo_texto, (texto_rect.x - 20, texto_rect.y - 10))
            tela.blit(texto, texto_rect)

            if pygame.key.get_pressed()[K_f]:
                Porta.som_porta()
                estado = EstadoJogo.floresta1
                personagem.rect.midbottom = (400, 520)

    if estado == EstadoJogo.floresta1:
        tela.blit(fundo_floresta, (0, 0))

   
        colisao_linha_esquerda = pygame.Rect(260, 0, 10, 600)
        colisao_linha_direita = pygame.Rect(540, 0, 10, 600)
        colisao_baixo = pygame.Rect(0, 580, 800, 20)
        saida_mapa1 = pygame.Rect(0, -10, 800, 20)

        pos_anterior_x = personagem.rect.x
        pos_anterior_y = personagem.rect.y

        Movimento.mover()

   
        if (personagem.rect.colliderect(colisao_linha_esquerda) or
            personagem.rect.colliderect(colisao_linha_direita) or
            personagem.rect.colliderect(colisao_baixo)):
            personagem.rect.x = pos_anterior_x
            personagem.rect.y = pos_anterior_y

        if personagem.rect.colliderect(saida_mapa1):
            estado = EstadoJogo.floresta2
            personagem.rect.midbottom = (400, 550)

        todos_sprites.draw(tela)
        todos_sprites.update()

    if estado == EstadoJogo.floresta2:
        tela.blit(fundo_floresta2, (0, 0))

        colisao_linha_esquerda = pygame.Rect(260, 0, 10, 600)
        colisao_linha_direita = pygame.Rect(540, 0, 10, 600)
        colisao_baixo = pygame.Rect(0, 580, 800, 20)
        saida_mapa2 = pygame.Rect(0, -10, 800, 20)

        pos_anterior_x = personagem.rect.x
        pos_anterior_y = personagem.rect.y

        Movimento.mover()
        
        if (personagem.rect.colliderect(colisao_linha_esquerda) or
            personagem.rect.colliderect(colisao_linha_direita) or
            personagem.rect.colliderect(colisao_baixo)):
            personagem.rect.x = pos_anterior_x
            personagem.rect.y = pos_anterior_y
        
        if personagem.rect.colliderect(saida_mapa2):
            estado = EstadoJogo.floresta3
            personagem.rect.midbottom = (400, 550)
        todos_sprites.draw(tela)
        todos_sprites.update()
    
    if estado == EstadoJogo.floresta3:
        tela.blit(fundo_floresta3, (0, 0))

        colisao_arvore = pygame.Rect(0, 200, 800, 10)
        colisao_linha_esquerda = pygame.Rect(270, 0, 10, 600)
        colisao_linha_direita = pygame.Rect(550, 0, 10, 600)
        colisao_baixo = pygame.Rect(0, 580, 800, 20)

        pos_anterior_x = personagem.rect.x
        pos_anterior_y = personagem.rect.y

        Movimento.mover()

        if (personagem.rect.colliderect(colisao_arvore) or
            personagem.rect.colliderect(colisao_linha_esquerda) or
            personagem.rect.colliderect(colisao_linha_direita) or
            personagem.rect.colliderect(colisao_baixo)):
            personagem.rect.x = pos_anterior_x
            personagem.rect.y = pos_anterior_y

        todos_sprites.draw(tela)
        todos_sprites.update()

    if estado == EstadoJogo.dialogo:
        tela.blit(fundo_recep, (0, 0))
        dialogo_recep.desenhar(tela, largura, altura)

        if pygame.key.get_pressed()[K_t] and dialogo_recep.ativo:
            dialogo_recep.avancar()
        elif not dialogo_recep.ativo:
            estado = EstadoJogo.recep

    pygame.display.flip()
    tempo.tick(60)

