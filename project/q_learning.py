import test as env
import pygame
from copy import deepcopy
import random
from tqdm import tqdm


def translate_action(jelly_list, action):
    grid_size = env.grid_size
    flag = 0
    for jelly in jelly_list:
        if len(jelly) == 2 and jelly[0][2] == action[0]:
            input_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
            y_axis, x_axis, _ = jelly[0]
            input_event.pos = (x_axis * grid_size + 1, y_axis * grid_size + 1)
            if action[-1] == 'l':
                input_event.button = 1
            else:
                input_event.button = 3
            return [input_event]
        if len(jelly) == 1 and jelly[0][2] == action[0] and flag == 0:
            flag += 1
            jelly_1 = jelly[0]
            continue
        if len(jelly) == 1 and jelly[0][2] == action[0] and flag == 1:
            jelly_2 = jelly[0]
            break
    y1_axis, x1_axis, _ = jelly_1
    y2_axis, x2_axis, _ = jelly_2
    if x1_axis > x2_axis:
        jelly_1, jelly_2 = jelly_2, jelly_1
    elif x1_axis == x2_axis and y1_axis > y2_axis:
        jelly_1, jelly_2 = jelly_2, jelly_1

    if action[1] == '1':
        act_jelly = jelly_1
    else:
        act_jelly = jelly_2
    input_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
    y_axis, x_axis, _ = act_jelly
    input_event.pos = (x_axis * grid_size + 1, y_axis * grid_size + 1)
    if action[-1] == 'l':
        input_event.button = 1
    else:
        input_event.button = 3
    return [input_event]

def get_max_action(q_dict):
    val = q_dict[max(q_dict, key=q_dict.get)]
    result = []
    for key in q_dict:
        if q_dict[key] == val:
            result.append(key)
    return result

q_table = dict()
episode_num = 100
episode_step = 40
epi_greedy = 0.8
alpha = 0.8
gamma = 0.9
reward = 100

actions = ['r1_r','r1_l','r2_r','r2_l','g1_r','g1_l','g2_r','g2_l','b1_l','b1_r','b2_l','b2_r']
# 1: left up one, 2: right bot one

for episode in tqdm(range(episode_num)):
    # initial the grid_world and jelly_list
    current_state = deepcopy(env.grid_world)
    grid_size = env.grid_size


    jelly_list = []
    for i in range(10):
        for j in range(14):
            if current_state[i][j] == "r" or current_state[i][j] == "g" or current_state[i][j] == "b":
                jelly_list.append([(i, j, current_state[i][j])])
    ############################################
    # Q-Learning
    for step in range(episode_step):
        if repr(current_state) not in q_table:
            q_table[repr(current_state)] = dict.fromkeys(actions, 0)
            current_action = random.choice(actions)
        else:
            state_detail = q_table[repr(current_state)]
            current_action = random.choice(get_max_action(state_detail))

        if random.random() > 0.8:
            current_action = random.choice(actions)

        eventloop = translate_action(jelly_list, current_action)
        prev_world = repr(current_state)
        current_state, jelly_list = env.run_game(current_state, eventloop, jelly_list)
        # env.draw_world(current_state)
        if len(jelly_list) == 3:
            act_reward = reward
        elif step == 50:
            act_reward = -reward
        else:
            act_reward = 0
        
        if repr(current_state) in q_table:
            q_dict = q_table[repr(current_state)]
            max_next_state = q_dict[max(q_dict, key=q_dict.get)]
        else:
            max_next_state = 0

        q_table[prev_world][current_action] = q_table[prev_world][current_action] + \
                                        alpha * (act_reward + gamma * max_next_state - q_table[prev_world][current_action])
    # env.draw_world(current_state)

