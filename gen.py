from random import randint
import libmineshaft.world as world
import sys
import json


def loadWorldFile(path):
    # This function is simple, it loads the file based on a path variable and then splits different attributes from the json up into seprate variables
    # While i've tried to make changes as versatile as they can be, unfortunately I cannot prepare for every needed function, so the json stores very simple info, just enough to render a small map.
    # hopefully it can be built apon by storing an array of chunks in [map] sometime in the future but that is outside the scope currently
    levelFile = json.load(open(path, "r"))
    level = levelFile["map"]
    playerPos = levelFile["player"]
    tileSize = levelFile["tilesize"]
    return level, playerPos, tileSize


def loadWorldFromMap():
    tile_rects = []
    y = 0
    for row in level:
        x = 0
        for tile in row:
            # For each tile you're checking for you can add an if statement checking for the tile's name
            # if the name is found you would then blit the image for that tile at the location of your tile. (i.e x * tileSize, y * tileSize.)
            # Note: If you want a scrolling map, you would also subtract a scroll value from this position to get the actual location
            # Also, this is a lazy renderer in that it doesnt check for tiles off screen so with larger worlds you *will* run into performance issues.
            # One way to prevent that would be to chunkify the worlds as appears to be happening in generateWorld()
            # Lastly it should be noted that checking every block in a seprate if statement every frame will get performance intensive once your block list gets long
            # A good way to optimize would be to use structural pattern matching, but that's not implemented currently as the project doesnt seem to be targetting python 3.10
            if tile != "0":
                # This appends a pygame rect t the tile_rects list, this can then be tested against every frame to detect collisions.
                tile_rects.append(
                    pygame.Rect(x * tileSize, y * tileSize, tileSize, tileSize)
                )
            x += 1
        y += 1


def generateBlankWorld():
    world = world.World()
    world_list = list()
    for chunk in range(0, 16):

        world_list.append(list())
        for y in range(0, 128):

            world_list[chunk].append(list())
            for x in range(0, 16):
                world_list[chunk][y].append(0)
    return world_list


def generateWorld(biome):
    world = generateBlankWorld()
    for chunk in range(0, 16):
        for y in range(0, 128):
            for x in range(0, 16):
                if y < 14:
                    world[chunk][y][x] = 0
                elif y > 15 and y < 17:
                    world[chunk][y][x] = 2
                elif y > 17 and y < 24:
                    world[chunk][y][x] = 1
    return world
