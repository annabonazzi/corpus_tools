#coding=utf8
'''
22/08/2017

# Script to make a network plot. 
Developed from model script on https://www.udacity.com/wiki/creating-network-graphs-with-python

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
graph = []
keyword = "approvisionnement"
folder = "/home/bonz/Documents/Corpus_work/GEothermie2020/collocates/bearbeitet/nouns/"
os.chdir(folder)
files = glob.glob("*/*" + keyword + ".txt")

for file1 in files:
	with open (file1, 'r') as f:
		for line in f:
			graph.append((''.join(file1[0:3].upper()), line.split('\t')[0]))

# Adds edges, collects frequency of each node
freq_dic = {} 
for edge in graph:
	G.add_edge(edge[0], edge[1])
	for word in edge:
		if word in freq_dic:
			freq_dic[word] += 1
		else:
			freq_dic[word] = 1

# Possible network layouts
graph_layout = "spring"
if graph_layout == 'spring':
	graph_pos=nx.spring_layout(G)
elif graph_layout == 'spectral':
	graph_pos=nx.spectral_layout(G)
elif graph_layout == 'random':
	graph_pos=nx.random_layout(G)
elif graph_layout == 'shell':
	graph_pos=nx.shell_layout(G)


# Nodes

# Prepares scales of sizes / colors
color_map = []
size_map = []
fontsize_map = []

for word in freq_dic:
	if freq_dic[word] > 2:
		color_map.append('red')
		size_map.append(1600)
	elif freq_dic[word] <=2 and freq_dic[word] > 1:
		color_map.append('orange')
		size_map.append(1200)
	else: 
		color_map.append('yellow')
		size_map.append(800)

nx.draw_networkx_nodes(G, graph_pos, node_size=size_map, alpha=0.3, node_color =color_map)

# Edges
width_map = []
for tup in graph:
	width_map.append(int(1 + freq_dic[tup[1]] * 1))
  
nx.draw_networkx_edges(G, graph_pos, width=width_map, alpha=0.3, edge_color="#8e7e8b")

# Node labels
txtcolor = "#3c3838"
txtfont = "DejaVu Sans"
nx.draw_networkx_labels(G, graph_pos,font_size=13, fontname=txtfont, color=txtcolor)

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

# Title
plt.title('"approvisionnement"\n\nKollokatoren nach Klasse', color=txtcolor, fontname = txtfont, fontsize = '16')

# Legend
leg = plt.legend(loc='best', labels = [" PAB: industry\n PBV: media\n PFU: policy makers"], frameon=False)#, facecolor = 'r', edgecolor = 'b' # Don't have to unless I want to change them

# Changes all legend 
for text in leg.get_texts():
	text.set_fontsize(12)
	text.set_fontname(txtfont)
	text.set_color(txtcolor)
	
# Shows graph
plt.show()

#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
