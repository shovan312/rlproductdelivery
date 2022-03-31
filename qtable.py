import numpy as np
import sys
import random
import matplotlib.pyplot as plt
from environment import Environment

if __name__ == "__main__":
    N = 6; M = 10; T = 1; S = 4; I_T = 4; I_S = 4
    s = ((M*N)**T)*(I_S**S)*(I_T**T)
    a = 11 ** T
    gamma = 0.95
    alpha = 0.8

    episodes = 9960
    steps = 1000

    q_table = np.zeros([s, a])
    epsilon = 1

    #argv = ['qtable.py', fuel, empty, unload]

    rewards = {
        "fuel": int(sys.argv[1]),
        "empty": int(sys.argv[2]),
        "unload": int(sys.argv[3]),
        "load": int(sys.argv[3]),
        "wall": int(sys.argv[1]),
        "illegal": -100
    }

    # print(rewards)

    environment = Environment(N, M, T, S, I_T, I_S, rewards)

    usedCoords = set()
    currCoord = 0
    for episode in range(episodes):
        environment.refresh()

        # if(episode%(episodes//(N*M)) == 0):
        #     while(True):
        #         currCoord = random.randint(0, (N*M - 1))
        #         if(currCoord not in usedCoords):
        #             break

        #     usedCoords.add(currCoord)
        #     print("new currCord : {}".format(currCoord))
        
        # environment.state["position"] = [[currCoord//M, currCoord%M]]

        environment.state["position"] = [[0, 0]]

        state = environment.state

        reward = 0
        totalReward = 0

        for step in range(steps):
            currStateNumber = environment.getStateNumber()
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, a - 1)  # random action
            else:
                action = np.random.choice(np.flatnonzero(q_table[currStateNumber] == q_table[currStateNumber].max())) #to prevent only left actions

            reward = environment.perform_action(0, action)
            totalReward += reward
        
            newStateNumber = environment.getStateNumber()

            next_max = np.max(q_table[newStateNumber])

            q_table[currStateNumber, action] = (1-alpha) * (q_table[currStateNumber, action]) + alpha * (reward + (gamma * next_max))

            epsilon = epsilon*np.exp(-np.log(2)/(step//2)) 

        if episode % 1000 == 0:
            print('Episode: {}'.format(episode))

    print('Training Finished..')

    # filename = "./qtable(" + str(sys.argv[1]) + ")(" + str(sys.argv[2]) + ")(" + str(sys.argv[3]) + ").txt"
    filename = "./qtable_start00.txt"
    np.savetxt(filename, q_table)