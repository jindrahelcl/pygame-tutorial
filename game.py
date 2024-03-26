import sys
import pygame

from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds


class Game:
  def __init__(self):
    pygame.init()
    pygame.display.set_caption("Game")

    self.screen = pygame.display.set_mode((640, 480))
    self.display = pygame.Surface((320, 240))
    self.clock = pygame.time.Clock()

    self.img = pygame.image.load("data/images/clouds/cloud_1.png")
    self.img.set_colorkey((0, 0, 0))
    self.img_pos = [160, 260]
    self.movement = [False, False]

    self.assets = {
      "player": load_image("entities/player.png"),
      "decor": load_images("tiles/decor"),
      "grass": load_images("tiles/grass"),
      "large_decor": load_images("tiles/large_decor"),
      "stone": load_images("tiles/stone"),
      "background": load_image("background.png"),
      "clouds": load_images("clouds")
    }

    self.player = PhysicsEntity(self, "player", (50, 50), (8, 15))
    self.tilemap = Tilemap(self, tile_size=16)
    self.clouds = Clouds(self.assets["clouds"], count=16)

    self.scroll = [0, 0]

  def run(self):
    while True:
      self.display.blit(self.assets["background"], (0, 0))


      self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 15
      self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 15
      render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

      self.clouds.update()
      self.clouds.render(self.display, offset=render_scroll)

      self.tilemap.render(self.display, offset=render_scroll)

      self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
      self.player.render(self.display, offset=render_scroll)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            self.movement[0] = True
          if event.key == pygame.K_RIGHT:
            self.movement[1] = True
          if event.key == pygame.K_UP:
            self.player.velocity[1] = -3
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LEFT:
            self.movement[0] = False
          if event.key == pygame.K_RIGHT:
            self.movement[1] = False

      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
      pygame.display.update()
      self.clock.tick(60)

Game().run()