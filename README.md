# Warehouse-Robot-Search-Problem

There is a robot that needs to load and unload a truck.  The truck contains small and large boxes.   Small boxes go to warehouse A and large boxes go to Warehouse B.  In addition there are medium boxes in both warehouses.  The robot must load these medium boxes onto the truck.  

The problem is modelled where each state is the number of small, large, and medium boxes not in their proper place.  We use an A* search alogorithm where the cost of travelling between locations is 1 except for between the two warehouses where the cost is 2.  We use two heuristics based on how many unsorted boxes are left in a state if we move to it.
