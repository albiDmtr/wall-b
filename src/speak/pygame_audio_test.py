import pygame

pygame.mixer.init()
pygame.mixer.music.load('/home/wallb/Desktop/wall-b/src/speak/sample-6s.mp3')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
	pygame.time.Clock().tick(10)