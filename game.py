import sys
import pygame

class Game:
  def __init__(self):
    pygame.init()
    pygame.display.set_caption("Game")

    self.screen = pygame.display.set_mode((640, 480))
    self.clock = pygame.time.Clock()


    self.img = pygame.image.load("data/images/clouds/cloud_1.png")
    self.img.set_colorkey((0, 0, 0))
    self.img_pos = [160, 260]
    self.movement = [False, False]

    self.collision_area = pygame.Rect(50, 50, 300, 50)


  def run(self):
    while True:
      self.screen.fill((0, 128, 255))
      self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5

      img_r = pygame.Rect(*self.img_pos, *self.img.get_size())
      if img_r.colliderect(self.collision_area):
        pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
      else:
        pygame.draw.rect(self.screen, (0, 100, 128), self.collision_area)

      self.screen.blit(self.img, self.img_pos)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP:
            self.movement[0] = True
          if event.key == pygame.K_DOWN:
            self.movement[1] = True
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_UP:
            self.movement[0] = False
          if event.key == pygame.K_DOWN:
            self.movement[1] = False

      pygame.display.update()
      self.clock.tick(60)

Game().run()