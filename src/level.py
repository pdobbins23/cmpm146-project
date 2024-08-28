import json
import LdtkJson

class Level:
    def __init__(self, level_file, tile_size=16):
        self.tile_size = tile_size

        with open(level_file, "r") as file:
            level_data = file.read()
        ldtk_level = LdtkJson.ldtk_json_from_dict(json.loads(level_data))

        lvl = ldtk_level.levels[0]
        layer = lvl.layer_instances[0]

        self.width = layer.c_wid
        self.height = layer.c_hei

        print("Loaded level with", len(lvl.layer_instances), "layers, layer[0] is", layer.c_wid, "x", layer.c_hei, "and has", len(layer.grid_tiles), "tiles")

        self.tiles = [[layer.grid_tiles[y * self.width + x] for x in range(0, self.width)] for y in range(0, self.height)]

        self.adj_tiles = {}

        for y in range(0, self.height):
            for x in range(0, self.width):
                tile = (x, y)

                self.adj_tiles[tile] = []

                if x - 1 >= 0:
                    left = (x - 1, y)

                    if self.tiles[left[1]][left[0]].t == 1:
                        self.adj_tiles[tile].append(left)
                if x + 1 < self.width:
                    right = (x + 1, y)

                    if self.tiles[right[1]][right[0]].t == 1:
                        self.adj_tiles[tile].append(right)
                if y - 1 >= 0:
                    up = (x, y - 1)

                    if self.tiles[up[1]][up[0]].t == 1:
                        self.adj_tiles[tile].append(up)
                if y + 1 < self.height:
                    down = (x, y + 1)

                    if self.tiles[down[1]][down[0]].t == 1:
                        self.adj_tiles[tile].append(down)

    def coord_to_tile(self, x, y):
        from math import floor
        return (floor(x / self.tile_size), floor(y / self.tile_size))
