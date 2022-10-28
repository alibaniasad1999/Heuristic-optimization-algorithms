# Python program to print all paths from a source to destination.

from math import inf
import csv
from collections import defaultdict

from torch import le
global allpaths
allpaths = []
# This class represents a directed graph
# using adjacency list representation
class Graph:

	def __init__(self, vertices):
		# No. of vertices
		self.V = vertices
		
		# default dictionary to store graph
		self.graph = defaultdict(list)

	# function to add an edge to graph
	def addEdge(self, u, v):
		self.graph[u].append(v)

	'''A recursive function to print all paths from 'u' to 'd'.
	visited[] keeps track of vertices in current path.
	path[] stores actual vertices and path_index is current
	index in path[]'''
	def printAllPathsUtil(self, u, d, visited, path):

		# Mark the current node as visited and store in path
		visited[u]= True
		path.append(u)

		# If current vertex is same as destination, then print
		# current path[]
		if u == d:
			# print(path)
			allpaths.append(path.copy())
		else:
			# If current vertex is not destination
			# Recur for all the vertices adjacent to this vertex
			for i in self.graph[u]:
				if visited[i]== False:
					self.printAllPathsUtil(i, d, visited, path)
					
		# Remove current vertex from path[] and mark it as unvisited
		path.pop()
		visited[u]= False


	# Prints all paths from 's' to 'd'
	def printAllPaths(self, s, d):

		# Mark all the vertices as not visited
		visited =[False]*(self.V)

		# Create an array to store paths
		path = []

		# Call the recursive helper function to print all paths
		self.printAllPathsUtil(s, d, visited, path)



Map = [[1, 1, 1, 1, 1],
	   [1, 1, 0, 1, 1],
	   [1, 0, 1, 1, 1],
	   [1, 0, 1, 1, 1],
	   [1, 1, 1, 1, 1]]

map_sum = 0
for i in Map:
	map_sum += sum(i)

numerical_map = [[0 for i in range(len(Map[0]))] for j in range(len(Map))]

counter = 0
for i in range(len(Map)*len(Map)):
	if Map[i//len(Map)][i%len(Map)] == 1:
		numerical_map[i//len(Map)][i%len(Map)] = counter
		counter += 1
	else:
		numerical_map[i//len(Map)][i%len(Map)] = inf

# print(numerical_map)

g = Graph(max(max(numerical_map)) + 1)
for i in range(len(numerical_map)):
	for j in range(len(numerical_map)):
		if numerical_map[i][j] == inf:
			continue
		if i >= 1:
			if numerical_map[i-1][j] != inf:
				g.addEdge(numerical_map[i][j], numerical_map[i-1][j])
				# print(numerical_map[i][j], numerical_map[i-1][j])
		if i < len(numerical_map)-1:
			if numerical_map[i+1][j] != inf:
				g.addEdge(numerical_map[i][j], numerical_map[i+1][j])
				# print(numerical_map[i][j], numerical_map[i+1][j])
		if j >= 1:
			if numerical_map[i][j-1] != inf:
				g.addEdge(numerical_map[i][j], numerical_map[i][j-1])
				# print(numerical_map[i][j], numerical_map[i][j-1])
		if j < len(numerical_map)-1:
			if numerical_map[i][j+1] != inf:
				g.addEdge(numerical_map[i][j], numerical_map[i][j+1])
				# print(numerical_map[i][j], numerical_map[i][j+1])
			



s = 15 ; d = 9
# print ("Following are all different paths from % d to % d :" %(s, d))
g.printAllPaths(s, d)
# print('#############')
# print(allpaths)
# print('#############')
# print(len(allpaths))

sorted_paths = sorted(allpaths, key=len)
for num, path in enumerate(sorted_paths):
	print(path, 'No:', num)

# np.savetxt("paths.csv", 
#            sorted_paths,
#            delimiter =", ", 
#            fmt ='% s')


with open('paths.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(sorted_paths)

with open('numerical_map.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(numerical_map)

with open('map.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(Map)
