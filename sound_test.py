import pygame

if __name__ == '__main__':
  try:
    pygame.mixer.init()
    pygame.mixer.music.load("sound_test.mp3")
    pygame.mixer.music.play()
    #while pygame.mixer.music.get_busy() == True:
      #continue
  except KeyboardInterrupt:
    pass
