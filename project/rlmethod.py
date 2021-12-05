import dr_test as env
import pygame
import copy
import time
from wall import Wall
from jelly import Jelly
from dr_test import get_jelly_list

# implementation of Breadth-First-Search
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

def expand(grid_world):

    jelly_list = env.get_jelly_list(grid_world)
    child_state_list = []

    for jelly_item in jelly_list:

        i = jelly_item[0][0]
        j = jelly_item[0][1]

        input_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        input_event.pos = (j * 50 + 1, i * 50 + 1)
        
        for button in [1, 3]:
            input_event.button = button
            temp_world = copy.deepcopy(grid_world)
            new_grid_world, _ = env.run_game(temp_world, [input_event])
            child_state_list.append((repr(new_grid_world)))

    return child_state_list

def is_goal(grid_world, num_of_color):

    return env.detect_winning(grid_world, num_of_color)
        
def breadth_first_search(grid_world):

    # Running BFS and build up the state transition table by the way
    
    frontier = [repr(grid_world)]
    reached = [repr(grid_world)]

    state_list_reached = [repr(grid_world)]

    while frontier:

        temp_grid_world = eval(frontier.pop(0))
        # temp_jelly_list = eval(tuple_[1])

        child_state_list = expand(temp_grid_world)

        # print("child_state_list: ", len(child_state_list))

        for world in child_state_list:
            
            # child_jelly_list = eval(jelly_list)
            if is_goal(eval(world), len(env.color_set)):
                print("Goal!")
                return state_list_reached, [eval(world)]

            if world not in reached:
                reached.append(world)
                frontier.append(world)
                state_list_reached.append(world)

        print("reached: ", len(reached))
        print("frontier: ", len(frontier))

    print("Failure!")

grid_world = env.grid_world

grid_world, jelly_list = env.run_game(grid_world, [])
print(jelly_list)

# child_states = expand(grid_world)

# child_states = [eval(world) for world in child_states]
# draw_world(child_states)


start = time.time()
reached, child_world = breadth_first_search(grid_world)
end = time.time()

print("time: ", end-start)
draw_world(child_world)

# state_to_num_dict = dict()
# num_to_jelly_list_dict = dict()

# for i, tuple_ in enumerate(reached):
#     state_to_num_dict[tuple_[0]] = i
#     num_to_jelly_list_dict[i] = tuple_[1]

# # print(state_to_num_dict)

# state_trans_dict = dict()

# for key, value in state_to_num_dict.items():

#     next_state_list = []
#     child_state_list = expand(eval(key), eval(num_to_jelly_list_dict[value]))

#     for tuple_ in child_state_list:
#         next_state_list.append(state_to_num_dict.get(tuple_[0]))

#     state_trans_dict[value] = next_state_list

# print(state_trans_dict)
