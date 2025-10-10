import pygame
class Carro:
  def som_carro():
    pygame.mixer.music.load('sounds/SOM DE CARRO PASSANDO(MP3_160K).mp3')
    pygame.mixer.music.set_volume(5)
    pygame.mixer.music.play(1)

class Porta:
  def som_porta():
    pygame.mixer.music.load('sounds/SOM DE PORTA ABRINDO(MP3_160K).mp3')
    pygame.mixer.music.set_volume(5)
    pygame.mixer.music.play(1)

class Tema:
  def som_tema():
    pygame.mixer.music.load('sounds\Day (Alt) - No_ I_m Not a Human OST(MP3_160K).mp3')
    pygame.mixer.music.set_volume(3)
    pygame.mixer.music.play(-1)