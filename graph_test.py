import json
import pprint as pp
from data.fees import *

c = 0
class Vertex(object):
    def __init__(self,symbol,address,decimals):
        self.symbol = symbol
        self.address = address
        self.decimals = decimals

class Edge(object):
    def __init__(self,pair_address,data:dict):
        self.pair_address = pair_address
        self.pair_symbol = data['pair_symbol']
        self.u = Vertex(data['token0_symbol'],data['token0_address'],data['token0_decimals'])
        self.v = Vertex(data['token1_symbol'],data['token1_address'],data['token1_decimals'])
        self.reserve0 = data['reserve0']
        self.reserve1 = data['reserve1']
        self.exchange = data['exchange']
        self.txn_fee = txn_cost[self.exchange]

    @property
    def reverse(self):
        self.u,self.v = self.v,self.u
        self.reserve0,self.reserve1 = self.reserve1,self.reserve0
        tmp = self.pair_symbol.split('/')
        self.pair_symbol = tmp[1]+'/'+tmp[0]

    def modify_reserves(self,r0,r1):
        self.reserve0 = r0
        self.reserve1 = r1

class GenerateGraph(object):
    def __init__(self,json_file):
        with open(json_file,'r') as f:
            self.data = json.load(f)
        self.vertices = {}
        self.edges = {}
        self.neighbours = {}
        self.generate_vertices()
        self.generate_edges()

    def generate_vertices(self):
        for i in self.data:
            v0 = Vertex(self.data[i]['token0_symbol'],self.data[i]['token0_address'],
            self.data[i]['token0_decimals'])
            v1 = Vertex(self.data[i]['token1_symbol'],self.data[i]['token1_address'],
            self.data[i]['token1_decimals'])
            self.vertices.update({v0.symbol:v0})
            self.vertices.update({v1.symbol:v1})
            if v0.symbol not in self.neighbours:
                self.neighbours[v0.symbol]=set()
            if v1.symbol not in self.neighbours:
                self.neighbours[v1.symbol]=set()
            self.neighbours[v0.symbol].add(v1.symbol)
            self.neighbours[v1.symbol].add(v0.symbol)
            
    def generate_edges(self):
        for i in self.data:
            e = Edge(i,self.data[i])
            self.edges.update({(e.u.symbol,e.v.symbol,e.exchange):e})
            self.edges.update({(e.v.symbol,e.u.symbol,e.exchange):e.reverse})

class CurrencyGraph(GenerateGraph):
    def __init__(self,path):
        super().__init__(path)
    
    def addvertex(self,v):
        if v not in self.neighbours:
            self.neighbours[v] = set()

    def addedge(self,u,v):
        self.addvertex(u)
        self.addvertex(v)
        self.edges.add(frozenset((u,v)))
        self.neighbours[u].add(v)
        self.neighbours[v].add(u)

    def deg(self,v):
        return len(self.neighbours[v])

    def neighbours(self,v):
        return self.neighbours[v]    

    @property
    def edges_count(self):
        return len(self.edges)

    @property
    def vertices_count(self):
        return len(self.neighbours)


    
    def printAllPathsUtil(self, u, d, visited, path):
        global c
        visited[u]= True
        path.append(u)
        if u == d:
            c+=1
            print(c)
        else:
            for i in self.neighbours[u]:
                if visited[i]== False:
                    self.printAllPathsUtil(i, d, visited, path)
        path.pop()
        visited[u]= False
    
    def printAllPaths(self, s):
        for j in self.neighbours['WETH']:
            visited ={}
            for i in self.vertices:
                visited.update({i:False})
            path = []
            self.printAllPathsUtil(s, j, visited, path)

    def sorted_arblist(self,source='WETH'):
        pass

# path = './data/cmn_unisushi_pairs.json'
# graph = CurrencyGraph(path)
# # pp.pprint(graph.neighbours)
# graph.printAllPaths('WETH')


from collections import defaultdict

class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.ROW = len(graph)
        # self.COL = len(gr[0])
    '''Returns true if there is a path from source 's' to sink 't' in
    residual graph. Also fills parent[] to store the path '''
    def BFS(self, s, t, parent):
        visited = [False]*(self.ROW)
        queue = []
        queue.append(s)
        visited[s] = True
 
        while queue:

            u = queue.pop(0)

            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True

        return False
             
     
    # Returns tne maximum flow from s to t in the given graph
    def FordFulkerson(self, source, sink):

        parent = [-1]*(self.ROW)
        max_flow = 0

        while self.BFS(source, sink, parent) :

            path_flow = float("Inf")
            s = sink
            while(s !=  source):
                path_flow = min (path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow +=  path_flow
            v = sink
            while(v !=  source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
 
        return max_flow

graph = [[0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]]
g = Graph(graph)
source = 0; sink = 5
print ("The maximum possible flow is %d " % g.FordFulkerson(source, sink))