import numpy as np

from benchmark import BenchmarkHeuristic
from environment import Environment
import copy

import sys


def simrew():
    N = 6; M = 10; T = 1; S = 4; I_T = 4; I_S = 4

    env = []

    rewards = {
        "fuel": int(sys.argv[1]),
        "empty": int(sys.argv[2]),
        "unload": int(sys.argv[3]),
        "load": int(sys.argv[3]),
        "wall": int(sys.argv[1]),
        "illegal": -100
    }

    q_table = np.loadtxt("./reward_test/qtable("+str(sys.argv[1])+")("+str(sys.argv[2])+")("+str(sys.argv[3])+").txt")
    # q_table = np.loadtxt("./qtable(-1)(-5)(20).txt")
    # q_table = np.loadtxt("./qtable_voronoi23.txt")
    # q_table = np.loadtxt("./qtable_voronoi23.txt")

    for i in range(T):
        env.append(Environment(N, M, 1, S, I_T, I_S, rewards))

    env[0].state["position"] = [[5, 9]]
    # env[1].state["position"] = [[0, 1]]
    # env[0].state["position"] = [[0, 2]]
    # env[3].state["position"] = [[0, 3]]

    totalReward = 0
    iterations = 200

    for i in range(iterations):
        for t in range(T):
            stateNumber = env[t].getStateNumber()

            q_values = q_table[stateNumber]

            if(np.count_nonzero(q_values) == 0):
                # print("all zero")
                position = env[t].state["position"][0]
                positionStateNumber = position[0]*10 + position[1]
                for j in range((I_T) * (I_S**S) * positionStateNumber, (I_T) * (I_S**S) * positionStateNumber + (I_T) * (I_S**S)):
                    if(np.count_nonzero(q_table[i]) >= 0):
                        print(j)
                        q_values = q_table[j]
                        break

                # for j in q_values:
                #     print(j ," ", end="")
                # print("\n")

            action = np.random.choice(np.flatnonzero(q_values == q_values.max()))

            actionStr = ""
            for stri, number in env[t].actions.items():
                if action == number:
                    actionStr = stri

            action = actionStr

            print(i, env[t].state, end=" ")

            reward = env[t].perform_action(0, env[t].actions[action])
            totalReward += reward
            print(reward, action)

            for t2 in range(T):
                env[t2].state["shop_inventory"] = env[t].state["shop_inventory"]
        
        # print("-----------------------")
        # print(env[1].state)
        print("\n")

    return totalReward


if __name__ == "__main__":
    totalReward = simrew()
    print(totalReward)

