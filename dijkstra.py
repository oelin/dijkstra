from math import *
from random import random


# graph implementation with nested hash tables
# insertion: O(1)
# lookup: O(1)
# space: ~O(k), k = |nodes| + |edges|

class edge:
    def __init__(self, start, end, cost):
        self.start = start
        self.end = end
        self.cost = cost


    def __repr__(self):
        return f'edge({self.cost})'


class node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.edges = {}


    def addEdge(self, key, node, cost):
        self.edges[key] = edge(self, node, cost)


    def __repr__(self):
        return f'node({self.value})'


class nodelist:
    def __init__(self):
        self.nodes = {}


    def insert(self, key, value):
        self.nodes[key] = node(key, value)


    def connect(self, start, end, cost):
        assert self.nodes[start]
        assert self.nodes[end]

        self.nodes[start].addEdge(end, self.nodes[end], cost)


    def connectBoth(self, start, end, cost):
        self.connect(start, end, cost)
        self.connect(end, start, cost)


    def edges(self, key):
        return self.nodes[key].edges
    

    def value(self, key):
      return self.nodes.get(key).value


    def __len__(self):
        return len(self.nodes)


    def __repr__(self):
        return f'nodelist({self.nodes})'
        


# priority queue implementation with a min-heap
# insert: O(log n) worst
# lookup: O(n)
# space: O(n)

class minheap:
    def __init__(self):
        self.contents = []


    def swap(self, i, j):
        self.contents[i], self.contents[j] = self.contents[j], self.contents[i]


    def parent(self, i):
        if (i == 0): return
        return floor((i - 1) / 2)


    def left(self, i):
        return 2 * i + 1


    def right(self, i):
        return 2 * (i + 1)
        

    def sift(self, i):
        while (1):
            parent = self.parent(i)
            
            if (parent is None or self.contents[i] >= self.contents[parent]):
                break

            self.swap(i, parent)
            i = parent


    def fix(self, i):
        l = self.left(i)
        r = self.right(i)
        smallest = i

        if (l < self.last() and self.contents[l] < self.contents[i]):
            smallest = l

        if (r < self.last() and self.contents[r] < self.contents[smallest]):
            smallest = r

        if (smallest != i):
            self.swap(i, smallest)
            self.fix(smallest)
            

    def last(self):
        return len(self.contents) -1


    def insert(self, key):
        self.contents.append(key)
        self.sift(self.last())


    def delete(self, key):
        i = self.contents.index(key)
        
        self.swap(i, self.last())
        self.contents.pop()
        self.fix(i)


    def deleteMin(self):
        key = self.contents[0]
        self.delete(key)

        return key


    def lower(self, key, new):
        i = self.contents.index(key)
        self.contents[i] = new
        self.sift(i)
        
        
    def __repr__(self):
        return str(self.contents)



class pq:
    def __init__(self):
        self.heap = minheap()
        self.values = {}


    def queue(self, key, value):
        self.heap.insert(key)
        self.values[key] = value


    def dequeue(self):
        key = self.heap.deleteMin()
        value = self.values.pop(key)

        return value


    def findKey(self, value):        
        keys = list(self.values)
        values = list(self.values.values())

        if value in values:
            return keys[values.index(value)]


    def lower(self, key, new):
        self.heap.lower(key, new)
        self.values[new] = self.values.pop(key)


    def __len__(self):
        return len(self.values)



# Dijkstra's algorithm (with a min-heap)
# runtime: O(e log n), e = |edges|, n = |nodes|

class auxlist:
    def __init__(self, nodes):
        self.edges = { node: None for node in nodes.nodes }
        self.dists = { node: float('inf') for node in nodes.nodes }


    def getEdge(self, key):
        return self.edges[key]


    def getDist(self, key):
        return self.dists[key]


    def setEdge(self, key, value):
        self.edges[key] = value


    def setDist(self, key, value):
        self.dists[key] = value


    def relax(self, start, end, edge):
        sum = self.getDist(start) + edge.cost
        
        if (sum < self.getDist(end)):
            self.setDist(end, sum)
            self.setEdge(end, edge)

            return True


    def path(self, end):
        current = end

        while (1):
            yield current
            
            edge = self.getEdge(current)
            if (edge == None): break
            
            current = edge.start.key
        


def dijkstra(nodes, source):
    
    aux = auxlist(nodes)
    aux.setDist(source, 0)
    q = pq()
    q.queue(0, source)

    while (len(q)):
        start = q.dequeue()

        for end, edge in nodes.edges(start).items():
            # relax the edge

            if (aux.relax(start, end, edge)):
                key = q.findKey(end)
                
                if (key):
                    q.lower(key, aux.getDist(end))

                else:
                    q.queue(aux.getDist(end), end)

    return aux
