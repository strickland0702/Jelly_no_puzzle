import pygame
from copy import deepcopy
from jelly import Jelly
from wall import Wall


# redSquare = pygame.image.load("wechat.jpg")

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



# Function Components

def color_convert(color_str):
    if color_str == "r":
        color = (255, 0 , 0)
    elif color_str == "g":
        color = (0, 255, 0)
    elif color_str == "b":
        color = (0, 0, 255)

def check_left_wall_collision(grid_world, jelly_item):
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
            if jelly_tuple[0] < frontier[jelly_tuple[1]][0]:
                frontier[jelly_tuple[1]] = jelly_tuple
    
    for jelly_tuple in frontier.values():
        i = jelly_tuple[0]
        j = jelly_tuple[1]

        if grid_world[i+1][j] != "a":
            return False

    return True

def find_merge_jelly(color_jelly_list):
    possible_merge_tuple = []

    # print("color_jelly_list: ", color_jelly_list)
    for jelly_item in color_jelly_list:
        # print("jelly_item: ", jelly_item)

        for jelly_tuple in jelly_item:
            i = jelly_tuple[0]
            j = jelly_tuple[1]
            color = jelly_tuple[2]

            possible_merge_tuple.append((i, j-1, color))
            possible_merge_tuple.append((i, j+1, color))
            possible_merge_tuple.append((i-1, j, color))
            possible_merge_tuple.append((i+1, j, color))

    # print("possible: ", possible_merge_tuple)
    # print("color_jelly_list: ", color_jelly_list)
    merge_list = []
        
    for jelly_item in color_jelly_list:
        for jelly_tuple in jelly_item:
            if jelly_tuple in possible_merge_tuple:
                if jelly_item not in merge_list:
                    merge_list.append(jelly_item)

    append_item = []       
    for item in merge_list:
        append_item = append_item + item

    # print("merge list:", merge_list)
    # print("append item:", append_item)

    return merge_list, append_item

def adjust_merge_jelly(jelly_list, merge_list, append_item):
    if merge_list and append_item:
        for jelly_item in merge_list:
            jelly_list.remove(jelly_item)
            
        if append_item not in jelly_list:
            jelly_list.append(append_item)

def merge(jelly_list):
    # check whether jellies will merge

    red_jelly_list = []
    green_jelly_list = []
    blue_jelly_list = []

    for jelly_item in jelly_list:

        color = jelly_item[0][2]

        if color == "r":
            red_jelly_list.append(jelly_item)
        elif color == "g":
            green_jelly_list.append(jelly_item)
        elif color == "b":
            blue_jelly_list.append(jelly_item)

    red_merge_list, red_append_item = find_merge_jelly(red_jelly_list)
    green_merge_list, green_append_item = find_merge_jelly(green_jelly_list)
    blue_merge_list, blue_append_item = find_merge_jelly(blue_jelly_list)

    adjust_merge_jelly(jelly_list, red_merge_list, red_append_item)
    adjust_merge_jelly(jelly_list, green_merge_list, green_append_item)
    adjust_merge_jelly(jelly_list, blue_merge_list, blue_append_item)

    # print(jelly_list)
    
def jelly_fall(grid_world, jelly_list):

    for jelly_item in jelly_list:

        if check_fall(grid_world, jelly_item):

            while check_fall(grid_world, jelly_item):          
                new_jelly_item = jelly_item_move_down(grid_world, jelly_item, jelly_list)
                jelly_item = new_jelly_item

            for jelly_item in jelly_list:
                jelly_fall(grid_world, jelly_list)

def draw_world(grid_world):
    pygame.init()
    screen_width = 700 # x-axis
    screen_height = 500 # y-axis
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Jelly No Puzzle')
    grid_size = 50
    
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
    import time
    time.sleep(3)
    pygame.quit()

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
        grid_world[i][j] = color

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

def detect_winning(jelly_list):
    for jelly_item in jelly_list:
        if len(jelly_item) < 2:
            return False

    return True

def run_game(grid_world, eventloop, jelly_list = []):
    if jelly_list == []:
        for i in range(10):
            for j in range(14):
                if grid_world[i][j] == "r" or grid_world[i][j] == "g" or grid_world[i][j] == "b":
                    jelly_list.append([(i, j, grid_world[i][j])])

    # print(jelly_list)
    grid_size = 50

    for event in eventloop:
        if event.type == pygame.QUIT:
            break

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            for jelly_item in jelly_list:

                for jelly_tuple in jelly_item:

                    i = jelly_tuple[0]
                    j = jelly_tuple[1]
                    color = jelly_tuple[2]
                        
                    jelly = Jelly(j, i, 1, 1, grid_size, color_convert(color))
                    if jelly.collidepoint(mouse_x, mouse_y):

                        if event.button == 1: # left click 
                            if not check_left_wall_collision(grid_world, jelly_item): 
                                
                                jelly_item_move_left(grid_world, jelly_item, jelly_list)
                                jelly_fall(grid_world, jelly_list)
                                merge(jelly_list)

                                # print("jelly_list: ", jelly_list)

                        elif event.button == 3: # right click

                            if not check_right_wall_collision(grid_world, jelly_item): 
                                
                                jelly_item_move_right(grid_world, jelly_item, jelly_list)
                                jelly_fall(grid_world, jelly_list)
                                merge(jelly_list)
                                # print("jelly_list: ", jelly_list)


    return grid_world, jelly_list

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
grid_size = 50

if __name__ == '__main__':
    input_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
    input_event.pos = (3 * 50 + 1, 7 * 50 + 1)
    input_event.button = 1
    eventloop = []
    eventloop.append(input_event)
    grid_world, jelly_list = run_game(grid_world, eventloop)
    draw_world(grid_world)