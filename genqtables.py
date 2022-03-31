import sys
import os

fuel_arr = [-1, -5, -10, -20]
empty_arr = [-1, -5, -10, -20]
unload_arr = [2, 5, 10, 20]

for i in range(64):
	f_ind = (i//16)%4
	e_ind = (i//4)%4
	u_ind = i%4

	os.system("python3 qtable.py " + str(fuel_arr[f_ind]) + " " + str(empty_arr[e_ind]) + " " + str(unload_arr[u_ind]))
