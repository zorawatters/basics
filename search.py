#!/usr/bin/python
import numpy as np
from collections import deque
import heapq


#this file is going to contain different search algorithms to find paths from one point on a grid to another

#helpers

#grid obstacles for test
grid = [(x+1, y+1) for x in range(25) for y in range(16)]
blocked = []
#stair block to the left
blocked = [(1,y) for y in range(2, 15)]
blocked = blocked + [(2,y) for y in range(3, 14)]
blocked = blocked + [(3,y) for y in range(4, 13)]
blocked = blocked + [(4,y) for y in range(5, 12)]
#line across bottom
blocked = blocked + [(x,1) for x in range(5, 24)]
#middle chunk
blocked = blocked + [(x,y) for x in range (10,14) for y in range(9, 13)]
blocked = blocked + [(x,y) for x in range (11,15) for y in range(13, 15)]
blocked.append((14, 12))
blocked.append((14, 11))
#big square
blocked = blocked + [(x,y) for x in range (21,26) for y in range(11, 17)]
#yellow square 
goal = (25, 9)
#returning dictionary of legal moves with step cost as values
def adjacent_states(state):
    states = {}
    #east
    if (state[0] + 1, state[1]) not in blocked and (state[0] + 1, state[1]) in grid: 
        states[(state[0] + 1, state[1])] = 1
    #west
    if (state[0] - 1, state[1]) not in blocked and (state[0] - 1, state[1]) in grid: 
        states[(state[0] - 1, state[1])] = 1
    #north
    if (state[0], state[1] + 1) not in blocked and (state[0], state[1] + 1) in grid: 
        states[(state[0], state[1] + 1)] = 1
    #south
    if (state[0], state[1] - 1) not in blocked and (state[0], state[1] - 1) in grid: 
        states[(state[0], state[1] - 1)] = 1
    #diagonals
    #up and right
    if (state[0] + 1, state[1] + 1) not in blocked and (state[0] + 1, state[1] + 1) in grid: 
        states[(state[0] + 1, state[1] + 1)] = np.sqrt(2)
    #up and left
    if (state[0] - 1, state[1] + 1) not in blocked and (state[0] - 1, state[1] + 1) in grid: 
        states[(state[0] - 1, state[1] + 1)] = np.sqrt(2)
    #down and left
    if (state[0] + 1, state[1] - 1) not in blocked and (state[0] + 1, state[1] - 1) in grid: 
        states[(state[0] + 1, state[1] - 1)] = np.sqrt(2)
    #down and right
    if (state[0] - 1, state[1] - 1) not in blocked and (state[0] - 1, state[1] - 1) in grid: 
        states[(state[0] - 1, state[1] - 1)] = np.sqrt(2)
    return states


#this is a recursive function to retrace the steps of the search and return the path it took. prev is a dictionary that holds the predecessor state that led to each state; initial will be None
def path(prev, state): 
    if state is None:
        return []
    return path(prev, prev[state])+[state]

#this is a function to return the cost of a given path
def pathcost(path):
    cost = 0
    for s in range(len(path)-1):
        if (path[s][0] == path[s+1][0]) or (path[s][1] == path[s+1][1]): #if col or row - moving left/right/up/down
            cost += 1
        else:
            cost += np.sqrt(2)
    return cost


#basics first!
def bfs(start, goal):
    frontier = deque([start]) #using a double ended queue so that we can take from the 0th index and place on the -1st
    previous = {start: None} #this is a dictionary of states that are next to other states and have been visited
    if start == goal:
        return [start], 0
    while frontier:
        state = frontier.popleft() #get state from top of q

        for adj in adjacent_states(state): #look through adjacent states
            if adj not in previous: #if we havent visted it before
                frontier.append(adj) #add the state to the list to be explored
                previous[adj] = state #set the state we got here from in the prev. dictionary
                if adj == goal:
                    found_path = path(previous, adj)
                    return found_path, pathcost(found_path)


def dfs(start, goal):
    frontier = [start] #regular list here since we just need to take from -1st and add to -1st index each time. Could use deque with same commands but no need to be extra  
    previous = {start: None} #this is a dictionary of states that are next to other states and have been visited
    if start == goal:
        return [start], 0
    while frontier:
        state = frontier.pop()
        for adj in adjacent_states(state):
            if adj not in previous:
                frontier.append(adj) #add the state to the list to be explored
                previous[adj] = state #set the state we got here from in the prev. dictionary
                if adj == goal:
                    found_path = path(previous, adj)
                    return found_path, pathcost(found_path)


#creating a priority queue frontier for UCS and A* ordered by path cost

class PQ:
    def __init__(self, start, cost):
        self.states = {} #keeps track of lowest cost to each state
        self.q = [] #this is the heap queue. is a set of (cost, state) tuples to represent elements on the frontier
        self.add(start, cost) #initialize that baby

    def add(self, state, cost):
        heapq.heappush(self.q, (cost,state)) #heapq is the priority queue algorithm so using it will maintain the heap invariant (each node smaller than children)
        self.states[state] = cost #add and set cost for new state

    def pop(self):
        (cost, state) =  heapq.heappop(self.q)  # get cost of getting to explored state (heappop returns the smallest item from heap, ie the lowest cost)
        self.states.pop(state) #not the same pop function. removing state from frontier
        return(cost, state)

    def replace(self, state, cost): #replace the lowest cost to the next state if we find one
        self.states[state] = cost #replace cost
        for i, (oldcost, oldstate) in enumerate(self.q): #look through the frontier
            if oldstate == state and oldcost > cost: #replace there too
                self.q[i] = (cost, state)
                heapq._siftdown(self.q, 0, i) # now i is posisbly out of order; restore
        return                

def ucs(start, goal):
    frontier = PQ(start, 0)
    previous = {start: None}
    explored = {}
    while frontier:
        s = frontier.pop() 
        cost, state = s[0], s[1]
        if state == goal:
            return path(previous, state), cost
        explored[state] = cost
        states = adjacent_states(state)
        for adj in states:
            newcost = explored[state] + states[adj]
            if (adj not in explored) and (adj not in frontier.states):
                frontier.add(adj, newcost)
                previous[adj] = state
            elif (adj in frontier.states) and (frontier.states[adj] > newcost): #if the cost to the adjacent state is less than previously found
                frontier.replace(adj, newcost)
                previous[adj] = state


def a_star(start, goal, heuristic):
    frontier = PQ(start, 0)
    previous = {start : None}
    explored = {}
    while frontier:
        s = frontier.pop() #get the first state
        if s[1] == goal: #check if it is the goal 
            return (path(previous, s[1]), s[0]) #i was using this to check if the numbers were right
        explored[s[1]] = pathcost(path(previous, s[1])) #append path cost
        adjacent = adjacent_states(s[1]) #grab adjacent states
        for s2 in adjacent: #then look thru em all
            movecost = adjacent[s2] #since is a dictionary
            newcost = explored[s[1]] + movecost + heuristic(s2, goal)
            if (s2 not in explored) and (s2 not in frontier.states):
                frontier.add(s2, newcost)
                previous[s2] = s[1]
            elif (s2[0] in frontier.states) and (frontier.states[s2] > newcost):
                frontier.replace(s2, newcost)
                previous[s2] = s[1]



def heuristic_max(state, goal):
    cols = abs(goal[0] - state[0])
    rows = abs(goal[1] - state[1])
    x1=np.array(state)
    x2=np.array(goal)
    euc = np.sqrt(np.sum((x1-x2)**2))
    return max(cols, rows, euc)


start = (1,15)
print(dfs(start, goal))
print(bfs(start, goal))
print(ucs(start, goal))
print(a_star(start, goal, heuristic_max))

#if instead we had a dict of path costs, we would also pass state and use that instead of states = adjacent_states(state)
