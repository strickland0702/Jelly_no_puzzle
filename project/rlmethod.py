import test as env
import pygame
import copy

# implementation of Breadth-First-Search

def expand(grid_world):

    child_state_list = []
    _, jelly_list = env.run_game(grid_world, [])

    for jelly_item in jelly_list:

        i = jelly_item[0][0]
        j = jelly_item[0][1]

        print("i: ", i)
        print("j: ", j)

        input_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        input_event.pos = (j * 50 + 1, i * 50 + 1)
        
        for button in [1, 3]:
            print("button: ", button)
            input_event.button = button

            print("input.button: ", input_event.button)

            print("raw_jelly_list: ", jelly_list)
            temp_world = copy.deepcopy(grid_world)

            _, old_jelly_list = env.run_game(temp_world, [])

            print("old_jelly_list: ", old_jelly_list)

            new_grid_world, new_jelly_list = env.run_game(temp_world, [input_event])

            print("raw_jelly_list: ", jelly_list)

            print("new_jelly_list: ", new_jelly_list)
            child_state_list.append(repr(new_grid_world))

    return child_state_list

def is_goal(grid_world):

    _, jelly_list = env.run_game(grid_world, [])
    return env.detect_winning(jelly_list)
        
def breadth_first_search(grid_world):
    if is_goal(grid_world):
        return grid_world
    
    frontier = [repr(grid_world)]
    reached = [repr(grid_world)]

    count = 0

    while frontier:
        grid_world = eval(frontier.pop(0))

        child_state_list = expand(grid_world)

        print("child_state_list: ", len(child_state_list))

        for child_world in child_state_list:
            if is_goal(child_world):
                return reached, child_world

            str_world = repr(child_world)
            if str_world not in reached:
                reached.append(str_world)
                frontier.append(str_world)

            print("reached: ", len(reached))
            # print("frontier: ", frontier)

        count += 1

        if count == 2:
            break

    print("Failure!")

grid_world = env.grid_world

child_state_list = expand(grid_world)

# for child_state in child_state_list:
#     env.draw_world(eval(child_state))

# reached, child_world = breadth_first_search(grid_world)

# print(len(reached))

# env.draw_world(child_world)
