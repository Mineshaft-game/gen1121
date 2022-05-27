"""
Copyright (C) 2021-2022  Alexey "LEHAtupointow" Pavlov
Copyright (C) 2021  Sakurai Mayu
Copyright (C) 2021  Nobody6502

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
    USA
"""


from libmineshaft.world import *
import json
import pygame
from pynbt import *
import gzip
import os

__version__ = "unknown"
__author__ = "LEHAtupointow, Sakurai Mayu and Nobody6502"
__description__ = "The default world generation engine for the 2D Pygame game Mineshaft."



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


def generateBlankWorld(name: str = "World", gamemode: int = 0,  saves_dir=os.path.join(".mineshaft",  "saves")):
    os.makedirs(os.path.join(saves_dir, name))
    nbt_contents = dict()
    for x in range(-128, 128):
        for y in range(-64, 64):
            value = {
                "block_type": TAG_Int(0), 
                "block_data":TAG_Int(0), 
            }
            nbt_contents[f"{x},{y}"] = TAG_Compound(value=value)
    nbt = NBTFile(value=nbt_contents)
    with open(os.path.join(saves_dir,  name,  "chunks.dat.tempsave.ungzipped"),  "wb") as io:
        nbt.save(io)
    with open(os.path.join(saves_dir,  name,  "chunks.dat.tempsave.ungzipped"),  "rb") as ungzipped,  gzip.open(os.path.join(saves_dir,  name,  "chunks.dat"),  "wb") as gzip_out:
        gzip_out.writelines(ungzipped)
    world = World(name=name, gamemode=gamemode,  saves_dir=saves_dir)
    return world

def generateSuperflatWorld(name: str = "Superflat World",  gamemode: int = 0,  saves_dir=os.path.join(".mineshaft",  "saves")):
    world = generateBlankWorld()
    for y in range(-64, 64):
        for x in range(-128, 128):
            if y <= 14:
                world.world[f"{x},{y}"] = TAG_Compound(value={
                "block_type": TAG_Int(0), 
                "block_data":TAG_Int(0), 
            })
            elif y >= 15 and y <= 17:
               world.world[f"{x},{y}"] = TAG_Compound(value={
                "block_type": TAG_Int(7), 
                "block_data":TAG_Int(0), 
            })
            elif y > 17:
                world.world[f"{x},{y}"] = TAG_Compound(value={
                "block_type": TAG_Int(1), 
                "block_data":TAG_Int(0), 
            })
    world.save()
    return world

if __name__ == "__main__":
    generateSuperflatWorld(name="World")
