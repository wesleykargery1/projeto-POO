import pygame
class Carro:
  def som_carro():
    carro = pygame.mixer.Sound('sounds/SOM DE CARRO PASSANDO(MP3_160K).mp3')
    carro.set_volume(1.0)
    carro.play()


class Porta:
  def som_porta():
    porta = pygame.mixer.Sound('sounds\porta.mp3')
    porta.set_volume(1.0)
    porta.play()

class Tema:
    def __init__(self):

        pygame.mixer.music.load("sounds/Day (Alt) - No_ I_m Not a Human OST(MP3_160K).mp3")
        pygame.mixer.music.set_volume(0.4)
    def som_tema(self):
        
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)