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

                oleft = x - 1 >= 0
                oright = x + 1 < self.width
                oup = y - 1 >= 0
                odown = y + 1 < self.height

                if oleft:
                    left = (x - 1, y)

                    if self.tiles[left[1]][left[0]].t == 1:
                        self.adj_tiles[tile].append(left)
                if oright:
                    right = (x + 1, y)

                    if self.tiles[right[1]][right[0]].t == 1:
                        self.adj_tiles[tile].append(right)
                if oup:
                    up = (x, y - 1)

                    if self.tiles[up[1]][up[0]].t == 1:
                        self.adj_tiles[tile].append(up)
                if odown:
                    down = (x, y + 1)

                    if self.tiles[down[1]][down[0]].t == 1:
                        self.adj_tiles[tile].append(down)
                if oleft and oup:
                    upleft = (x - 1, y - 1)

                    if self.tiles[upleft[1]][upleft[0]].t == 1:
                        self.adj_tiles[tile].append(upleft)
                if oright and oup:
                    upright = (x + 1, y - 1)

                    if self.tiles[upright[1]][upright[0]].t == 1:
                        self.adj_tiles[tile].append(upright)
                if oleft and odown:
                    downleft = (x - 1, y + 1)

                    if self.tiles[downleft[1]][downleft[0]].t == 1:
                        self.adj_tiles[tile].append(downleft)
                if oright and odown:
                    downright = (x + 1, y + 1)

                    if self.tiles[downright[1]][downright[0]].t == 1:
                        self.adj_tiles[tile].append(downright)
                    

    def coord_to_tile(self, x, y):
        from math import floor
        return (floor(x / self.tile_size), floor(y / self.tile_size))
