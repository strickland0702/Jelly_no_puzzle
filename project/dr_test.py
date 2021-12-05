import copy
import pygame
from copy import deepcopy
from jelly import Jelly
from wall import Wall

# Function Components

def color_convert(color_str):
    if color_str == "r":
        color = (255, 0 , 0)
    elif color_str == "g":
        color = (0, 255, 0)
    elif color_str == "b":
        color = (0, 0, 255)

def check_left_wall_collision(grid_world, jelly_item, jelly_list):
    frontier = {}
    for jelly_tuple in jelly_item:
        if jelly_tuple[0] not in frontier.keys():
            frontier[jelly_tuple[0]] = jelly_tuple
        else:
            if jelly_tuple[1] < frontier[jelly_tuple[0]][1]:
                frontier[jelly_tuple[0]] = jelly_tuple
    
    # print(frontier)

    for jelly_tuple in frontier.values():
        i = jelly_tuple[0]
        j = jelly_tuple[1]

        if grid_world[i][j-1] != "a":
            return True

        # if grid_world[i][j-1] == "w":
        #     return True
        
        # if grid_world[i][j-1] == "r" or grid_world[i][j-1] == "g" or grid_world[i][j-1] == "b":
        #     for jelly_item in jelly_list:
        #         if (i, j-1, grid_world[i][j-1]) in jelly_item:
        #             if check_left_wall_collision(grid_world, jelly_item, jelly_list):
        #                 return True

    return False

def check_right_wall_collision(grid_world, jelly_item):
    frontier = {}
    for jelly_tuple in jelly_item:
        if jelly_tuple[0] not in frontier.keys():
            frontier[jelly_tuple[0]] = jelly_tuple
        else:
            if jelly_tuple[1] > frontier[jelly_tuple[0]][1]:
                frontier[jelly_tuple[0]] = jelly_tuple
    
    # print(frontier)

    for jelly_tuple in frontier.values():
        i = jelly_tuple[0]
        j = jelly_tuple[1]

        if grid_world[i][j+1] != "a":
            return True
        
    return False

def check_fall(grid_world, jelly_item):
    frontier = {}
    for jelly_tuple in jelly_item:
        if jelly_tuple[1] not in frontier.keys():
            frontier[jelly_tuple[1]] = jelly_tuple
        else:
            if jelly_tuple[0] > frontier[jelly_tuple[1]][0]:
                frontier[jelly_tuple[1]] = jelly_tuple
    
    for jelly_tuple in frontier.values():
        i = jelly_tuple[0]
        j = jelly_tuple[1]

        if grid_world[i+1][j] != "a":
            return False

    return True

def jelly_fall(grid_world, jelly_list):

    for jelly_item in jelly_list:

        if check_fall(grid_world, jelly_item):

            while check_fall(grid_world, jelly_item):          
                new_jelly_item = jelly_item_move_down(grid_world, jelly_item, jelly_list)
                jelly_item = new_jelly_item

            for jelly_item in jelly_list:
                jelly_fall(grid_world, jelly_list)

def jelly_item_move_left(grid_world, jelly_item, jelly_list):

    
    new_jelly_item = []
    for jelly_tuple in jelly_item:
        i = jelly_tuple[0]
        j = jelly_tuple[1]
        color = jelly_tuple[2]
        new_jelly_item.append((i, j-1, color))
        grid_world[i][j] = "a"

    for jelly_tuple in new_jelly_item:
        i = jelly_tuple[0]
        j = jelly_tuple[1]
        color = jelly_tuple[2]

        # if grid_world[i][j] == "a":
        grid_world[i][j] = color

        # elif grid_world[i][j] == "r" or grid_world[i][j] == "g" or grid_world[i][j] == "b":
        #     print("collide")
        #     for jelly_item in jelly_list:
        #         if (i, j, grid_world[i][j]) in jelly_item:
        #             jelly_item_move_left(grid_world, jelly_item, jelly_list)

    jelly_list.remove(jelly_item)
    jelly_list.append(new_jelly_item)

def jelly_item_move_right(grid_world, jelly_item, jelly_list):

    new_jelly_item = []
    for jelly_tuple in jelly_item:
        i = jelly_tuple[0]
        j = jelly_tuple[1]
        color = jelly_tuple[2]
        new_jelly_item.append((i, j+1, color))
        grid_world[i][j] = "a"
        
    for jelly_tuple in new_jelly_item:
        i = jelly_tuple[0]
        j = jelly_tuple[1]
        color = jelly_tuple[2]
        grid_world[i][j] = color

    jelly_list.remove(jelly_item)
    jelly_list.append(new_jelly_item)

def jelly_item_move_down(grid_world, jelly_item, jelly_list):
    new_jelly_item = []
    for jelly_tuple in jelly_item:
        i = jelly_tuple[0]
        j = jelly_tuple[1]
        color = jelly_tuple[2]
        new_jelly_item.append((i+1, j, color))
        grid_world[i][j] = "a"
        
    for jelly_tuple in new_jelly_item:
        i = jelly_tuple[0]
        j = jelly_tuple[1]
        color = jelly_tuple[2]
        grid_world[i][j] = color

    jelly_list.remove(jelly_item)
    jelly_list.append(new_jelly_item)

    return new_jelly_item

def check_surround_jellies(grid_world, i, j, full_jelly_item):
    color_str = grid_world[i][j]
    
    if grid_world[i+1][j] == color_str:
        if (i+1, j, color_str) not in full_jelly_item:
            full_jelly_item.append((i+1, j, color_str))
            check_surround_jellies(grid_world, i+1, j, full_jelly_item)
    if grid_world[i-1][j] == color_str:
        if (i-1, j, color_str) not in full_jelly_item:
            full_jelly_item.append((i-1, j, color_str))
            check_surround_jellies(grid_world, i-1, j, full_jelly_item)
    if grid_world[i][j+1] == color_str:
        if (i, j+1, color_str) not in full_jelly_item:
            full_jelly_item.append((i, j+1, color_str))
            check_surround_jellies(grid_world, i, j+1, full_jelly_item)
    if grid_world[i][j-1] == color_str:
        if (i, j-1, color_str) not in full_jelly_item:
            full_jelly_item.append((i, j-1, color_str))
            check_surround_jellies(grid_world, i, j-1, full_jelly_item)
            
    return full_jelly_item 

def get_jelly_list(grid_world):
    
    jelly_list = []
    visited = []
    for i in range(10):
        for j in range(14):
            
            if grid_world[i][j] in ["r", "g", "b"]:
                if (i, j, grid_world[i][j]) not in visited:
                    full_jelly_item = [(i, j, grid_world[i][j])]                
                    full_jelly_item = check_surround_jellies(grid_world, i, j, full_jelly_item)
                    jelly_list.append(full_jelly_item)
                              
                    for jelly_tuple in full_jelly_item:
                        visited.append(jelly_tuple)
                
    return jelly_list

def detect_winning(grid_world, num_of_color):
    jelly_list = get_jelly_list(grid_world)
    if len(jelly_list) == num_of_color:
        return True

    return False

def draw_world(grid_world, screen):
    
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

# def draw_world(grid_world):
#     pygame.init()
#     screen_width = 700 # x-axis
#     screen_height = 500 # y-axis
#     screen = pygame.display.set_mode((screen_width, screen_height))
#     pygame.display.set_caption('Jelly No Puzzle')
#     grid_size = 50
    
#     screen.fill((0, 0, 0))

#     for i in range(10):
#         for j in range(14):
#             if grid_world[i][j] == "w":
#                 wall = Wall(j, i, 1, 1, grid_size)
#                 pygame.draw.rect(screen, wall.color, wall)
#             elif grid_world[i][j] == "r":
#                 jelly = Jelly(j ,i, 1, 1, grid_size, color=(255, 0, 0))
#                 pygame.draw.rect(screen, jelly.color, jelly)
#             elif grid_world[i][j] == "g":
#                 jelly = Jelly(j ,i, 1, 1, grid_size, color=(0, 255, 0))
#                 pygame.draw.rect(screen, jelly.color, jelly)
#             elif grid_world[i][j] == "b":
#                 jelly = Jelly(j ,i, 1, 1, grid_size, color=(0, 0, 255))
#                 pygame.draw.rect(screen, jelly.color, jelly)
#             else:
#                 pass

#     pygame.display.update()
#     import time
#     time.sleep(3)
#     pygame.quit()

def run_game(grid_world, eventloop):

    grid_size = 50

    jelly_list = get_jelly_list(grid_world)

    for event in eventloop:
        if event.type == pygame.QUIT:
            break

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos

            jelly_list = get_jelly_list(grid_world)

            fixed_jelly_list = copy.deepcopy(jelly_list)

            for jelly_item in fixed_jelly_list:

                for jelly_tuple in jelly_item:

                    i = jelly_tuple[0]
                    j = jelly_tuple[1]
                    color = jelly_tuple[2]
                        
                    jelly = Jelly(j, i, 1, 1, grid_size, color_convert(color))
                    if jelly.collidepoint(mouse_x, mouse_y):

                        if event.button == 1: # left click 
                            if not check_left_wall_collision(grid_world, jelly_item, jelly_list): 
                                jelly_item_move_left(grid_world, jelly_item, jelly_list)
                                jelly_fall(grid_world, jelly_list)
                                # jelly_list = get_jelly_list(grid_world)
                                # print("jelly_list: ", jelly_list)

                        elif event.button == 3: # right click
                            if not check_right_wall_collision(grid_world, jelly_item): 
                                
                                jelly_item_move_right(grid_world, jelly_item, jelly_list)
                                jelly_fall(grid_world, jelly_list)
                                # jelly_list = get_jelly_list(grid_world)
                                # print("jelly_list: ", jelly_list)

    return grid_world, jelly_list

# pygame.init()
# screen_width = 700 # x-axis
# screen_height = 500 # y-axis
# grid_size = 50
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption('Jelly No Puzzle')

# Level - 01
grid_world = [["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w"],
            ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
            ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
            ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
            ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
            ["w", "a", "a", "a", "a", "a", "a", "a", "r", "a", "a", "a", "a", "w"],
            ["w", "a", "a", "a", "a", "a", "a", "w", "w", "a", "a", "a", "a", "w"],
            ["w", "a", "a", "g", "a", "a", "a", "a", "a", "r", "a", "b", "a", "w"],
            ["w", "w", "b", "w", "w", "w", "g", "a", "w", "w", "w", "w", "w", "w"],
            ["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w"]]


# Level - 02
# grid_world = [["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "a", "a", "a", "a", "a", "g", "a", "a", "a", "g", "a", "a", "w"],
#               ["w", "a", "a", "a", "r", "a", "r", "a", "a", "a", "r", "a", "a", "w"],
#               ["w", "w", "w", "w", "w", "a", "w", "a", "w", "a", "w", "w", "w", "w"],
#               ["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w"]]

# Level - 03 (Fail)
# grid_world = [["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "a", "a", "a", "b", "g", "a", "a", "w", "a", "g", "a", "a", "w"],
#               ["w", "w", "w", "a", "w", "w", "w", "r", "w", "w", "w", "a", "a", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "b", "a", "a", "a", "a", "a", "w"],
#               ["w", "w", "w", "a", "w", "w", "w", "r", "w", "w", "w", "w", "w", "w"],
#               ["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w"]]

# Level - 04
# grid_world = [["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "r", "a", "a", "a", "a", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "b", "a", "a", "a", "a", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "w", "a", "a", "a", "a", "w"],
#               ["w", "a", "b", "a", "r", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "a", "b", "a", "r", "a", "a", "a", "a", "a", "a", "b", "a", "w"],
#               ["w", "w", "w", "a", "w", "a", "a", "a", "a", "a", "a", "w", "w", "w"],
#               ["w", "w", "w", "w", "w", "a", "w", "w", "w", "w", "w", "w", "w", "w"],
#               ["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w"]]

# Level - 05
# grid_world = [["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "r", "g", "a", "a", "g", "g", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "w", "w", "a", "w", "w", "w", "w", "a", "w", "w", "a", "a", "w"],
#               ["w", "r", "g", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "w"],
#               ["w", "w", "w", "w", "w", "a", "a", "w", "w", "a", "a", "a", "w", "w"],
#               ["w", "w", "w", "w", "w", "w", "a", "w", "w", "a", "a", "w", "w", "w"],
#               ["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w"]]

grid_size = 50
color_set = set()

# jelly_list = []
for i in range(10):
    for j in range(14):
        if grid_world[i][j] == "r" or grid_world[i][j] == "g" or grid_world[i][j] == "b":
            # jelly_list.append([(i, j, grid_world[i][j])])
            color_set.add(grid_world[i][j])

# print(jelly_list)

# running = True
# while (running):

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#         elif event.type == pygame.MOUSEBUTTONDOWN:

#             mouse_x, mouse_y = event.pos

#             jelly_list = get_jelly_list(grid_world)

#             fixed_jelly_list = copy.deepcopy(jelly_list)

#             for jelly_item in fixed_jelly_list:

#                 for jelly_tuple in jelly_item:

#                     i = jelly_tuple[0]
#                     j = jelly_tuple[1]
#                     color = jelly_tuple[2]
                        
#                     jelly = Jelly(j, i, 1, 1, grid_size, color_convert(color))
#                     if jelly.collidepoint(mouse_x, mouse_y):

#                         if event.button == 1: # left click 
#                             if not check_left_wall_collision(grid_world, jelly_item, jelly_list): 
#                                 jelly_item_move_left(grid_world, jelly_item, jelly_list)
#                                 jelly_fall(grid_world, jelly_list)
#                                 jelly_list = get_jelly_list(grid_world)
#                                 print("jelly_list: ", jelly_list)

#                         elif event.button == 3: # right click
#                             if not check_right_wall_collision(grid_world, jelly_item): 
                                
#                                 jelly_item_move_right(grid_world, jelly_item, jelly_list)
#                                 jelly_fall(grid_world, jelly_list)
#                                 jelly_list = get_jelly_list(grid_world)
#                                 print("jelly_list: ", jelly_list)

    
#             if detect_winning(grid_world, len(color_set)):
#                 print("YOU WIN!")

#     draw_world(grid_world, screen)

# pygame.quit()

if __name__ == '__main__':
    input_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
    input_event.pos = (6 * 50 + 1, 4 * 50 + 1)
    input_event.button = 3
    eventloop = [input_event]
    # eventloop.append(input_event)
    grid_world, jelly_list = run_game(grid_world, eventloop)
    print(jelly_list)
    # draw_world(grid_world, screen)