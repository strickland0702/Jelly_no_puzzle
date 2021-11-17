import test as env
import pygame
from copy import deepcopy
import random
from tqdm import tqdm
import numpy as np

def translate_action(action):
    
    input_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
    y_axis, x_axis = action[0][0], action[0][1]
    input_event.pos = (x_axis * 50 + 1, y_axis * 50 + 1)
    input_event.button = action[1]

    return [input_event]
        

def get_max_action(dict_):
    best_action = None
    max_value = -np.inf
    for key, value in dict_.items():
        if value > max_value:
            max_value = value
            best_action = [key]
        elif value == max_value:
            best_action.append(key)
            
    return best_action

num_of_episodes = 100000
num_of_steps = 66
q_table = dict()
epi_greedy = 0.9
alpha = 0.5
gamma = 0.9
reward = 100

current_state = deepcopy(env.grid_world)
init_jelly = []
for i in range(10):
    for j in range(14):
        if current_state[i][j] == "r" or current_state[i][j] == "g" or current_state[i][j] == "b":
            init_jelly.append([(i, j, current_state[i][j])])
            

for episode in tqdm(range(num_of_episodes)):
    current_state = deepcopy(env.grid_world)
    jelly_list = init_jelly.copy()
    
    # env.draw_world(current_state)
    
    ################################################
    # Q-Learning
        
    for step in range(num_of_steps):
        
        action_list = []
        for jelly_item in jelly_list:
            for jelly in jelly_item:
                for button in [1, 3]:
                    action_list.append((jelly, button)) 
                    
        if repr(current_state) not in q_table.keys():
            q_table[repr(current_state)] = dict.fromkeys(action_list, 0)
            current_action = random.choice(action_list)
        else:
            state_detail = q_table[repr(current_state)]
            current_action = random.choice(get_max_action(state_detail))

        # epsilon-greedy
        if random.random() > 0.95:
            current_action = random.choice(action_list)

        eventloop = translate_action(current_action)
        prev_world = repr(current_state)
        current_state, jelly_list = env.run_game(current_state, eventloop, jelly_list)
        
        break_flag = 0
        
        if len(jelly_list) == 3:
            print("yes!")
            act_reward = 1000
            break_flag = 1
        elif step == (num_of_steps-1):
            act_reward = -5
#         elif repr(current_state) in mistake:
#             act_reward = -100
#             break_flag = 1
        else:
            act_reward = 0
        
        if repr(current_state) in q_table:
            q_dict = q_table[repr(current_state)]
            max_next_state = q_dict[max(q_dict, key=q_dict.get)]
        else:
            max_next_state = 0

        q_table[prev_world][current_action] = q_table[prev_world][current_action] + \
                                        alpha * (act_reward + gamma * max_next_state - q_table[prev_world][current_action])
        
        if break_flag:
            break

current_state = deepcopy(env.grid_world)
jelly_list = init_jelly.copy()

while True:
    env.draw_world(current_state)
    state_detail = q_table[repr(current_state)]
    current_action = random.choice(get_max_action(state_detail))

    eventloop = translate_action(current_action)
    current_state, jelly_list = env.run_game(current_state, eventloop, jelly_list)
    
    if len(jelly_list) == 3:
        print("Yes!")
        break