import networkx as nx
import matplotlib.pyplot as plt
#import pygame
# Create the triangular lattice graph (3 rows, 5 columns)
class board():
    def __init__(self):
        self.dim = self.select_dimention()
        self.board = self.create_base_board()


    def select_dimention(self):
        option = input(f'Please select the number of the game size that you want to play. \n '
                       f'1. Small [4x4 game]\n '
                       f'2. Meduim [7x7 game]\n '
                       f'3. Large [10x10 game]')
        if option == 1:
            return [4, 4]
        elif option == 2:
            return [7, 7]
        elif option == 3:
            return [10, 10]
        else:
            print(f' You have chosen an invalid input. '
                  f'Please enter the number corresponding to the size of game you want to play. \ni.e., 1, 2, or 3.')
            return self.select_dimention()
    def create_base_board(self):
        regular_lattice = nx.grid_2d_graph(10, 10)
        pos = {(x, y): (y, -x) for x, y in regular_lattice.nodes()}
        nx.draw_networkx_nodes(regular_lattice, pos=pos, with_labels=True, node_color='skyblue', node_size=250, font_size=12)
        plt.title("Regular 2d")
        plt.figure(dpi=500)
        plt.show()
        return nx, pos



