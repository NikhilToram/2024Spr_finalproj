import networkx as nx
import matplotlib.pyplot as plt
#import pygame
# Create the triangular lattice graph (3 rows, 5 columns)


class Board:
    def __init__(self):
        self.dim = self.select_dimention()
        self.board, self.positions = self.create_base_board()
        self.legal_moves = [tuple(sorted([edge[0], edge[1]])) for edge in nx.edges(self.board)]

    def select_dimention(self):
        option = input(f'Please select the number of the game size that you want to play. \n '
                       f'1. Small [4x4 game]\n '
                       f'2. Meduim [7x7 game]\n '
                       f'3. Large [10x10 game]')
        if int(option) == 1:
            return [4, 4]
        elif int(option) == 2:
            return [7, 7]
        elif int(option) == 3:
            return [10, 10]
        else:
            print(f' You have chosen an invalid input. '
                  f'Please enter the number corresponding to the size of game you want to play. \ni.e., 1, 2, or 3.')
            return self.select_dimention()
    def create_base_board(self):
        regular_lattice = nx.grid_2d_graph(self.dim[0], self.dim[1])
        pos = {(x, y): (y, -x) for x, y in regular_lattice.nodes()}
        nx.draw(regular_lattice, pos=pos, with_labels=True, node_color='skyblue', node_size=250, font_size=12)
        plt.title("Regular 2d")
        plt.figure(dpi=500)
        plt.show()
        return regular_lattice, pos


def ask_for_selection():
    node1, node2 = input('Make a move. Enter in the format: node1, node2')
    return selection(node1, node2)


def selection(board: nx.Graph, node1:int, node2: int, player) -> nx.Graph:
    still_legal_moves = board.legal_moves
    color = {'player1': 'red', 'player2': 'lightskyblue'}
    if tuple(sorted(node1, node2)) not in still_legal_moves:
        print("This move is not legal. Please try again.")
        ask_for_selection()
    else:
        board.legal_moves.remove(tuple(sorted(node1, node2)))
        edge_list = [(node1, node2)]
        all_node_positions = nx.get_node_attributes(board, 'pos')
        selected_node_pos = {node1: all_node_positions[node1],
                             node2: all_node_positions[node2]}
        nx.draw_networkx_edges(G=board, pos=selected_node_pos, edgelist=edge_list, edge_color=color[player])
        return plt.show()


Game = Board()

