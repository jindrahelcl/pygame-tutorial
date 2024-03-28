import pygame
import json

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {"grass", "stone"}
AUTOTILE_TYPES = {"grass", "stone"}
AUTOTILE_MAP = [ # stored as bitmap: there is something on the top/right/bottom/left.
  1, # nothing
  2, # left
  1, # bottom
  2, # bottom left
  0, # right
  1, # right left
  0, # right bottom
  1, # right bottom left
  8, # top
  4, # top left
  5, # top bottom
  3, # top bottom left
  6, # top right
  8, # top right left
  7, # top right bottom
  5, # top right bottom left
]

class Tilemap:
  def __init__(self, game, tile_size=16):
    self.game = game
    self.tile_size = tile_size
    self.tilemap = {}
    self.offgrid_tiles = []

  def tiles_around(self, pos):
    # conver to grid pos
    tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))

    # only check colisions within reason
    tiles = []
    for offset in NEIGHBOR_OFFSETS:
      check_loc = str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1])
      if check_loc in self.tilemap:
        tiles.append(self.tilemap[check_loc])

    return tiles

  def physics_rects_around(self, pos):
    rects = []
    for tile in self.tiles_around(pos):
      if tile["type"] in PHYSICS_TILES:
        rects.append(
          pygame.Rect(tile["pos"][0] * self.tile_size,
                      tile["pos"][1] * self.tile_size,
                      self.tile_size,
                      self.tile_size))

    return rects

  def render(self, surf, offset=(0, 0)):

    for tile in self.offgrid_tiles:
      surf.blit(self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]))

    # optimization: only render what is visible
    for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
      for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
        loc = str(x) + ";" + str(y)
        if loc in self.tilemap:
          tile = self.tilemap[loc]
          surf.blit(self.game.assets[tile["type"]][tile["variant"]],
                 (tile["pos"][0] * self.tile_size - offset[0],
                  tile["pos"][1] * self.tile_size - offset[1]))  # because tile coords are in grid, not in pixels

  def save(self, path):
    with open(path, "w") as f:
      json.dump({"tilemap": self.tilemap,
                "tile_size": self.tile_size,
                "offgrid": self.offgrid_tiles}, f, indent=2)

  def load(self, path):
    with open(path, "r") as f:
      obj = json.load(f)
      self.tilemap = obj["tilemap"]
      self.tile_size = obj["tile_size"]
      self.offgrid_tiles = obj["offgrid"]

  def autotile(self):
    for loc in self.tilemap:
      tile = self.tilemap[loc]
      if tile["type"] not in AUTOTILE_TYPES:
        continue

      variant = 0
      for i, shift in enumerate([(-1, 0), (0, 1), (1, 0), (0, -1)]):
        check_loc = str(tile["pos"][0] + shift[0]) + ";" + str(tile["pos"][1] + shift[1])
        if check_loc in self.tilemap:
          if self.tilemap[check_loc]["type"] == tile["type"]:
            variant += 2 ** i

      tile["variant"] = AUTOTILE_MAP[variant]
