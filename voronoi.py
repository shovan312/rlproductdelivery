import numpy as np

M = 6; N = 10; s = 4

def manDist(a, b):
	return (abs(a[0] - b[0]) + abs(a[1] - b[1]))

shop = [4, 31, 17, 45]
voronoi = []

for i in range(60):
	voronoi.append(0)

for i in range(M*N):
	for j in range(s):
		if(manDist([shop[j]//10, shop[j]%10], [i//10, i%10]) < manDist([shop[voronoi[i]]//10, shop[voronoi[i]]%10], [i//10, i%10])):
			voronoi[i] = j

voronoiString = []
for i in range(6):
	string = ""
	for j in range(10):
		string += str(voronoi[10*i + j])
	print(string)
	voronoiString.append(string)

# ranges = []
# for i in range(6):
# 	x = max(voronoiString[i].rfind('0'), voronoiString[i].rfind('1'))
# 	ranges.append(x)

# print(voronoiString)
# print(ranges)
