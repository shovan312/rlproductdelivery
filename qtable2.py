import numpy as np
import sys
import random
import matplotlib.pyplot as plt
from environment import Environment

if __name__ == "__main__":
    tr = []
    for i in range(3):
        N = 6; M = 10; T = 1; S = 4; I_T = 4; I_S = 4
        s = ((M*N)**T)*(I_S**S)*(I_T**T)
        a = 11 ** T
        gamma = 0.95
        alpha = 0.8

        episodes = 240
        steps = 1000


        #argv = ['qtable.py', fuel, empty, unload]

        rewards = {
            "fuel": int(sys.argv[1]),
            "empty": int(sys.argv[2]),
            "unload": int(sys.argv[3]),
            "load": int(sys.argv[3]),
            "wall": int(sys.argv[1]),
            "illegal": -100
        }

        environment = Environment(N, M, T, S, I_T, I_S, rewards)

        usedCoords = set()
        currCoord = 0
        currCoords = [0, 0, 59]
        epsilon = 1
        q_table = np.zeros([s, a])
        rew = []
        for episode in range(episodes):
            environment.refresh()

            if(i==1):
                if(episode%(episodes//(N*M)) == 0):
                    while(True):
                        currCoord = random.randint(0, (N*M - 1))
                        if(currCoord not in usedCoords):
                            break

                    usedCoords.add(currCoord)
                    print("new currCord : {}".format(currCoord))
                
                environment.state["position"] = [[currCoord//M, currCoord%M]]

            if(i==0 or i==2):
                environment.state["position"] = [[currCoords[i]//M, currCoords[i]//N]]

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

            if episode % 10 == 0:
                print('Episode: {}'.format(episode))
            rew.append(totalReward)
        tr.append(rew)

        print('Training Finished..')

    # filename = "./qtable(" + str(sys.argv[1]) + ")(" + str(sys.argv[2]) + ")(" + str(sys.argv[3]) + ").txt"
    # filename = "./qtable_start59.txt"
    # np.savetxt(filename, q_table)
    x = [i for i in range(240)]
    plt.plot(x, tr[0], 'r')
    plt.plot(x, tr[1], 'g')
    plt.plot(x, tr[2], 'b')
    plt.xticks(np.arange(min(x), max(x)+1, 8))
    plt.grid()
    plt.show()