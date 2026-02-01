import pygame
import random

LARGURA = 800
ALTURA = 600

pygame.init()
pygame.mixer.init()

fundo_battle = pygame.image.load("background/battle.png").convert()
fundo_battle = pygame.transform.scale(fundo_battle, (LARGURA, ALTURA))

fundo_game_over = pygame.image.load("background/GameOver.png").convert()
fundo_game_over = pygame.transform.scale(fundo_game_over, (LARGURA, ALTURA))

fundo_vitoria = pygame.image.load("background/vitoria.png").convert()
fundo_vitoria = pygame.transform.scale(fundo_vitoria, (LARGURA, ALTURA))

pygame.mixer.music.load("sounds/SPAWN.mp3")
pygame.mixer.music.set_volume(0.5)

som_hit_boss = pygame.mixer.Sound("sounds/Ataque.mp3")
som_hit_boss.set_volume(0.7)

som_hit_player = pygame.mixer.Sound("sounds/Dano.mp3")
som_hit_player.set_volume(0.7)


class Jogador:
    def __init__(self):
        self.rect = pygame.Rect(380, 480, 40, 40)
        self.vel = 5
        self.vida = 5

        self.sprite = pygame.image.load("sprites/alma.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (40, 40))

        self.vida_sprite = pygame.image.load("sprites/vida.png").convert_alpha()
        self.vida_sprite = pygame.transform.scale(self.vida_sprite, (24, 24))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.vel
        if keys[pygame.K_d]:
            self.rect.x += self.vel
        if keys[pygame.K_w]:
            self.rect.y -= self.vel
        if keys[pygame.K_s]:
            self.rect.y += self.vel
        self.rect.clamp_ip(pygame.Rect(0, 0, LARGURA, ALTURA))

    def draw(self, tela):
        tela.blit(self.sprite, self.rect)
        for i in range(self.vida):
            tela.blit(self.vida_sprite, (20 + i * 28, 560))


class Boss:
    def __init__(self):
        self.rect = pygame.Rect(LARGURA // 2 - 80, 120, 160, 160)
        self.vida = 100

        self.frames = []
        for i in range(11):
            img = pygame.image.load(f"sprites/arvore/arvore{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (self.rect.width, self.rect.height))
            self.frames.append(img)

        self.frame_atual = 0
        self.tempo_animacao = 120
        self.ultimo_frame = pygame.time.get_ticks()

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_frame >= self.tempo_animacao:
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            self.ultimo_frame = agora

    def draw(self, tela):
        tela.blit(self.frames[self.frame_atual], self.rect)
        pygame.draw.rect(tela, (60, 60, 60), (300, 60, 200, 15))
        pygame.draw.rect(
            tela,
            (200, 0, 0),
            (300, 60, 200 * (self.vida / 100), 15),
        )


class Ataque:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, LARGURA - 72), -72, 72, 72)
        self.tipo = random.choice(["normal", "saltador", "cacador"])

        if self.tipo == "normal":
            self.sprite = pygame.image.load("sprites/Tronco.png").convert_alpha()
        elif self.tipo == "saltador":
            self.sprite = pygame.image.load("sprites/Slime.png").convert_alpha()
        else:
            self.sprite = pygame.image.load("sprites/Raio.png").convert_alpha()

        self.sprite = pygame.transform.scale(self.sprite, (72, 72))

        self.vel_y = 2
        self.dir = random.choice([-1, 1])
        self.gravidade = 0.5
        self.forca_pulo = -10

    def update(self, jogador):
        if self.tipo == "normal":
            self.rect.y += 2
        elif self.tipo == "saltador":
            self.rect.x += self.dir * 4
            self.rect.y += self.vel_y
            self.vel_y += self.gravidade
            if self.rect.bottom >= ALTURA - 20:
                self.rect.bottom = ALTURA - 20
                self.vel_y = self.forca_pulo
            if self.rect.left <= 0 or self.rect.right >= LARGURA:
                self.dir *= -1
        else:
            if jogador.rect.centerx < self.rect.centerx:
                self.rect.x -= 2.5
            if jogador.rect.centerx > self.rect.centerx:
                self.rect.x += 2.5
            if jogador.rect.centery < self.rect.centery:
                self.rect.y -= 2.5
            if jogador.rect.centery > self.rect.centery:
                self.rect.y += 2.5

    def draw(self, tela):
        tela.blit(self.sprite, self.rect)


class Combate:
    def __init__(self):
        self.jogador = Jogador()
        self.boss = Boss()
        self.game_over = False
        self.vitoria = False

        self.fonte_game_over = pygame.font.Font(None, 48)
        self.fonte_vitoria = pygame.font.Font(None, 36)
        self.fonte = pygame.font.Font(None, 36)

        self.ataques = []
        self.ultimo_spawn = pygame.time.get_ticks()

        self.cooldown = 3000
        self.ultimo_ataque = -self.cooldown

        pygame.mixer.music.play(-1)

    def resetar(self):
        pygame.mixer.music.stop()
        self.__init__()

    def atualizar(self, tela):
        agora = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if self.vitoria:
            pygame.mixer.music.stop()
            tela.blit(fundo_vitoria, (0, 0))

            linhas = [
                "Parabéns!",
                "Você vingou seu pai",
                "matando aquilo que estava",
                "o consumindo!",
            ]

            y = 300
            for linha in linhas:
                texto = self.fonte_vitoria.render(linha, True, (255, 255, 255))
                tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, y))
                y += 40

            if keys[pygame.K_m]:
                return "MENU"
            return None

        if self.game_over:
            pygame.mixer.music.stop()
            tela.blit(fundo_game_over, (0, 0))
            texto = self.fonte_game_over.render(
                "Tentar de novo? Aperte R", True, (255, 255, 255)
            )
            tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 450))
            if keys[pygame.K_r]:
                self.resetar()
            return None

        self.jogador.update()

        if keys[pygame.K_SPACE] and agora - self.ultimo_ataque >= self.cooldown:
            self.boss.vida -= 5
            som_hit_boss.play()
            self.ultimo_ataque = agora

        if agora - self.ultimo_spawn >= 5000:
            self.ataques = [Ataque() for _ in range(5)]
            self.ultimo_spawn = agora

        tela.blit(fundo_battle, (0, 0))

        for ataque in self.ataques[:]:
            ataque.update(self.jogador)
            if ataque.rect.colliderect(self.jogador.rect):
                self.jogador.vida -= 1
                som_hit_player.play()
                self.ataques.remove(ataque)
            elif ataque.rect.top > ALTURA:
                self.ataques.remove(ataque)

        if self.jogador.vida <= 0:
            self.game_over = True
        if self.boss.vida <= 0:
            self.vitoria = True

        self.jogador.draw(tela)
        self.boss.update()
        self.boss.draw(tela)

        for ataque in self.ataques:
            ataque.draw(tela)

        self.desenhar_cooldown(tela)
        return None

    def desenhar_cooldown(self, tela):
        agora = pygame.time.get_ticks()
        restante = self.cooldown - (agora - self.ultimo_ataque)
        if restante <= 0:
            texto = self.fonte.render("Atacar! (Espaço)", True, (0, 255, 0))
            tela.blit(texto, (350, 520))
        else:
            proporcao = restante / self.cooldown
            pygame.draw.rect(tela, (80, 80, 80), (250, 520, 300, 20))
            pygame.draw.rect(
                tela,
                (0, 200, 0),
                (250, 520, 300 * (1 - proporcao), 20),
            )
