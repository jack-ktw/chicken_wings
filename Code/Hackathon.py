import sys
import os

print sys.version

world = '2b-prime'
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
    adjacency_list = [[] for i in xrange(node_count + 1)]
    degree_list = [0 for i in xrange(node_count + 1)]
    edge_count = 0

    with open(edge_file_path, 'r') as node_f:
        for line in node_f:
            fields = line.split()
            if fields[0] == 'e':
                node1 = int(fields[1])
                node2 = int(fields[2])
                adjacency_list[node1].append(node2)
                adjacency_list[node2].append(node1)
                degree_list[node1] += 1
                degree_list[node2] += 1
                edge_count += 1
    print edge_count
    return (adjacency_list, degree_list, edge_count)

adjacency_list, degree_list, edge_count = parse_edge_file(edge_file_path, node_count)
adjacency_list = [list(a) for a in zip(adjacency_list, degree_list)]
from operator import itemgetter
max_degree = max(adjacency_list, key=itemgetter(1))[1]

D_list = [[] for i in xrange(max_degree + 1)]
for index, node in enumerate(adjacency_list):
    D_list[node[1]].append(index)
print len(D_list)


from collections import deque
from bisect import bisect_left
from pprint import pprint
degeneracy_list = deque()
k = 0
from itertools import takewhile
def f(l): return len([x for x in takewhile(lambda x: not x[1], enumerate(l))])
for i in xrange(len(adjacency_list)):
    nonempty_i = f(D_list)
    k = max(k, nonempty_i)
    v = D_list[nonempty_i].pop(0)
    degeneracy_list.appendleft(v)
    adjacency_list[v][1] = -1
    
    neigbours = adjacency_list[v][0]

    for neigbour_index in neigbours:
        D_index = adjacency_list[neigbour_index][1]

        if D_index > -1:
            pop_index = bisect_left(D_list[D_index], neigbour_index)
            D_list[D_index].pop(pop_index)
            adjacency_list[neigbour_index][1] -= 1
            insert_index = bisect_left(D_list[D_index - 1], neigbour_index)
            D_list[D_index - 1].insert(insert_index, neigbour_index)

print len(degeneracy_list)
print len(set(degeneracy_list))

def BronKerboshc(R, P, X):
    if (not P and not X):
        print len(R)
    while P:
        v = P.pop()
        X.add(v)
        BronKerboshc(R.union(set([v])), P.intersection(set(adjacency_list[v][0])), X.intersection(set(adjacency_list[v][0])))

def getPivot(P, X):
    # need to maximize P INTERCEPT N(u)
    rand_u = P.union(X).pop()
    return rand_u
    
def BronKerboshcPivot(R, P, X, size):
    if (not P and not X):
        if len(R) > size[0]:
            size[0] = len(R)
        print len(R)
        return
    u = getPivot(P, X)
    nu = set(adjacency_list[u][0])
    tmp_P = set()
    while P:
        v = P.pop()
        if not v in nu:
            print "called:"
            BronKerboshcPivot2(R.union(set([v])), P.union(tmp_P).union(set([v])).intersection(set(adjacency_list[v][0])), X.intersection(set(adjacency_list[v][0])), [0], size)
            X.add(v)
        else:
            tmp_P.add(v)

def BronKerboshcPivot2(R, P, X, done, size):
    if len(R) + len(P) < size[0]:
        return
    if (not P and not X):
        print len(R)
        done[0] = 1
        return
    u = getPivot(P, X)
    nu = set(adjacency_list[u][0])
    tmp_P = set()
    while P:
        v = P.pop()
        if not v in nu:
            BronKerboshcPivot2(R.union(set([v])), P.union(tmp_P).union(set([v])).intersection(set(adjacency_list[v][0])), X.intersection(set(adjacency_list[v][0])), done, size)
            X.add(v)
        else:
            tmp_P.add(v)



# In[ ]:

import profile
sys.setrecursionlimit(3000)
from itertools import islice
i = 0
while i < len(degeneracy_list):
    v = degeneracy_list[i]
    post_set = set(islice(degeneracy_list, i+1, None))
    pre_set = set(islice(degeneracy_list, i))
    P = set(adjacency_list[v][0]).intersection(post_set)
    X = set(adjacency_list[v][0]).intersection(pre_set)
    BronKerboshcPivot(set([v]), P, X, [0])
    # profile.run('BronKerboshcPivot(set([v]), P, X)')
    i += 1


