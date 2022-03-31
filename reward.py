import sys

purchase_probability = 0.05
iterations = 0


def get_reward(state, action, environment):
    reward = -0.1
    if purchase_probability * iterations >= 1:
        pass
    # for i in shops:
    #     if (i.Inv == 0):
    #         reward -= 5

    L = environment.actions[action] - 3
    T = state["truck1_inventory"]
    if state["position"] == 2:
        S = state["shop1_inventory"]
    elif state["position"] == 5:
        S = state["shop2_inventory"]
    else:
        print("Unexpected Error")
        sys.exit(0)

    T = T - L
    S = S + L
    if T < 0 or S > 3:
        return -10000

    reward += 10 ** (S - 3)

    return reward
