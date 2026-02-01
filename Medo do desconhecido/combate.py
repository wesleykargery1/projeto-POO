import pygame
import random

LARGURA = 800
ALTURA = 600


class Jogador:
    def __init__(self):
        self.rect = pygame.Rect(380, 480, 40, 40)
        self.vel = 5
        self.vida = 5

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
        pygame.draw.rect(tela, (80, 180, 255), self.rect)

        for i in range(self.vida):
            pygame.draw.rect(tela, (0, 200, 0), (20 + i * 25, 560, 20, 20))


class Boss:
    def __init__(self):
        self.rect = pygame.Rect(LARGURA // 2 - 80, 120, 160, 80)
        self.vida = 100

    def draw(self, tela):
        pygame.draw.rect(tela, (200, 60, 60), self.rect)

        largura_barra = 200
        vida_ratio = self.vida / 100
        pygame.draw.rect(tela, (60, 60, 60), (300, 60, largura_barra, 15))
        pygame.draw.rect(
            tela,
            (200, 0, 0),
            (300, 60, largura_barra * vida_ratio, 15),
        )


class Ataque:
    def __init__(self):
        TAM_ATAQUE = 72
        self.rect = pygame.Rect(
            random.randint(0, LARGURA - TAM_ATAQUE),
            -TAM_ATAQUE,
            TAM_ATAQUE, TAM_ATAQUE,
        )

        self.tipo = random.choice(["normal", "saltador", "cacador"])
        self.spawn_time = pygame.time.get_ticks()

        if self.tipo == "normal":
            self.sprite = pygame.image.load("sprites/Tronco.png").convert_alpha()

        elif self.tipo == "saltador":
            self.sprite = pygame.image.load("sprites/Slime.png").convert_alpha()

        elif self.tipo == "cacador":
            self.sprite = pygame.image.load("sprites/Raio.png").convert_alpha()

        self.sprite = pygame.transform.scale(
            self.sprite, (self.rect.width, self.rect.height)
        )

        self.vel_y = 2
        self.vel_x = 2
        self.dir = random.choice([-1, 1])
        self.gravidade = 0.5
        self.forca_pulo = -10

    def update(self, jogador):
        velocidade = 2

        if self.tipo == "normal":
            self.rect.y += velocidade

        elif self.tipo == "saltador":
            self.rect.x += self.dir * 4
            self.rect.y += self.vel_y

            self.vel_y += self.gravidade

            if self.rect.bottom >= ALTURA - 20:
                self.rect.bottom = ALTURA - 20
                self.vel_y = self.forca_pulo

            if self.rect.left <= 0 or self.rect.right >= LARGURA:
                self.dir *= -1

        elif self.tipo == "cacador":
            velocidade = 2.5

            if jogador.rect.centerx < self.rect.centerx:
                self.rect.x -= velocidade
            elif jogador.rect.centerx > self.rect.centerx:
                self.rect.x += velocidade

            if jogador.rect.centery < self.rect.centery:
                self.rect.y -= velocidade
            elif jogador.rect.centery > self.rect.centery:
                self.rect.y += velocidade

    def draw(self, tela):
        tela.blit(self.sprite, self.rect)


class Combate:
    def __init__(self):
        self.jogador = Jogador()
        self.boss = Boss()

        self.ataques = []
        self.ultimo_spawn = pygame.time.get_ticks()

        self.cooldown = 3000
        self.ultimo_ataque = -self.cooldown

        self.fonte = pygame.font.Font(None, 36)

    def atualizar(self, tela):
        agora = pygame.time.get_ticks()

        self.jogador.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if agora - self.ultimo_ataque >= self.cooldown:
                self.boss.vida -= 5
                self.ultimo_ataque = agora

        if agora - self.ultimo_spawn >= 5000:
            self.ataques.clear()
            for _ in range(5):
                self.ataques.append(Ataque())
            self.ultimo_spawn = agora

        for a in self.ataques[:]:
            a.update(self.jogador)

            if a.rect.colliderect(self.jogador.rect):
                self.ataques.remove(a)
                self.jogador.vida -= 1

            elif a.rect.top > ALTURA:
                self.ataques.remove(a)

        tela.fill((15, 15, 30))
        self.jogador.draw(tela)
        self.boss.draw(tela)

        for a in self.ataques:
            a.draw(tela)

        self.desenhar_cooldown(tela)

    def desenhar_cooldown(self, tela):
        agora = pygame.time.get_ticks()
        restante = self.cooldown - (agora - self.ultimo_ataque)

        if restante <= 0:
            texto = self.fonte.render("Atacar!", True, (0, 255, 0))
            tela.blit(texto, (350, 520))
        else:
            proporcao = restante / self.cooldown
            pygame.draw.rect(tela, (80, 80, 80), (250, 520, 300, 20))
            pygame.draw.rect(
                tela,
                (0, 200, 0),
                (250, 520, 300 * (1 - proporcao), 20),
            )
