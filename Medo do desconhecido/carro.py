import pygame
class Carro:
  def som_carro():
    pygame.mixer.music.load('sounds/SOM DE CARRO PASSANDO(MP3_160K).mp3')
    pygame.mixer.music.set_volume(5)
    pygame.mixer.music.play(1)