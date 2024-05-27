print("\n[week12] Brand & Bound Pruning: 0-1 Knapsack Problem")

class Queue:
    def __init__(self):         # initialization
        self.items = []
    
    def isEmpty(self):          # check emptiness
        return len(self.items) == 0
    
    def enqueue(self, item):    # insert new item
        self.items.insert(0, item)
    
    def dequeue(self):          # delete and return the item
        if (not self.isEmpty()):
            return self.items.pop()
        else:
            raise IndexError("Queue is empty")

    def size(self):             # size of the queue
        return len(self.items)

class Node:
    def __init__(self, level, weight, profit, include):
        self.level = level
        self.weight = weight
        self.profit = profit
        self.include = include

def compBound(u):
    if (u.weight >= W): # exceed the limit
        return 0
    else:
        result = u.profit           # total profit of node 'u'
        j = u.level                 # level of node 'u'
        total_weight = u.weight     # total weight of node 'u'

        while ((j < n) and (total_weight + w[j] <= W)):
            total_weight += w[j]    # add weight
            result += p[j]          # add profit
            j += 1                  # next item

        if (j < n):                 # for remaining capacity
            result += (W - total_weight) * p[j] / w[j]

        return result


def kp_BFS():   # Breadth-First Search
    global maxProfit, bestset, numNodes, maxQueueSize

    q = Queue()                 # initialize queue
    v = Node(0, 0, 0, [0] * n)  # initial node
    q.enqueue(v)                # enqueue initial node to queue  
    numNodes += 1               # increment the number of nodes generated

    while (not q.isEmpty()):    # repeat until queue is not empty
        v = q.dequeue()         # delete and return (pop)

        if (v.level < n):       # current node level vs. number of items
            # generate (first) child node 'u'
            u = Node(v.level + 1, v.weight + w[v.level], v.profit + p[v.level], v.include[:])
            u.include[v.level] = 1

            if ((u.weight <= W) and (u.profit > maxProfit)):    # update
                maxProfit = u.profit
                bestset = u.include[:]

            if (compBound(u) > maxProfit):  # higher bound
                q.enqueue(u)                # enqueue the node to queue
                numNodes += 1

            # not adding item -> move to next level
            # generate second child node
            u = Node(v.level + 1, v.weight, v.profit, v.include[:])
            if (compBound(u) > maxProfit):
                q.enqueue(u)
                numNodes += 1

        maxQueueSize = max(maxQueueSize, q.size())  # update max size of the queue

n = 4                  # number of items
W = 6                  # capacity of knapsack
p = [12, 12, 18, 2]    # profit list
w = [2, 3, 6, 1]       # weight list

include = [0] * n
maxProfit = 0
bestset = n * [0]
numNodes = 0
maxQueueSize = 0

print(f"n = {n}\nW = {W}\np = {p}\nw = {w}\n")

print("<1> Branch & Bound Pruning: Breadth-First Search")
kp_BFS()
print(f"Best Set: {bestset}")
print(f"Max Profit: {maxProfit}\n")
print(f"(1) Number of Total Nodes Generated: {numNodes}")
print(f"(2) Maximum Queue Size: {maxQueueSize}")
print()
print()

print("<2> Branch & Bound Pruning: Best-First Search >")

class PriorityQueue:
    def __init__(self):  # initialize
        self.elements = []

    def isEmpty(self):  # check emptiness
        return len(self.elements) == 0

    def put(self, item):  # insert new item
        self.elements.append(item)
        self.elements.sort(key=lambda x: x[0])  # sorting -> priority queue

    def get(self):  # delete and return the 'first' item
        if not self.isEmpty():
            return self.elements.pop(0)
        else:
            raise IndexError("Priority Queue is empty")

    def size(self):  # size of the priority queue
        return len(self.elements)

class Node2:
    def __init__(self, level, weight, profit, bound, include):
        self.level = level
        self.weight = weight
        self.profit = profit
        self.bound = bound
        self.include = include

def compBound2(u):      # compute 'bound' for current node 'u'
    if (u.weight >= W): # exceed the limit
        return 0
    else:
        result = u.profit           # total profit of node 'u'
        j = u.level                 # level of node 'u'
        total_weight = u.weight     # total weight of node 'u'

        while ((j < n) and (total_weight + w[j] <= W)):
            total_weight += w[j]    # add weight
            result += p[j]          # add profit
            j += 1                  # next item

        if (j < n):                 # for remaining capacity
            result += (W - total_weight) * p[j] / w[j]

        # return 'negative' of result
        # highest bound -> highest priority (min-heap)
        return -result

def kp_Best_FS():   # Best-First Search
    global maxProfit, bestset, numNodes, maxQueueSize
    numNodes = 0
    maxQueueSize = 0

    temp = [0] * n                  # temporary list (include or not)
    v = Node2(-1, 0, 0, 0.0, temp)  #level, weight, profit, bound, include
    q = PriorityQueue()             # priority queue - sorted by 'bound'
    q.put((v.bound, v))             # use 'bound' -> insert (min-heap) 

    while (not q.isEmpty()):        # repeat until priority queue is not empty 
        _, v = q.get()              # node with highest priority (lowest bound)
        numNodes += 1
        
        if (v.level == n - 1):      # check whether it is the last level
            continue
        
        # generate child node 'u1'
        # level, weight, profit, bound, include
        u1 = Node2(v.level + 1,
                   v.weight + w[v.level + 1],
                   v.profit + p[v.level + 1],
                   compBound2(Node2(v.level + 1, v.weight + w[v.level + 1], v.profit + p[v.level + 1], 0.0, v.include)),
                   v.include[:])
        u1.include[v.level + 1] = 1     # update 'include'
        
        u2 = Node2(v.level + 1, v.weight, v.profit, compBound2(Node2(v.level + 1, v.weight, v.profit, 0.0, v.include)), v.include[:])
        
        if (u1.weight <= W) and (u1.profit > maxProfit):    # update
            maxProfit = u1.profit
            bestset = u1.include[:]
        
        if (u1.bound < maxProfit):  # lower bound
            q.put((u1.bound, u1))   # insert the node to priority queue
            maxQueueSize = max(maxQueueSize, q.size())  # update max size of the queue
        
        if (u2.bound < maxProfit):  # do the same (second child node)
            q.put((u2.bound, u2))
            maxQueueSize = max(maxQueueSize, q.size())  # update max size of the queue

# testing data (n, W, p, w)
# n = 4
# W = 16
# p = [40, 30, 50, 10]
# w = [2, 5, 10, 5]

include = [0] * n
maxProfit = 0
bestset = n * [0]
numNodes = 0
maxQueueSize = 0

kp_Best_FS()
print(f"Best Set: {bestset}")
print(f"Max Profit: {maxProfit}\n")
print(f"(1) Number of Total Nodes Generated: {numNodes}")
print(f"(2) Maximum Priority Queue Size: {maxQueueSize}")
print()