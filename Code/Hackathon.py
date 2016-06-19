import sys
import os
import time
from collections import deque
from bisect import bisect_left
from itertools import takewhile

cur_time = time.ctime()
world = '2A'
node_file_path = os.getcwd() + "\\input\\world " + world + "\\nodes_world_" + world + ".txt"

print "file path: ", node_file_path

# def parse_node_file(node_file_path):
#     node_count = 0
#     with open(node_file_path, 'r') as node_f:
#         for line in node_f:
#             node_count += 1
#
#     com_type_L = [0] * node_count
#     with open(node_file_path, 'r') as node_f:
#         for line in node_f:
#             id0, com_type = line.split()
#             com_type_L[int(id0)] = com_type
#     return (node_count, com_type_L)

def count_node(node_file_path):
    node_count = 0
    with open(node_file_path, 'r') as node_f:
        for line in node_f:
            node_count += 1
    return node_count


node_count= count_node(node_file_path)

edge_file_path = os.getcwd() + "\\input\\world " + world + "\\edges_world_" + world + ".clq"

print "node file path: " + node_file_path

def parse_edge_file(edge_file_path, node_count):
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
                edge_count += 1
    print edge_count
    return (adjacency_list, degree_list, edge_count)

adjacency_list, degree_list, edge_count = parse_edge_file(edge_file_path, node_count)
######################

def get_degeneracy_list(degree_list, adjacency_list):
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
    return degeneracy_list

degeneracy_list = get_degeneracy_list(degree_list, adjacency_list)

print len(degeneracy_list)

def BronKerboshc(R, P, X):
    if (not P and not X):
        print len(R)
    while P:
        v = P.pop()
        X.add(v)
        BronKerboshc(R.union(set([v])), P.intersection(adjacency_list[v]), X.intersection(adjacency_list[v]))

def getPivot(P, X):
    # need to maximize P INTERCEPT N(u)
    rand_u = max(P.union(X), key=lambda x : degree_list[x])
    return rand_u
    
def BronKerboshcPivot(R, P, X, done, size, result, adj, deg):
    adjacency_list = adj[0]
    if (not P and not X):
        if len(R) > size[0]:
            size[0] = len(R)
            result[0] = R

        print len(R)
        done[0] = 1
        return

    if done[0]:
        return

    u = getPivot(P, X)
    nu = set(adjacency_list[u])
    tmp_P = set()
    while P:
        v = P.pop()
        degree = degree_list[v]
        if degree > size[0] - 1 and not done[0]:
            if v not in nu:
                # print "called: ", degree, size[0]
                BronKerboshcPivot2(R.union(set([v])), P.union(tmp_P).union(set([v])).intersection(adjacency_list[v]), X.intersection(adjacency_list[v]), done, size, result, adj, deg)
                X.add(v)
            else:
                tmp_P.add(v)

def BronKerboshcPivot2(R, P, X, done, size, result, adj, deg):
    adjacency_list = adj[0]
    if (not P and not X):
        if len(R) > size[0]:
            size[0] = len(R)
            result[0] = R
        print len(R)
        done[0] = 1
        return

    if done[0]:
        return
    if len(R) + len(P) < size[0]:
        return

    u = getPivot(P, X)
    nu = set(adjacency_list[u])
    tmp_P = set()
    while P:
        v = P.pop()
        degree = degree_list[v]
        if degree > size[0] - 1 and not done[0]:
            if not v in nu:
                BronKerboshcPivot2(R.union(set([v])), P.union(tmp_P).union(set([v])).intersection(adjacency_list[v]), X.intersection(adjacency_list[v]), done, size, result, adj, deg)
                X.add(v)
            else:
                tmp_P.add(v)



# In[ ]:

import profile
sys.setrecursionlimit(3000)
from itertools import islice
i = 0
size = [0]
result = [set()]
while i < len(degeneracy_list):
    v = degeneracy_list[i]
    post_set = set(islice(degeneracy_list, i+1, None))
    pre_set = set(islice(degeneracy_list, i))
    P = adjacency_list[v].intersection(post_set)
    X = adjacency_list[v].intersection(pre_set)
    degree = degree_list[v]
    if degree > size[0] - 1:
        # print "root called: ", degree
        BronKerboshcPivot(set([v]), P, X, [0], size, result, [adjacency_list], [degree_list])
    # profile.run('BronKerboshcPivot(set([v]), P, X)')
    i += 1
print result

result_path = os.getcwd() + "\\result.txt"

with open(result_path, 'w') as f:
    f.writelines([str(x) + "\n" for x in sorted(result[0])])

finish_time = time.ctime()
print finish_time
print cur_time
