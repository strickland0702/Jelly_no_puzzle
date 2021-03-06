from time import time
import dr_test as env
import pygame
from copy import deepcopy
from wall import Wall
from jelly import Jelly
import time 

class SearchTree:
    root = None
    node_dict = None
    visited = []

    def __init__(self, root) -> None:
        self.root = root
        self.node_dict = dict()

    def cleanvisited(self):
        self.visited = []

    def dfs_expand_node(self, node, goal_state, path):
        if node.grid_world == goal_state:
            new_path = path.copy()
            new_path.append(node.grid_world)
            return True, new_path
        
        if repr(node.grid_world) not in self.visited:
            self.visited.append(repr(node.grid_world))
            
        for next_node in node.next:
            if next_node not in self.visited:
                new_path = path.copy()
                new_path.append(self.node_dict[next_node].grid_world)
                result,re_path = self.dfs_expand_node(self.node_dict[next_node], goal_state, new_path)
                if result == True:
                    return True, re_path
        return False, 0

class TreeNode:
    grid_world = None
    next = None
    jelly_list = None
    def __init__(self, grid_world, jelly_list) -> None:
        self.next = []
        self.grid_world = grid_world
        self.jelly_list = jelly_list

def expand_node(node:TreeNode, tree:SearchTree, next_expand_list = []):
    # expand node, add repr(next_node) to node.next, add repr(node):node to tree.node_dict
    for jelly in node.jelly_list:
        for action in [1,3]:
            input_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
            y_axis, x_axis, _ = jelly[0]
            input_event.pos = (x_axis * grid_size + 1, y_axis * grid_size + 1)
            input_event.button = action
            eventloop = [input_event]
            grid_world,jelly_list = env.run_game(deepcopy(node.grid_world), eventloop)
            if repr(grid_world) not in tree.node_dict:
                next_node = TreeNode(grid_world, jelly_list)
                tree.node_dict[repr(grid_world)] = next_node
                if repr(grid_world) not in next_expand_list:
                    next_expand_list.append(repr(grid_world))
            if repr(grid_world) not in node.next:
                node.next.append(repr(grid_world))
    return next_expand_list


def draw_world(sequence_result):
    pygame.init()
    screen_width = 700 # x-axis
    screen_height = 500 # y-axis
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Jelly No Puzzle')
    grid_size = 50
    
    for grid_world in sequence_result:
        screen.fill((0, 0, 0))

        for i in range(10):
            for j in range(14):
                if grid_world[i][j] == "w":
                    wall = Wall(j, i, 1, 1, grid_size)
                    pygame.draw.rect(screen, wall.color, wall)
                elif grid_world[i][j] == "r":
                    jelly = Jelly(j ,i, 1, 1, grid_size, color=(255, 0, 0))
                    pygame.draw.rect(screen, jelly.color, jelly)
                elif grid_world[i][j] == "g":
                    jelly = Jelly(j ,i, 1, 1, grid_size, color=(0, 255, 0))
                    pygame.draw.rect(screen, jelly.color, jelly)
                elif grid_world[i][j] == "b":
                    jelly = Jelly(j ,i, 1, 1, grid_size, color=(0, 0, 255))
                    pygame.draw.rect(screen, jelly.color, jelly)
                else:
                    pass

        pygame.display.update()
        time.sleep(0.5)


grid_world = env.grid_world
grid_size = env.grid_size

jelly_list = []
for i in range(10):
    for j in range(14):
        if grid_world[i][j] == "r" or grid_world[i][j] == "g" or grid_world[i][j] == "b":
            jelly_list.append([(i, j, grid_world[i][j])])

root = TreeNode(deepcopy(grid_world), deepcopy(jelly_list))
tree = SearchTree(root)
tree.node_dict[repr(root.grid_world)] = root
next_expand_list = expand_node(root, tree)
while len(next_expand_list) != 0:
    next_expand_list = expand_node(tree.node_dict[next_expand_list[0]],tree,next_expand_list)
    next_expand_list.remove(next_expand_list[0])

print('build finished')

for i in tree.node_dict.values():
    if env.detect_winning(i.grid_world, len(env.color_set)):
        goal_state = i.grid_world

_, result = tree.dfs_expand_node(tree.root, goal_state, [])

draw_world(result)