# Genetic Algorithm-Facility Assignment
 
Let N be the set of clients, M be the set of candidate sites for locating facilities, and dij be the distance from client i, i ϵ N, to candidate site j, j ϵ M. The problem is to open k facilities and assign each client to its closest open facility, in order to minimize the total distance (the sum of the distances for all the clients to go to the closest open facility). A specific example for you to solve is given in the attached Excel file (Sheet 1), where there are 100 clients and 20 candidate sites. Suppose to open 5 facilities (k = 5). 

Variables:
i: clients, i ϵ N.
j: candidate locations, j ϵ M.
dij: distance between client i and location j.
k: the number of facilities to open. 

Decision variable: 
Binary variable Xj ϵ {0, 1}: if the candidate location j is open. 
Binary variable Aij ϵ {0, 1}: if client i is assigned to location j.

Objective function: 
	Min: ∑∑_[dij *  Aij]*Xj   

Constraints:
	ΣAij = 1, ∀ⅈ
	ΣX_j=k 
	Aij ≤ Xj, ∀j
