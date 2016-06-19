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