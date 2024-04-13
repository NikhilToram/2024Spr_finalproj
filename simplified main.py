import networkx as nx
import matplotlib.pyplot as plt
#import pygame
# Create the triangular lattice graph (3 rows, 5 columns)
regular_lattice = nx.grid_2d_graph(10, 10)
pos = {(x, y): (y, -x) for x, y in regular_lattice.nodes()}
nx.draw(regular_lattice, pos=pos, with_labels=True, node_color='skyblue', node_size=250, font_size=12)
plt.title("Regular 2d")
plt.figure(dpi=500)
plt.show()



