
from random import randint
import libmineshaft.classes as classes

def generateBlankWorld():
    world = classes.World()
    world_list = list()
    for chunk in range(0, 16):

        world_list.append(list())
        for y in range(0, 128):

            world_list[chunk].append(list())
            for x in range(0, 16):
                world_list[chunk][y].append(0)

    #world = classes.World(world_list)
    return world_list

def generateWorld(biome):
    world = generateBlankWorld()
    for chunk in range(0, 16) :
        for y in range(0, 128):
            for x in range(0, 16):

                if y < 14 :
                    world[chunk][y][x] = 0 #

                elif y > 15 and y < 17:
                    world[chunk][y][x] = 2
                elif  y > 17 and y < 24:
                    world[chunk][y][x] = 1 # dirt
                #elif 127 < y > 24:
                #    world[chunk][y][x] = 3 #stone


    return world












