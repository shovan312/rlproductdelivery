import numpy as np
from environment import Environment
import matplotlib.pyplot as plt

def simrew(qtable, start_pos):
    N = 6; M = 10; T = 1; S = 4; I_T = 4; I_S = 4

    env = []

    rewards = {
        "fuel": -1,
        "empty": -5,
        "unload": 20,
        "load": 20,
        "wall": -1,
        "illegal": -100
    }

    q_table = np.loadtxt(qtable)
    # q_table = np.loadtxt("./qtablestart_00.txt")
    # q_table = np.loadtxt("./qtablestart_59.txt")
    # q_table = np.loadtxt("./qtable_voronoi23.txt")
    # q_table = np.loadtxt("./qtable_voronoi23.txt")

    for i in range(T):
        env.append(Environment(N, M, 1, S, I_T, I_S, rewards))

    env[0].state["position"] = [start_pos]
    # env[1].state["position"] = [[0, 1]]
    # env[0].state["position"] = [[0, 2]]
    # env[3].state["position"] = [[0, 3]]

    totalReward = 0
    iterations = 200

    reward_arr = []

    for i in range(iterations):
        for t in range(T):
            stateNumber = env[t].getStateNumber()

            q_values = q_table[stateNumber]

            if(np.count_nonzero(q_values) == 0):
                position = env[t].state["position"][0]
                positionStateNumber = position[0]*10 + position[1]
                for j in range((I_T) * (I_S**S) * positionStateNumber, (I_T) * (I_S**S) * positionStateNumber + (I_T) * (I_S**S)):
                    if(np.count_nonzero(q_table[i]) >= 0):
                        print(j)
                        q_values = q_table[j]
                        break

            action = np.random.choice(np.flatnonzero(q_values == q_values.max()))

            actionStr = ""
            for stri, number in env[t].actions.items():
                if action == number:
                    actionStr = stri

            action = actionStr

            reward = env[t].perform_action(0, env[t].actions[action])
            totalReward += reward
            reward_arr.append(totalReward)
        
    return reward_arr


if __name__ == "__main__":
    reward_arr00 = simrew("qtable_start00.txt", [0, 0])
    reward_arr59 = simrew("qtable_start59.txt", [0, 0])
    reward_arr_random = simrew("qtable(-1)(-5)(20).txt", [0, 0])

    x = [i for i in range(200)]
    plt.plot(x, reward_arr00, 'r')
    plt.plot(x, reward_arr59, 'g')
    plt.plot(x, reward_arr_random, 'b')
    plt.show()


