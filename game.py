import sys
import pygame

pygame.init()

pygame.display.caption("Game")
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

while True:

  for event in pygame.events.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  pygame.display.update()
  clock.tick()
