import pygame

class Dialogo:
    def __init__(self, linhas, delay=500):
        self.linhas = linhas
        self.indice = 0
        self.ativo = False
        self.fonte = pygame.font.Font(None, 36)
        self.delay = delay
        self.ultimo_avanco = 0

    def iniciar(self):
        self.ativo = True
        self.indice = 0
        self.ultimo_avanco = pygame.time.get_ticks()

    def avancar(self):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_avanco >= self.delay:
            if self.indice < len(self.linhas) - 1:
                self.indice += 1
                self.ultimo_avanco = tempo_atual
            else:
                self.ativo = False

    def desenhar(self, tela, largura, altura):
        if self.ativo:
            texto = self.fonte.render(self.linhas[self.indice], True, (255, 255, 255))
            texto_rect = texto.get_rect(center=(largura // 2, altura // 2))
            
            fundo_texto = pygame.Surface((texto.get_width() + 40, texto.get_height() + 20), pygame.SRCALPHA)
            pygame.draw.rect(fundo_texto, (0, 0, 0), 
                             (0, 0, texto.get_width() + 40, texto.get_height() + 20), 
                             border_radius=10)
            tela.blit(fundo_texto, (texto_rect.x - 20, texto_rect.y - 10))
            tela.blit(texto, texto_rect)
            
            instr = self.fonte.render("Pressione T para continuar", True, (255, 255, 255))
            instr_rect = instr.get_rect(center=(largura // 2, altura // 2 + 60))
            tela.blit(instr, instr_rect)