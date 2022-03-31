from environment import Environment, get_dict_key
from scipy.spatial.distance import cdist
import numpy as np


def mdist(A, B):
    A = A.reshape(1, -1)
    B = B.reshape(1, -1)
    return cdist(A, B, metric='cityblock')[0][0]


class BenchmarkHeuristic:

    def __init__(self, new_environment):
        self.environment = new_environment
        self.state = self.environment.state
        self.actions = self.environment.actions

    def go_to_coordinate(self, truck_position, coord, destination):
        if truck_position[1] > coord[1]:
            return self.actions["go_left"]
        elif truck_position[1] < coord[1]:
            return self.actions["go_right"]
        else:
            if truck_position[0] > coord[0]:
                return self.actions["go_up"]
            elif truck_position[0] < coord[0]:
                return self.actions["go_down"]
            else:
                # print("Arrived at {}".format(destination))
                if destination == "shop1":
                    return self.get_unload_action(self.state["truck1_inventory"], self.state["shop1_inventory"])
                elif destination == "shop2":
                    return self.get_unload_action(self.state["truck1_inventory"], self.state["shop2_inventory"])
                elif destination == "depot":
                    return self.actions["load_3"]
                else:
                    print("ERROR: DESTINATION NOT FOUND")

    def get_unload_action(self, truck_inventory, shop_inventory):
        max_acceptable_inventory = 3 - shop_inventory
        if max_acceptable_inventory == 0:
            return self.actions["wait"]
        chosen_action = None
        get_dict_result = None
        if truck_inventory < max_acceptable_inventory:
            # print("Truck inventory < max_acceptable_inventory")
            get_dict_result = get_dict_key(self.actions, 3 + truck_inventory)
            chosen_action = self.actions[get_dict_result]
        else:
            # print("Truck inventory >= max_acceptable_inventory")
            get_dict_result = get_dict_key(self.actions, 3 + max_acceptable_inventory)
            chosen_action = self.actions[get_dict_result]
        return chosen_action

    def benchmark_heuristic(self):
        state = self.state
        actions = self.environment.actions
        # state = environment.state
        truck_position = state["position"]
        depot_position = np.array([0, 2])
        shop1_position = np.array([1, 4])
        shop2_position = np.array([2, 1])

        # Check empty truck
        if state["truck1_inventory"] == 0:
            # Try reducing distance b/w depot and truck
            return self.go_to_coordinate(truck_position, depot_position, "depot")

        elif state["shop1_inventory"] == 0:
            return self.go_to_coordinate(truck_position, shop1_position, "shop1")

        elif state["shop2_inventory"] == 0:
            return self.go_to_coordinate(truck_position, shop2_position, "shop2")

        else:
            if mdist(truck_position, shop1_position) < mdist(truck_position, shop2_position):
                return self.go_to_coordinate(truck_position, shop1_position, "shop1")

            else:
                return self.go_to_coordinate(truck_position, shop2_position, "shop2")
