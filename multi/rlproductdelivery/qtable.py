import numpy as np
import random
import matplotlib.pyplot as plt
from environment import Environment
from sim import simrew


if __name__ == "__main__":
    s = ((5*3)**2)*(4**2)*(4**2)
    a = 11 ** 2
    gamma = 0.95
    alpha = 0.8
    alp = []
    simreward = []
    benchmarkreward = []
    iterations = 100
    prob_shops = [0.3, 0.2]

    customer_behaviour = np.random.rand(2, iterations)
    customer_behaviour[0] = customer_behaviour[0] < prob_shops[0]
    customer_behaviour[1] = customer_behaviour[1] < prob_shops[1]
    customer_behaviour = customer_behaviour.T.astype(int)

    q_table = np.zeros([s, a])
    epsilon = 1
    N = 3; M = 5; T = 2; S = 2; I_T = 4; I_S = 4
    environment = Environment(N, M, T, S, I_T, I_S)
    for i in range(1, 100001):
        environment.refresh()
        state = environment.state
        reward = 0
        done = False
        totalReward = 0
        while not done:
            action_array = np.array([0, 0], dtype=int)
            currStateNumber = environment.getStateNumber()
            for truck_id in range(len(state["position"])):
                if random.uniform(0, 1) < epsilon:
                    action_array[truck_id] = np.random.randint(11)  # random action
                else:
                    if truck_id == 0:
                        action_array[truck_id] = np.argmax(q_table[currStateNumber]) // (11**(T-truck_id))
                    elif T - truck_id - 1 == 0:
                        action_array[truck_id] = np.argmax(q_table[currStateNumber]) % 11

            for truck_id in range(len(state["position"])):
                reward += environment.perform_action(truck_id, action_array[truck_id])
            
            totalReward += reward
            
            newStateNumber = environment.getStateNumber()
            
            if(totalReward <= -15000 or totalReward >= 10000):
                done = True

            next_max = np.max(q_table[newStateNumber])

            action = 0
            for j in range(T):
                action += action_array[j]*(11**(T-j-1))

            q_table[currStateNumber, action] = (1-alpha) * q_table[currStateNumber, action] + alpha * (
                    reward + (gamma * next_max))

            epsilon = epsilon*np.exp(-np.log(2)/10000)
            
        if i % 10000 == 0:
            print('Episode: {}'.format(i))

    print('Training Finished..')
    np.savetxt("qtable.txt", q_table)


    # environment.refresh()
    # netReward = 0

    # for j in range(100):
    #     s0 = environment.state
    #     print("State:{}".format(s0))
    #     print()
    #     sNumber = environment.getStateNumber()
    #     actionNum = np.argmax(q_table[sNumber])
    #     reward = [0, 0]
    #     action_array= [actionNum//11, actionNum%11]

    #     for truck_id in range(2):
    #         if truck_id == 0:
    #             reward[truck_id] = environment.perform_action(truck_id, actionNum//11)
    #         elif truck_id == 1:
    #             reward[truck_id] = environment.perform_action(truck_id, actionNum%11)
    #     actionStr_array = ["", ""]
    #     netReward += reward[0] + reward[1]
    #     for j in range(2):
    #         actionStr = ""
    #         for stri, number in environment.actions.items():
    #             if action_array[j] == number:
    #                 actionStr = stri
    #         actionStr_array[j] = actionStr
    #     print("Action:{}".format(actionStr_array))
    #     print()
    #     print("NewState: {}".format(s0))
    #     print()
    #     print("Reward:{}".format(reward))
    #     print()
    # print(netReward)