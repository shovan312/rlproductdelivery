import numpy as np
from environment import Environment


array_00 = []
array_59 = []
array_rand = []

def simrew(start_pos):
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

	q_table = np.loadtxt("./qtable_start59.txt")

	for i in range(T):
		env.append(Environment(N, M, 1, S, I_T, I_S, rewards))

	env[0].state["position"] = [start_pos]

	totalReward = 0
	iterations = 200

	for i in range(iterations):
		for t in range(T):
			stateNumber = env[t].getStateNumber()
			
			q_values = q_table[stateNumber]

			if(np.count_nonzero(q_values) == 0):
				position = env[t].state["position"][0]
				positionStateNumber = position[0]*10 + position[1]
				for j in range((I_T) * (I_S**S) * positionStateNumber, (I_T) * (I_S**S) * positionStateNumber + (I_T) * (I_S**S)):
					if(np.count_nonzero(q_table[i]) >= 0):
						q_values = q_table[j]
						break

			action = np.random.choice(np.flatnonzero(q_values == q_values.max()))

			actionStr = ""
			for stri, number in env[t].actions.items():
				if action == number:
					actionStr = stri

			action = actionStr

			reward = env[t].perform_action(0, env[t].actions[action])
			# print(env[0].state, action, reward)
			totalReward += reward

			for t2 in range(T):
				env[t2].state["shop_inventory"] = env[t].state["shop_inventory"]
	print(totalReward)
	return totalReward

for i in range(60):
	reward = 0
	for j in range(5):
		reward += simrew([i//10, i%10])
	reward /= 5
	print(i)
	array_59.append(reward)

filename = "./array59.txt"
np.savetxt(filename, array_59)
# filename = "./array00.txt"
# np.savetxt(filename, array_00)
# filename = "./arrayrand.txt"
# np.savetxt(filename, array_rand)