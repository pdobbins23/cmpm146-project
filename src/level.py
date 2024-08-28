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

    def coord_to_tile(self, x, y):
        from math import floor
        return (floor(x / self.tile_size), floor(y / self.tile_size))
