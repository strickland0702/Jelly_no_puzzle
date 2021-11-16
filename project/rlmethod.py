import test as env
import pygame
import copy
import time

# implementation of Breadth-First-Search

def expand(grid_world, jelly_list):

    child_state_list = []

    for jelly_item in jelly_list:

        i = jelly_item[0][0]
        j = jelly_item[0][1]

        input_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        input_event.pos = (j * 50 + 1, i * 50 + 1)
        
        for button in [1, 3]:
            input_event.button = button

            temp_world = copy.deepcopy(grid_world)
            temp_jelly_list = copy.deepcopy(jelly_list)

            new_grid_world, new_jelly_list = env.run_game(temp_world, [input_event], temp_jelly_list)
            child_state_list.append((repr(new_grid_world), repr(new_jelly_list)))

    return child_state_list

def is_goal(jelly_list):

    return env.detect_winning(jelly_list)
        
def breadth_first_search(grid_world, jelly_list):

    # Running BFS and build up the state transition table by the way
    
    frontier = [(repr(grid_world), repr(jelly_list))]
    reached = [repr(grid_world)]

    state_list_reached = [(repr(grid_world), repr(jelly_list))]

    while frontier:

        tuple_ = frontier.pop(0)
        temp_grid_world = eval(tuple_[0])
        temp_jelly_list = eval(tuple_[1])

        child_state_list = expand(temp_grid_world, temp_jelly_list)

        # print("child_state_list: ", len(child_state_list))

        for (world, jelly_list) in child_state_list:
            
            child_jelly_list = eval(jelly_list)
            if is_goal(child_jelly_list):
                print("Goal!")
                return state_list_reached, eval(world), child_jelly_list

            if world not in reached:
                reached.append(world)
                frontier.append((world, jelly_list))
                state_list_reached.append((world, jelly_list))

        print("reached: ", len(reached))
        print("frontier: ", len(frontier))

    print("Failure!")

grid_world = env.grid_world

grid_world, jelly_list = env.run_game(grid_world, [])

print(jelly_list)

start = time.time()
reached, child_world, child_jelly_list = breadth_first_search(grid_world, jelly_list)
end = time.time()

print("time: ", end-start)
env.draw_world(child_world)

state_to_num_dict = dict()
num_to_jelly_list_dict = dict()

for i, tuple_ in enumerate(reached):
    state_to_num_dict[tuple_[0]] = i
    num_to_jelly_list_dict[i] = tuple_[1]

# print(state_to_num_dict)

state_trans_dict = dict()

for key, value in state_to_num_dict.items():

    next_state_list = []
    child_state_list = expand(eval(key), eval(num_to_jelly_list_dict[value]))

    for tuple_ in child_state_list:
        next_state_list.append(state_to_num_dict.get(tuple_[0]))

    state_trans_dict[value] = next_state_list

print(state_trans_dict)
