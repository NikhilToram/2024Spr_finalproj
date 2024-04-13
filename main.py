import copy

import networkx as nx
import matplotlib.pyplot as plt
#import pygame
# Create the triangular lattice graph (3 rows, 5 columns)


class Board:
    def __init__(self):
        self.style_dict = {'unplayed': 'dashed', 'unplayable': 'solid'}
        self.color_dict = {'unplayed': 'black', 'unplayable': 'white'}
        self.dim = self.select_dimension()
        self.board, self.positions = self.create_base_board()


    def select_dimension(self):
        option = input(f'Please select the number of the game size that you want to play. \n '
                       f'1. Small [4x4 game]\n '
                       f'2. Medium [7x7 game]\n '
                       f'3. Large [10x10 game]\n'
                       f'Your selection: ')
        if int(option) == 1:
            return [4, 4]
        elif int(option) == 2:
            return [7, 7]
        elif int(option) == 3:
            return [10, 10]
        else:
            print(f' You have chosen an invalid input. '
                  f'Please enter the number corresponding to the size of game you want to play. \ni.e., 1, 2, or 3.')
            return self.select_dimension()
    def create_base_board(self):
        regular_lattice = nx.grid_2d_graph(self.dim[0], self.dim[1])
        pos = {(x, y): (y, -x) for x, y in regular_lattice.nodes()}
        nx.set_node_attributes(regular_lattice, 'game', name='NodeType')
        nx.set_edge_attributes(regular_lattice, 'unplayed', name='EdgeType')
        initial_nodes = list(copy.copy(regular_lattice.nodes()))
        for x, y in initial_nodes:
            if ((x, y+1) in initial_nodes) and \
                ((x+1, y+1) in initial_nodes) and \
                    ((x+1, y) in initial_nodes):
                regular_lattice.add_node((x+0.5, y+0.5), NodeType='shape')
                regular_lattice.add_edge((x+0.5, y+0.5), (x, y), EdgeType='unplayable')
                regular_lattice.add_edge((x + 0.5, y + 0.5), (x, y+1), EdgeType='unplayable')
                regular_lattice.add_edge((x + 0.5, y + 0.5), (x+1, y+1), EdgeType='unplayable')
                regular_lattice.add_edge((x + 0.5, y + 0.5), (x+1, y), EdgeType='unplayable')
                pos[(x+0.5, y+0.5)] = ((y+0.5), -(x+0.5))
        for node in regular_lattice.nodes():
            print(f"for node {node} NodeType is: {regular_lattice.nodes[node]['NodeType']}")
        for edge in regular_lattice.edges():
            print(f"for edge connecting {edge} EdgeType is: {regular_lattice[edge[0]][edge[1]]['EdgeType']}")
        EdgeType = nx.get_edge_attributes(regular_lattice, 'EdgeType').values()
        nx.draw_networkx(regular_lattice, pos=pos, with_labels=True, node_color='darkgrey', node_size=250,
                         edge_color=[self.color_dict[Edge] for Edge in EdgeType],
                         font_size=5, style=[self.style_dict[Edge] for Edge in EdgeType])
        plt.title("Regular 2d")
        plt.figure(dpi=500)
        plt.show()
        return regular_lattice, pos

class Play:
    def __init__(self):
        self.board = Board
        self.legal_moves = [tuple(sorted([edge[0], edge[1]])) for edge in nx.edges(self.board)]
        self.players = ['player1', 'player2']
        self.current_player = self.players[0]
        self.box_counts = {player: 0 for player in self.players}
    def box(self, move):
        node1, node2 = move[0], move[1]
        without_shapes_board = self.board.copy()
        try:
           if nx.find_cycle(without_shapes_board, source= [node1,node2]):
               return True
        except nx.NetworkXNoCycle:
            self.current_player = self.players[self.players[self.current_player].index+1]
            print(self.current_player)

    def player_turn(self, move):
        if self.box(move):

    def ask_for_selection(self, player):
        node1, node2 = input('Make a move. Enter in the format: node1, node2')
        return self.selection(node1, node2, player)


    def selection(self, node1: int, node2: int, player) -> nx.Graph:
        still_legal_moves = self.board.legal_moves
        color = {'player1': 'red', 'player2': 'lightskyblue'}
        if tuple(sorted(node1, node2)) not in still_legal_moves or \
                self.board[node1][node2]["EdgeType"] != "unplayable" :
            print("This move is not legal. Please try again.")
            self.ask_for_selection(player)
        else:
            self.board.legal_moves.remove(tuple(sorted(node1, node2)))
            edge_list = [(node1, node2)]
            all_node_positions = nx.get_node_attributes(self.board, 'pos')
            selected_node_pos = {node1: all_node_positions[node1],
                                 node2: all_node_positions[node2]}
            nx.draw_networkx_edges(G=self.board, pos=selected_node_pos, edgelist=edge_list, edge_color=color[player])
            return plt.show()


Game = Board()

