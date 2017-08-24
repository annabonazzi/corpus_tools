#coding=utf8
'''
22/08/2017


# Script to make a network plot. Model script from https://www.udacity.com/wiki/creating-network-graphs-with-python

'''
# To time the script
from datetime import datetime
startTime = datetime.now()

import os, glob, re

#--------------------------
import networkx as nx
import matplotlib.pyplot as plt

# Creates empty networkx graph
G=nx.Graph()

# Prepares content as list of tuples
graph = [("géothermie", "prix"), ("géothermie", "sous-sol"), ("géothermie", "eau"), ("électricité", "eau"), ("géothermie", "électricité")]#, (4, 5), (4, 8), (1, 6), (3, 7), (5, 9), (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]

# Collects frequency of each node
freq_dic = {} 

# add edges
for edge in graph:
	G.add_edge(edge[0], edge[1])
	for word in edge:
		if word in freq_dic:
			freq_dic[word] += 1
		else:
			freq_dic[word] = 1

color_map = []
for word in freq_dic:
    if freq_dic[word] > 2:
        color_map.append('red')
    elif freq_dic[word] <=2 and freq_dic[word] > 1:
        color_map.append('orange')
    else: color_map.append('yellow') 

size_map = []
for word in freq_dic:
    if freq_dic[word] > 2:
        size_map.append(1600)
    elif freq_dic[word] <=2 and freq_dic[word] > 1:
        size_map.append(1200)
    else: size_map.append(800)
       
# these are different layouts for the network you may try
graph_layout = "shell"
if graph_layout == 'spring':
  graph_pos=nx.spring_layout(G)
elif graph_layout == 'spectral':
  graph_pos=nx.spectral_layout(G)
elif graph_layout == 'random':
  graph_pos=nx.random_layout(G)
elif graph_layout == 'shell': # shell seems to work best
  graph_pos=nx.shell_layout(G)

# draw graph

# Nodes
nx.draw_networkx_nodes(G, graph_pos, node_size=size_map, alpha=0.3, node_color =color_map)
# Edges
nx.draw_networkx_edges(G, graph_pos, width=1, alpha=0.3, edge_color="blue")
# Node labels
nx.draw_networkx_labels(G, graph_pos,font_size=12, font_family="sans-serif")

# Edge labels
'''
labels = None
# or 
#labels = map(chr, range(65, 65+len(graph))) # To name the labels with characters from the character list

if labels is None:
	labels = range(len(graph))

edge_labels = dict(zip(graph, labels))
nx.draw_networkx_edge_labels(G, graph_pos, label_pos=0.3, edge_labels=edge_labels)
'''
# show graph
plt.show()



'''
# Simple polygon-like. How to label knots?
def draw_graph(graph):

    # extract nodes from graph
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph
    G=nx.Graph()

    # add nodes
    for node in nodes:
        G.add_node(node)

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # draw graph
    pos = nx.shell_layout(G)
    nx.draw(G, pos)

    # show graph
    plt.show()

# draw example
graph = [(20, 21),(21, 22),(22, 23), (23, 24),(24, 25), (25, 20)]
draw_graph(graph)
'''

#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
