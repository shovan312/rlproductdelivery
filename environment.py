import numpy as np
import sys
import random

default_rewards = {
    "fuel": -20, 
    "empty": -5,
    "unload": 50,
    "load": 5,
    "wall": -20,
    "illegal": -100
}


def get_dict_key(dictionary, value):
    final_key = None
    for key, dict_val in dictionary.items():
        if value == dict_val:
            final_key = key
    return final_key

class Environment:
    # State of the environment

    # Actions supported by environment
    prob_shops = [0.3, 0.2, 0.3, 0.2]

    actions = {
        "go_left": 0,
        "go_right": 1,
        "go_up": 2,
        "go_down": 3,

        "unload_1": 4,
        "unload_2": 5,
        "unload_3": 6,

        "load_1": 7,
        "load_2": 8,
        "load_3": 9,

        "wait": 10
    }

    # Position types are used to decide whether or not certain actions can be performed.
    # Eg. Unload actions can only be performed at shops.
    position_types = {
        "shop": 0,
        "depot": 1,
        "location": 2
    }

    shopArray = [4, 17, 31, 45]
    depotArray = [11, 37]

    # Each position is mapped to its type

    #e
    positions = {
        0: position_types["location"],
        1: position_types["location"],
        2: position_types["location"],
        3: position_types["location"],
        4: position_types["shop"],
        5: position_types["location"],
        6: position_types["location"],
        7: position_types["location"],
        8: position_types["location"],
        9: position_types["location"],
        10: position_types["location"],
        11: position_types["depot"],
        12: position_types["location"],
        13: position_types["location"],
        14: position_types["location"],
        15: position_types["location"],
        16: position_types["location"],
        17: position_types["shop"],
        18: position_types["location"],
        19: position_types["location"],
        20: position_types["location"],
        21: position_types["location"],
        22: position_types["location"],
        23: position_types["location"],
        24: position_types["location"],
        25: position_types["location"],
        26: position_types["location"],
        27: position_types["location"],
        28: position_types["location"],
        29: position_types["location"],
        30: position_types["location"],
        31: position_types["shop"],
        32: position_types["location"],
        33: position_types["location"],
        34: position_types["location"],
        35: position_types["location"],
        36: position_types["location"],
        37: position_types["depot"],
        38: position_types["location"],
        39: position_types["location"],
        40: position_types["location"],
        41: position_types["location"],
        42: position_types["location"],
        43: position_types["location"],
        44: position_types["location"],
        45: position_types["shop"],
        46: position_types["location"],
        47: position_types["location"],
        48: position_types["location"],
        49: position_types["location"],
        50: position_types["location"],
        51: position_types["location"],
        52: position_types["location"],
        53: position_types["location"],
        54: position_types["location"],
        55: position_types["location"],
        56: position_types["location"],
        57: position_types["location"],
        58: position_types["location"],
        59: position_types["location"]
    }

    rewards = default_rewards;

    def perform_action(self, truck_id, action, customer_behavior=None):
        action = get_dict_key(self.actions, action)

        reward = 0

        for index, value in enumerate(self.state["shop_inventory"]):
            if customer_behavior is None:
                n = random.random()
                n = n <= self.prob_shops[index]
            else:
                n = customer_behavior[index]
            if n != 0:
                inventory = value
                if inventory > 0:
                    self.state["shop_inventory"][index] -= 1
                else:
                    reward += self.rewards["empty"]


        position = self.state["position"][truck_id]
        positionInd = position[0] * 10 + position[1]

        type_of_location = self.positions[positionInd]
        type_of_action = ""

        if self.actions[action] <= 3:
            type_of_action = 'move'
        elif self.actions[action] <= 6:
            type_of_action = 'unload'
        elif self.actions[action] <= 9:
            type_of_action = 'load'
        else:
            type_of_action = 'wait'

        if type_of_action == 'move':
            # reward += self.rewards["fuel"]
            position = self.state["position"][truck_id]
            newPosition, r = self.moveTruck(position, action, self.n, self.m) 
            if r == self.rewards["wall"]:
                reward += self.rewards["wall"]
                return reward
            else:
                self.state["position"][truck_id] = newPosition

        elif type_of_action == 'unload':

            if type_of_location != self.position_types["shop"]:
                return self.rewards["illegal"]
            else:
                indShop = self.shopArray.index(positionInd)

                L = self.actions[action] - 3
                T = self.state["truck_inventory"][truck_id]
                S = self.state["shop_inventory"][indShop]

                T = T - L
                S = S + L
                if T < 0 or S > 3:
                    return self.rewards["illegal"]

                self.state["shop_inventory"][indShop] = S
                self.state["truck_inventory"][truck_id] = T
                reward += self.rewards["unload"]

        elif type_of_action == 'load':
            if type_of_location != self.position_types["depot"]:
                return self.rewards["illegal"]
            else:
                L = self.actions[action] - 6
                T = self.state["truck_inventory"][truck_id]

                T = T + L
                if T > 3:
                    return self.rewards["illegal"]

                self.state["truck_inventory"][truck_id] = T
                reward += self.rewards["load"]
        return reward

    def __init__(self, n, m, t, s, i_t, i_s, rewards=default_rewards): #dimensions of grid, no. of trucks, no. of shops, max inv of truck, max inv of shop
        self.n = n
        self.m = m
        self.t = t
        self.s = s
        self.i_s = i_s
        self.i_t = i_t
        self.state = {
            "position": np.array([[0, 0]]),
            "shop_inventory": np.array([1, 1, 1, 1]),
            "truck_inventory": np.array([3])
        }
        self.rewards = rewards

    def refresh(self):
        self.state['position'] = np.array([[0, 0]])
        self.state["shop_inventory"] = np.array([1, 1, 1, 1])
        self.state["truck_inventory"] = np.array([3])

    def getStateNumber(self):
        state = self.state
        positionArray = np.array([i[0] * self.m + i[1] for i in state["position"]])

        shopStateNumber = 0
        for i in range(self.s):
            shopStateNumber += state["shop_inventory"][i] * ((self.i_s)**(self.s - i - 1))

        truckInventoryState = 0
        for i in range(self.t):
            truckInventoryState += state["truck_inventory"][i] * ((self.i_t)**(self.t - i - 1))
        
        positionStateNumber = 0
        for i in range(self.t):
            positionStateNumber += positionArray[i] * ((self.m*self.n)**(self.t - 1 - i))

        ans = (self.i_t**self.t) * (self.i_s**self.s) * positionStateNumber + (self.i_t**self.t) * shopStateNumber + truckInventoryState  # 0 - 57599
        return ans


    def moveTruck(self, position, action, n, m):
        reward = 0

        rangesX = [7, 6, 5, 4, 3, 3]
        rangesY = [-1, -1, -1, 4, 3, 2, 1, 0, 0, 0]

        if action == "go_left":
            if position[1] != 0:
            # if position[1] != rangesX[position[0]]:
                position[1] -= 1
                reward = self.rewards["fuel"]
            else:
                reward = self.rewards["wall"]
        if action == "go_right":
            if position[1] != m - 1:
                position[1] += 1
                reward = self.rewards["fuel"]
            else:
                reward = self.rewards["wall"]
        if action == "go_up":
            if position[0] != 0:
            # if position[0] != rangesY[position[1]]:
                position[0] -= 1
                reward = self.rewards["fuel"]
            else:
                reward = self.rewards["wall"]
        if action == "go_down":
            if position[0] != n - 1:
                position[0] += 1
                reward = self.rewards["fuel"]
            else:
                reward = self.rewards["wall"]
        return position, reward


# state = {'position': [[0, 0]], 'shop_inventory': [[0, 0, 2, 0]], 'truck_inventory' : [[2]]}
# N = 6; M = 10; T = 4; S = 4; I_T = 4; I_S = 4
# env = Environment(N, M, 1, S, I_T, I_S)
# print(env.getStateNumber())