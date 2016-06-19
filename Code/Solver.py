import os
import sys
import time
from bisect import bisect_left
from collections import deque
from itertools import islice
from itertools import takewhile

sys.setrecursionlimit(3000)

class Solver:

    def __init__(self, node_file_path, edge_file_path, result_path):
        self.node_file_path = node_file_path
        self.edge_file_path = edge_file_path
        self.result_path = result_path

        self.node_count = 0
        self.com_type_L = None
        self.adjacency_list = None
        self.degree_list = None
        self.degeneracy_list = None

        self.parse_node_file(node_file_path)
        self.parse_edge_file(edge_file_path, self.node_count)

        self.gen_degeneracy_list(self.degree_list, self.adjacency_list)

        self.solution = set()
        self.solution_size = 0


    def parse_node_file(self, node_file_path):
        node_count = 0
        with open(node_file_path, 'r') as node_f:
            for line in node_f:
                node_count += 1

        com_type_L = [0] * node_count
        with open(node_file_path, 'r') as node_f:
            for line in node_f:
                id0, com_type = line.split()
                com_type_L[int(id0)] = com_type
        self.node_count = node_count
        self.com_type_L = com_type_L

    def parse_edge_file(self, edge_file_path, node_count):
        adjacency_list = [set() for i in xrange(node_count + 1)]
        degree_list = [0 for i in xrange(node_count + 1)]
        edge_count = 0

        with open(edge_file_path, 'r') as node_f:
            for line in node_f:
                fields = line.split()
                if fields[0] == 'e':
                    node1 = int(fields[1])
                    node2 = int(fields[2])
                    adjacency_list[node1].add(node2)
                    adjacency_list[node2].add(node1)
                    degree_list[node1] += 1
                    degree_list[node2] += 1
        self.adjacency_list = adjacency_list
        self.degree_list = degree_list

    def gen_degeneracy_list(self, degree_list, adjacency_list):
        max_degree = max(degree_list)
        D_list = [[] for i in xrange(max_degree + 1)]
        for index, degree in enumerate(degree_list):
            D_list[degree].append(index)
        # print len(D_list)

        dynamic_degree_L = degree_list[:]
        degeneracy_list = deque()
        k = 0

        def f(l): return len([x for x in takewhile(lambda x: not x[1], enumerate(l))])
        for i in xrange(len(adjacency_list)):
            nonempty_i = f(D_list)
            k = max(k, nonempty_i)
            v = D_list[nonempty_i].pop(0)
            degeneracy_list.appendleft(v)
            dynamic_degree_L[v] = -1

            neighbours = adjacency_list[v]

            for neighbour_index in neighbours:
                D_index = dynamic_degree_L[neighbour_index]

                if D_index > -1:
                    pop_index = bisect_left(D_list[D_index], neighbour_index)
                    D_list[D_index].pop(pop_index)
                    dynamic_degree_L[neighbour_index] -= 1
                    insert_index = bisect_left(D_list[D_index - 1], neighbour_index)
                    D_list[D_index - 1].insert(insert_index, neighbour_index)
        self.degeneracy_list = degeneracy_list

    def getPivot(self, P, X):
        # need to maximize P INTERCEPT N(u)
        rand_u = max(P.union(X), key=lambda x : self.degree_list[x])
        return rand_u

    def BronKerboshcPivot2(self, R, P, X, done):
        if (not P and not X):
            if len(R) > self.solution_size:
                self.solution_size = len(R)
                self.solution = R
            print len(R)
            done[0] = 1
            return

        if done[0]:
            return
        if len(R) + len(P) < self.solution_size:
            return

        u = self.getPivot(P, X)
        nu = set(self.adjacency_list[u])
        tmp_P = set()
        while P:
            v = P.pop()
            degree = self.degree_list[v]
            if degree > self.solution_size - 1 and not done[0]:
                if v not in nu:
                    self.BronKerboshcPivot2(R.union(set([v])), P.union(tmp_P).union(set([v])).intersection(self.adjacency_list[v]), X.intersection(self.adjacency_list[v]), done)
                    X.add(v)
                else:
                    tmp_P.add(v)

    def BronKerboshcDegeneracy(self):
        i = 0
        while i < len(self.degeneracy_list):
            v = self.degeneracy_list[i]
            post_set = set(islice(self.degeneracy_list, i+1, None))
            pre_set = set(islice(self.degeneracy_list, i))
            P = self.adjacency_list[v].intersection(post_set)
            X = self.adjacency_list[v].intersection(pre_set)
            degree = self.degree_list[v]
            if degree > self.solution_size - 1:
                # print "root called: ", degree
                self.BronKerboshcPivot2(set([v]), P, X, [0])
            i += 1

        print "Solution Size: ", self.solution_size
        with open(self.result_path, 'w') as f:
            f.writelines([str(x) + "\n" for x in sorted(self.solution)])

if __name__ == '__main__':
    print "Started - Time: ", time.ctime()
    world = '2A'
    node_file_path = os.getcwd() + "\\input\\world " + world + "\\nodes_world_" + world + ".txt"
    edge_file_path = os.getcwd() + "\\input\\world " + world + "\\edges_world_" + world + ".clq"
    result_path = os.getcwd() + "\\result.txt"
    solver = Solver(node_file_path, edge_file_path, result_path)
    print "Initialized - Time: ", time.ctime()
    solver.BronKerboshcDegeneracy()
    finish_time = time.ctime()
    print "Finished - Time: ", time.ctime()
