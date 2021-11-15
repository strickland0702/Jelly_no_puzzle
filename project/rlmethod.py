import dr_test as env
import pygame
import copy

# implementation of Breadth-First-Search

def expand(grid_world, jelly_list):

    child_state_list = []

    for jelly_item in jelly_list:

        i = jelly_item[0][0]
        j = jelly_item[0][1]

        # print("i: ", i)
        # print("j: ", j)

        input_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        input_event.pos = (j * 50 + 1, i * 50 + 1)
        
        for button in [1, 3]:
            # print("button: ", button)
            input_event.button = button

            # print("input.button: ", input_event.button)

            # print("raw_jelly_list: ", jelly_list)
            temp_world = copy.deepcopy(grid_world)
            temp_jelly_list = copy.deepcopy(jelly_list)

            new_grid_world, new_jelly_list = env.run_game(temp_world, [input_event], temp_jelly_list)

            # print("raw_jelly_list: ", jelly_list)

            # print("new_jelly_list: ", new_jelly_list)
            if (repr(new_grid_world), repr(new_jelly_list)) not in child_state_list:
                child_state_list.append((repr(new_grid_world), repr(new_jelly_list)))

    return child_state_list

def is_goal(jelly_list):

    return env.detect_winning(jelly_list)
        
def breadth_first_search(grid_world, jelly_list):
    
    frontier = [(repr(grid_world), repr(jelly_list))]
    reached = [(repr(grid_world), repr(jelly_list))]

    while frontier:

        temp_tuple = frontier.pop(0)
        temp_grid_world = eval(temp_tuple[0])
        temp_jelly_list = eval(temp_tuple[1])

        child_state_list = expand(temp_grid_world, temp_jelly_list)

        # print("child_state_list: ", len(child_state_list))

        for tuple_ in child_state_list:
            
            child_jelly_list = eval(tuple_[1])
            if is_goal(child_jelly_list):
                print("Goal!")
                return reached

            if tuple_ not in reached:
                reached.append(tuple_)
                frontier.append(tuple_)

        print("reached: ", len(reached))
        print("frontier: ", len(frontier))

    print("Failure!")
    return reached

grid_world = env.grid_world

grid_world, jelly_list = env.run_game(grid_world, [])

print(jelly_list)

child_state_list = expand(grid_world, jelly_list)

print(len(child_state_list))

for (state, jelly_list) in child_state_list:
    print(eval(jelly_list))

# for child_state in child_state_list:
#     env.draw_world(eval(child_state))

# reached = breadth_first_search(grid_world, jelly_list)

# for state in reached:
#     if is_goal(eval(state)):
#         print("Goal！")
#         break
     

# env.draw_world(child_world)
