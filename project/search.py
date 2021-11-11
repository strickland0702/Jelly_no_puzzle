import test as env
import pygame

class SearchTree:
    root = None
    node_dict = None
    def __init__(self, root) -> None:
        self.root = root
        self.node_dict = dict()

class TreeNode:
    name = None
    next = None
    def __init__(self, name, next) -> None:
        self.name = name
        self.next = next


grid_world = env.grid_world
input_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
input_event.pos = (3 * 50 + 1, 7 * 50 + 1)
input_event.button = 1
eventloop = []
eventloop.append(input_event)
grid_world = env.run_game(grid_world, eventloop)
env.draw_world(grid_world)