import sys
import pygame.freetype
import random
import Pacman
import Food
import Monster
import Map
from Specification import *
import BFS

current_level = 1
current_map_index = 0
def level_1():
        """
        Level 1: Pac-man know the food’s position in map and monsters do not appear in map.
        There is only one food in the map.
        """
        graph_map, pacman_pos, monster_pos = Map.read_map_level_1_monster(
            MAP_INPUT_TXT[current_level - 1][current_map_index])
        
        print("Graph map:", graph_map)
        print("\npacman_pos: ", pacman_pos)
        print("\nmonster_pos: ", monster_pos)
        path = BFS.bfs(graph_map , monster_pos, pacman_pos)


        print("\nPath from Pacman to food:", path)

level_1()
