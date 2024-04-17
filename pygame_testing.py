import copy
import networkx as nx
import pygame
import random
import matplotlib.pyplot as plt
from pygame.locals import *


class Board:
    def __init__(self):
        self.style_dict = {'player1': 'solid', 'player2': 'solid', 'unplayed': 'dashed', 'unplayable': 'solid'}
        self.color_dict = {'player1': 'red', 'player2': 'lightskyblue', 'unplayed': 'black', 'unplayable': 'white',
                           'game': 'black','shape': 'green'}
        self.dim = self.select_dimension()
        self.board, self.positions, self.circle, self.triangle, self.square, self.initial_nodes = self.create_base_board()

    def legal_move_edges(self):
        legal_moves = []
        for edge in nx.edges(self.board):
            if self.board[edge[0]][edge[1]]['EdgeType'] == 'unplayed':
                legal_moves.append(edge)
        return legal_moves

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
        shapes = ['o', '^', 's']
        if self.dim[0] == 4:
            pattern = shapes[0] * 2 + shapes[1] * 3 + shapes[2] * 4
        elif self.dim[0] == 7:
            pattern = shapes[0] * 7 + shapes[1] * 11 + shapes[2] * 18
        else:
            pattern = [shapes[0]] * 16 + [shapes[1]] * 25 + [shapes[2]] * 40
        # random.shuffle(pattern)
        pattern = list(pattern)
        random.shuffle(pattern)
        pos = {(x, y): (y, -x) for x, y in regular_lattice.nodes()}
        nx.set_node_attributes(regular_lattice, 'game', name='NodeType')
        nx.set_node_attributes(regular_lattice, 'o', name='NodeShape')
        nx.set_edge_attributes(regular_lattice, 'unplayed', name='EdgeType')
        initial_nodes = list(copy.copy(regular_lattice.nodes()))
        i = 0
        circle = []
        triangle = []
        square = []
        for x, y in initial_nodes:
            if ((x, y + 1) in initial_nodes) and \
                    ((x + 1, y + 1) in initial_nodes) and \
                    ((x + 1, y) in initial_nodes) and \
                    i < len(pattern):
                regular_lattice.add_node((x + 0.5, y + 0.5), NodeType='shape', NodeShape=list(pattern)[i])

                print(pattern[i])
                if pattern[i] == 'o':
                    circle.append((x + 0.5, y + 0.5))
                elif pattern[i] == '^':
                    triangle.append((x + 0.5, y + 0.5))
                else:
                    square.append((x + 0.5, y + 0.5))
                regular_lattice.add_edge((x + 0.5, y + 0.5), (x, y), EdgeType='unplayable')
                regular_lattice.add_edge((x + 0.5, y + 0.5), (x, y + 1), EdgeType='unplayable')
                regular_lattice.add_edge((x + 0.5, y + 0.5), (x + 1, y + 1), EdgeType='unplayable')
                regular_lattice.add_edge((x + 0.5, y + 0.5), (x + 1, y), EdgeType='unplayable')
                pos[(x + 0.5, y + 0.5)] = ((y + 0.5), -(x + 0.5))
                i = i + 1
        for node in regular_lattice.nodes():
            print(f"for node {node} NodeType is: {regular_lattice.nodes[node]['NodeType']}")
        for edge in regular_lattice.edges():
            print(f"for edge connecting {edge} EdgeType is: {regular_lattice[edge[0]][edge[1]]['EdgeType']}")

        EdgeType = nx.get_edge_attributes(regular_lattice, 'EdgeType').values()
        NodeShape = list(nx.get_node_attributes(regular_lattice, 'NodeShape').values())
        print(NodeShape)
        nx.draw_networkx(regular_lattice, pos=pos, with_labels=True, node_color='darkgrey', node_size=250,
                         edge_color=[self.color_dict[Edge] for Edge in EdgeType], nodelist=initial_nodes,
                         node_shape='o',
                         font_size=5, style=[self.style_dict[Edge] for Edge in EdgeType])
        nx.draw_networkx_nodes(regular_lattice, pos, nodelist=circle, node_shape='o', node_color='green')
        nx.draw_networkx_nodes(regular_lattice, pos, nodelist=triangle, node_shape='^', node_color='green')
        nx.draw_networkx_nodes(regular_lattice, pos, nodelist=square, node_shape='s', node_color='green')
        plt.title("Regular 2d")
        plt.figure(dpi=500)
        plt.show()
        return regular_lattice, pos, circle, triangle, square, initial_nodes

    def draw_board(self):
        screen = pygame.display.set_mode((800, 600), RESIZABLE)
        screen.fill((255, 255, 255))
        for edge in self.board.edges():
            start_pos = (int(self.positions[edge[0]][0] * 50) + 400, int(self.positions[edge[0]][1] * 50) + 300)
            end_pos = (int(self.positions[edge[1]][0] * 50) + 400, int(self.positions[edge[1]][1] * 50) + 300)
            pygame.draw.line(screen, self.color_dict[self.board[edge[0]][edge[1]]['EdgeType']],
                             start_pos, end_pos, 3)
        for node in self.board.nodes():
            print(self.board[node])
            node_type = self.board.nodes[node]['NodeType']
            node_shape = self.board.nodes[node]['NodeShape']
            node_pos = (int(self.positions[node][0] * 50) + 400, int(self.positions[node][1] * 50) + 300)
            if node_type == 'shape':
                if node_shape == '^':
                    triangle_size = 10
                    triangle_vertices = [(node_pos[0], node_pos[1] - triangle_size),
                                         (node_pos[0] - triangle_size, node_pos[1] + triangle_size),
                                         (node_pos[0] + triangle_size, node_pos[1] + triangle_size)]
                    pygame.draw.polygon(screen, self.color_dict[self.board.nodes[node]['NodeType']], triangle_vertices)
                elif node_shape == 'o':
                    pygame.draw.circle(screen, self.color_dict[self.board.nodes[node]['NodeType']], node_pos, 10)
                elif node_shape == 's':
                    node_rect = pygame.Rect(node_pos[0] - 10, node_pos[1] - 10, 20, 20)
                    pygame.draw.rect(screen, self.color_dict[self.board.nodes[node]['NodeType']], node_rect)
            else:
                pygame.draw.circle(screen, (0, 0, 0), node_pos, 10)

            # pygame.draw.circle(screen, (0, 0, 0), node_pos, 10)
        pygame.display.flip()


class Play:
    def __init__(self):
        self.board = Board()
        self.players = ['player1', 'player2']
        self.current_player = self.players[0]
        self.box_counts = {player: 0 for player in self.players}
        self.start = self.play()

    def player_turn(self, move):
        if self.box(move):
            pass

    def ask_for_selection(self, player, legal_moves):
        i = 1
        print(f'The available moves are as follows:')
        for legal_move in legal_moves:
            print(f'{i} Node {legal_move[0]} to {legal_move[1]}')
            i = i + 1

        selection = int(input('Make a move. Enter the index of the move you want to play'))
        return legal_moves[selection - 1]

    def selection(self, player):
        still_legal_moves = self.board.legal_move_edges()

        move = self.ask_for_selection(player, still_legal_moves)
        self.board.board[move[0]][move[1]]['EdgeType'] = player
        self.board.draw_board()
        return self.box(move)

    def box(self, move):
        node1, node2 = move[0], move[1]
        player_edges = [(u, v, d) for u, v, d in self.board.board.edges(data=True) if d['EdgeType'] in self.players]
        only_played_board = nx.Graph(player_edges)
        only_played_board.add_edge(node1, node2, EdgeType=self.current_player)  # Add the move to the board
        closed_loops = nx.cycle_basis(only_played_board)  # Find all closed loops

        for loop in closed_loops:
            if len(loop) == 4:  # If the loop has 4 edges, it encloses a box
                # Determine the player who completes the box
                players_in_loop = set(
                    only_played_board[u][v]['EdgeType'] for u, v in zip(loop, loop[1:] + [loop[0]]))
                completing_player = next(iter(players_in_loop - {'unplayed', 'unplayable'}), None)
                if completing_player:
                    self.box_counts[completing_player] += 1
        return self.box_counts

    def play(self):
        pygame.init()

        players = ['player1', 'player2']
        player = 0
        while len(self.board.legal_move_edges()) > 0:
            box_added = self.selection(players[player])
            if not box_added:
                if player == 0:
                    player = 1
                else:
                    player = 0
        return 0


Game = Play()
