#Implementing A* search algorithm
#F29AI Fall 2017/2018
#Corey Sutphin 
#A* search code adapted form https://www.redblobgames.com/pathfinding/a-star/implementation.html

#State Space: Each state contains number of small,large, and medium boxes in A and B that are not in their correct position
#Heuristic 1: h(n) = initial total of all packages - current total of all packages
#Heuristic 2: h(n) = ratio of sorted vs. unsorted boxes
#Goal encoding: S,L,Ma, and Mb all = 0

import collections, heapq

#Cost of moving from an adjacent location(A to truck, B to truck) has cost 1,
#cost of moving from warehouse to warehouse has cost of 2.
cost_of_moving = {
	('Truck','A'): 1,
	('Truck','B'): 1,
	('A','Truck'): 1,
	('B','Truck'): 1,
	('A','B'): 2,
	('B','A'): 2
}

#Our transition function, returns the states they can move to given their position
def get_transitions(small,large,medium_A,medium_B,position):
	if(position == 'Truck'):
		return [filter(small-1,large,medium_A,medium_B,'A'),filter(small,large-1,medium_A,medium_B,'B')]
	elif(position == 'A'):
		return [filter(small,large,medium_A-1,medium_B,'Truck'),filter(small,large,medium_A,medium_B,'B')]
	elif(position == 'B'):
		return [filter(small,large,medium_A,medium_B-1,'Truck'),filter(small,large,medium_A,medium_B,'A')]
		
# When passed the variables of a state, ensures that no values are negative.  Used in get_transitions()
def filter(small, large, medium_A, medium_B, position):
	if(small < 0):
		small = 0
	if(large < 0):
		large = 0
	if(medium_A < 0):
		medium_A = 0
	if(medium_B < 0):
		medium_B = 0
	return (small,large,medium_A,medium_B,position)

class WeightedGraph:
	def __init__(self):
		self.edges = {}
		
	def cost(self, from_node, to_node):
		(s1,l1,ma1,mb1,pos1) = from_node
		(s2,l1,ma2,mb2,pos2) = to_node
		return cost_of_moving[pos1,pos2]
		
	def neighbors(self, id):
		(small,large,medium_A,medium_B,position) = id
		return get_transitions(small,large,medium_A,medium_B,position)
			
class PriorityQueue:
	def __init__(self):
		self.elements = []
	
	def empty(self):
		return len(self.elements) == 0
	
	def put(self, item, priority):
		heapq.heappush(self.elements, (priority, item))
	
	def get(self):
		return heapq.heappop(self.elements)[1]
		
# Subtracts the current number of unsorted boxes from the intial number of unsorted boxes
def heuristic_1(x,y):
	(small_1,large_1,medium_A_1,medium_B_1,position) = x
	(small_2,large_2,medium_A_2,medium_B_2,position) = y
	return (small_1 + large_1 + medium_A_1 + medium_B_1) - (small_2 + large_2 + medium_A_2 + medium_B_2)
	
# Returns the ratio of sorted boxes vs. unsorted boxes
def heuristic_2(x,y):
	(small_1,large_1,medium_A_1,medium_B_1,position) = x
	(small_2,large_2,medium_A_2,medium_B_2,position) = y
	sorted = (small_1 + large_1 + medium_A_1 + medium_B_1) - (small_2 + large_2 + medium_A_2 + medium_B_2)
	unsorted = (small_2 + large_2 + medium_A_2 + medium_B_2)
	if(unsorted == 0):
		return sorted;
	else:
		return (sorted/unsorted)
	
def a_star_search(graph,start,goal,heuristic):
	frontier = PriorityQueue()
	frontier.put(start,0)
	came_from = {}
	cost_so_far = {}
	came_from[start] = None
	cost_so_far[start] = 0
	
	while not frontier.empty():
		current = frontier.get()
		
		if current == goal:
			break
	
		for next in graph.neighbors(current):
			new_cost = cost_so_far[current] + graph.cost(current, next)
			if next not in cost_so_far or new_cost < cost_so_far[next]:
				cost_so_far[next] = new_cost
				priority = new_cost + heuristic(start, next)
				print(next,priority)
				frontier.put(next, priority)
				came_from[next] = current
				
	return came_from, cost_so_far
	
def reconstruct_path(came_from, start, goal):
	current = goal
	path = [current]
	while current != start:
		current = came_from[current]
		path.append(current)
	path.reverse() 
	return path

#Main code to perform the searches with heuristic 1 and heuristic 2
graph = WeightedGraph()
start = (2,2,3,4,'Truck')
goal = (0,0,0,0,'Truck')
came_from, cost_so_far = a_star_search(graph,start,goal,heuristic_1)
print("\nPath found!")
print(reconstruct_path(came_from,start,goal))
print("\nA* Search ran with heuristic 2!")
start = (5,6,2,4,'Truck')
goal = (0,0,0,0,'Truck')
came_from,cost_so_far = a_star_search(graph,start,goal,heuristic_2)
print("\nPath found!")
print(reconstruct_path(came_from,start,goal))
