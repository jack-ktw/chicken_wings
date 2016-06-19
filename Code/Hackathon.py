import sys
print sys.version


# In[22]:

import os


# In[23]:

world = '2b-prime'
node_file_path = os.getcwd() + "\\input\\world " + world + "\\nodes_world_" + world + ".txt"
node_count = 0

print_limit = 10
print_index = 0
print node_file_path
with open(node_file_path, 'r') as node_f:
    for line in node_f:
        if print_index < print_limit:
            print line
            print_index += 1
        node_count += 1
print node_count


# In[24]:

edge_file_path = os.getcwd() + "\\input\\world " + world + "\\edges_world_" + world + ".clq"
adjacency_list = [[[], 0] for i in xrange(node_count + 1)]
edge_count = 0

print_limit = 10
print_index = 0
print node_file_path

prev_node = -1
with open(edge_file_path, 'r') as node_f:
    for line in node_f:
        if print_index < print_limit:
            print line
            print_index += 1
        fields = line.split()
        if fields[0] == 'e':
            node1 = int(fields[1])
            node2 = int(fields[2])
            method = fields[3]
            adjacency_list[node1][0].append(node2)
            adjacency_list[node2][0].append(node1)
            adjacency_list[node1][1] += 1
            adjacency_list[node2][1] += 1
            edge_count += 1
print edge_count
        


# print adjacency_list
#     

# In[25]:

from operator import itemgetter
max_degree = max(adjacency_list, key=itemgetter(1))[1]


# In[26]:

D_list = [[] for i in xrange(max_degree + 1)]
for index, node in enumerate(adjacency_list):
    D_list[node[1]].append(index)
print len(D_list)


# In[27]:

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


# In[28]:

print len(degeneracy_list)
print len(set(degeneracy_list))


# BronKerbosch1(R, P, X):
#        if P and X are both empty:
#            report R as a maximal clique
#        for each vertex v in P:
#            BronKerbosch1(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
#            P := P \ {v}
#            X := X ⋃ {v}

# In[ ]:




# In[ ]:

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


