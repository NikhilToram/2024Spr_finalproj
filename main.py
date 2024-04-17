import copy
import random

import networkx as nx
import matplotlib.pyplot as plt
#import pygame
# Create the triangular lattice graph (3 rows, 5 columns)


class Board:
    def __init__(self):
        self.style_dict = {'player1': 'solid', 'player2': 'solid', 'unplayed': 'dashed', 'unplayable': 'solid'}
        self.color_dict = {'player1': 'red', 'player2': 'lightskyblue', 'unplayed': 'black', 'unplayable': 'white'}
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
            pattern = shapes[0]*2 + shapes[1]*3 + shapes[2]*4
        elif self.dim[0] == 7:
            pattern = shapes[0] * 7 + shapes[1] * 11 + shapes[2] * 18
        else:
            pattern = [shapes[0]]*16 + [shapes[1]]*25 + [shapes[2]]*40
        #random.shuffle(pattern)
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
            if ((x, y+1) in initial_nodes) and \
                ((x+1, y+1) in initial_nodes) and \
                    ((x+1, y) in initial_nodes) and \
                    i < len(pattern):
                regular_lattice.add_node((x+0.5, y+0.5), NodeType='shape', NodeShape=list(pattern)[i])
                #print(pattern[i])
                if pattern[i] == 'o':
                    circle.append((x+0.5, y+0.5))
                elif pattern[i] == '^':
                    triangle.append((x+0.5, y+0.5))
                else:
                    square.append((x+0.5, y+0.5))
                regular_lattice.add_edge((x+0.5, y+0.5), (x, y), EdgeType='unplayable')
                regular_lattice.add_edge((x + 0.5, y + 0.5), (x, y+1), EdgeType='unplayable')
                regular_lattice.add_edge((x + 0.5, y + 0.5), (x+1, y+1), EdgeType='unplayable')
                regular_lattice.add_edge((x + 0.5, y + 0.5), (x+1, y), EdgeType='unplayable')
                pos[(x+0.5, y+0.5)] = ((y+0.5), -(x+0.5))
                i = i + 1
        for node in regular_lattice.nodes():
            print(f"for node {node} NodeType is: {regular_lattice.nodes[node]['NodeType']}")
        for edge in regular_lattice.edges():
            print(f"for edge connecting {edge} EdgeType is: {regular_lattice[edge[0]][edge[1]]['EdgeType']}")

        EdgeType = nx.get_edge_attributes(regular_lattice, 'EdgeType').values()
        NodeShape = list(nx.get_node_attributes(regular_lattice, 'NodeShape').values())
        #print(NodeShape)
        nx.draw_networkx(regular_lattice, pos=pos, with_labels=True, node_color='darkgrey', node_size=250,
                         edge_color=[self.color_dict[Edge] for Edge in EdgeType], nodelist = initial_nodes,
                         node_shape= 'o',
                         font_size=5, style=[self.style_dict[Edge] for Edge in EdgeType])
        nx.draw_networkx_nodes(regular_lattice, pos, nodelist=circle, node_shape='o', node_color='green')
        nx.draw_networkx_nodes(regular_lattice, pos, nodelist=triangle, node_shape='^', node_color='green')
        nx.draw_networkx_nodes(regular_lattice, pos, nodelist=square, node_shape='s', node_color='green')
        plt.title("Regular 2d")
        plt.figure(dpi=500)
        plt.show()
        return regular_lattice, pos, circle, triangle, square, initial_nodes

    # def draw_board(self):
    #     # Calculate the dimensions of the board
    #     max_x = max(pos[0] for pos in self.positions.values())
    #     min_x = min(pos[0] for pos in self.positions.values())
    #     max_y = max(pos[1] for pos in self.positions.values())
    #     min_y = min(pos[1] for pos in self.positions.values())
    #
    #     # Calculate the center of the board
    #     center_x = (max_x + min_x) / 2
    #     center_y = (max_y + min_y) / 2
    #
    #     # Calculate the offset to center the board
    #     offset_x = 600 - center_x  # Half of the screen width is 600
    #     offset_y = 600 - center_y  # Assuming a square display
    #
    #     screen = pygame.display.set_mode((800, 600))
    #     screen.fill((255, 255, 255))
    #     for edge in self.board.edges():
    #         # Adjust the positions based on the offset
    #         adjusted_start = (self.positions[edge[0]][0] + offset_x, self.positions[edge[0]][1] + offset_y)
    #         adjusted_end = (self.positions[edge[1]][0] + offset_x, self.positions[edge[1]][1] + offset_y)
    #         pygame.draw.line(screen, self.color_dict[self.board[edge[0]][edge[1]]['EdgeType']],
    #                          adjusted_start, adjusted_end, 3)
    #     for node in self.board.nodes():
    #         # Adjust the positions based on the offset
    #         adjusted_pos = (self.positions[node][0] + offset_x, self.positions[node][1] + offset_y)
    #         pygame.draw.circle(screen, (0, 0, 0), adjusted_pos, 20)
    #     pygame.display.flip()

    def show_board(self, scores: dict, player):
        # EdgeType = nx.get_edge_attributes(self.board, 'EdgeType').values()
        # nx.draw_networkx(self.board, pos=self.positions, with_labels=True, node_color='darkgrey', node_size=250,
        #                  edge_color=[self.color_dict[Edge] for Edge in EdgeType],
        #                  font_size=5, style=[self.style_dict[Edge] for Edge in EdgeType])
        # plt.title("Regular 2d")
        # plt.figure(dpi=500)
        # plt.show()
        EdgeType = nx.get_edge_attributes(self.board, 'EdgeType').values()
        NodeShape = list(nx.get_node_attributes(self.board, 'NodeShape').values())
        #print(NodeShape)
        nx.draw_networkx(self.board, pos=self.positions, with_labels=True, node_color='darkgrey', node_size=250,
                         edge_color=[self.color_dict[Edge] for Edge in EdgeType], nodelist=self.initial_nodes,
                         node_shape='o',
                         font_size=5, style=[self.style_dict[Edge] for Edge in EdgeType])
        nx.draw_networkx_nodes(self.board, self.positions, nodelist=self.circle, node_shape='o', node_color='green')
        nx.draw_networkx_nodes(self.board, self.positions, nodelist=self.triangle, node_shape='^', node_color='green')
        nx.draw_networkx_nodes(self.board, self.positions, nodelist=self.square, node_shape='s', node_color='green')
        plt.title(f"Scores: Player 1 (red) has {scores['player1']} points and Player 2(blue) has {scores['player2']} points\nCurrent player: {player}")
        plt.figure(dpi=500)
        plt.show()


class Play:
    def __init__(self):
        self.board = Board()
        self.score_tracker = {}
        self.player_scores = {'player1': {'circle': 0, 'triangle': 0, 'square': 0},
                              'player2': {'circle': 0, 'triangle': 0, 'square': 0}}
        self.players = ['player1', 'player2']
        self.current_player = self.players[0]
        self.box_counts = {player: 0 for player in self.players}
        self.start = self.play()

    def ask_for_selection(self, player, legal_moves):
        i = 1
        print(f'The available moves are as follows:')
        for legal_move in legal_moves:
            print(f'{i} Node {legal_move[0]} to {legal_move[1]}')
            i = i + 1

        selection = int(input('Make a move. Enter the index of the move you want to play: '))
        return legal_moves[selection - 1]

    def selection(self, player):
        still_legal_moves = self.board.legal_move_edges()

        move = self.ask_for_selection(player, still_legal_moves)
        self.board.board[move[0]][move[1]]['EdgeType'] = player
        #self.board.draw_board()

        return self.advanced_box(player)

    # def box(self, move):
    #     node1, node2 = move[0], move[1]
    #     player_edges = [(u, v, d) for u, v, d in self.board.board.edges(data=True) if d['EdgeType'] in self.players]
    #     only_played_board = nx.Graph(player_edges)
    #     only_played_board.add_edge(node1, node2, EdgeType=self.current_player)  # Add the move to the board
    #     closed_loops = nx.cycle_basis(only_played_board)  # Find all closed loops
    #
    #     for loop in closed_loops:
    #         if len(loop) == 4:  # If the loop has 4 edges, it encloses a box
    #             # Determine the player who completes the box
    #             players_in_loop = set(
    #                 only_played_board[u][v]['EdgeType'] for u, v in zip(loop, loop[1:] + [loop[0]]))
    #             completing_player = next(iter(players_in_loop - {'unplayed', 'unplayable'}), None)
    #             if completing_player:
    #                 self.box_counts[completing_player] += 1
    #     return self.box_counts

    def neighbors_boxed(self, neighbors):
        valid_connection_counter = 0
        neighbors = list(neighbors)
        print(neighbors)
        try:
            if self.board.board[neighbors[0]][neighbors[1]]['EdgeType'] in ['player1', 'player2']:
                valid_connection_counter += 1
        except KeyError:
            pass
        try:
            if self.board.board[neighbors[1]][neighbors[2]]['EdgeType'] in ['player1', 'player2']:
                valid_connection_counter += 1
        except KeyError:
            pass
        try:
            if self.board.board[neighbors[2]][neighbors[3]]['EdgeType'] in ['player1', 'player2']:
                valid_connection_counter += 1
        except KeyError:
            pass
        try:
            if self.board.board[neighbors[0]][neighbors[3]]['EdgeType'] in ['player1', 'player2']:
                valid_connection_counter += 1
        except KeyError:
            pass
        try:
            if self.board.board[neighbors[0]][neighbors[2]]['EdgeType'] in ['player1', 'player2']:
                valid_connection_counter += 1
        except KeyError:
            pass
        try:
            if self.board.board[neighbors[1]][neighbors[3]]['EdgeType'] in ['player1', 'player2']:
                valid_connection_counter += 1
        except KeyError:
            pass

        if valid_connection_counter == 4:
            return True
        else:
            return False

    def advanced_box(self, player):
        boxed = False
        for node in self.board.circle:
            neighbours = nx.neighbors(self.board.board, node)
            if node in self.score_tracker.keys():
                pass
            else:
                if self.neighbors_boxed(neighbours):
                    self.score_tracker[node] = 'circle'
                    self.player_scores[player]['circle'] += 1
                    boxed = True

        for node in self.board.triangle:
            neighbours = nx.neighbors(self.board.board, node)
            if node in self.score_tracker.keys():
                pass
            else:
                if self.neighbors_boxed(neighbours):
                    self.score_tracker[node] = 'triangle'
                    self.player_scores[player]['triangle'] += 1
                    boxed = True

        for node in self.board.square:
            neighbours = nx.neighbors(self.board.board, node)
            if node in self.score_tracker.keys():
                pass
            else:
                if self.neighbors_boxed(neighbours):
                    self.score_tracker[node] = 'square'
                    self.player_scores[player]['square'] += 1
                    boxed = True
        return boxed

    def redraw_map(self, nodes, player, shape):
        for node in nodes:
            self.score_tracker[node] = shape
            neighbors = list(nx.neighbors(self.board.board, node))
            try:
                self.board.board[neighbors[0]][neighbors[1]]['EdgeType'] = player
            except KeyError:
                pass
            try:
                self.board.board[neighbors[1]][neighbors[2]]['EdgeType'] = player
            except KeyError:
                pass
            try:
                self.board.board[neighbors[2]][neighbors[3]]['EdgeType'] = player
            except KeyError:
                pass
            try:
                self.board.board[neighbors[0]][neighbors[3]]['EdgeType'] = player
            except KeyError:
                pass
            try:
                self.board.board[neighbors[0]][neighbors[2]]['EdgeType'] = player
            except KeyError:
                pass
            try:
                self.board.board[neighbors[1]][neighbors[3]]['EdgeType'] = player
            except KeyError:
                pass

    def capturing_shape(self, shape, player):
        if shape == 'circle':
            self.redraw_map(self.board.circle, player, shape)
            self.player_scores[self.players[int(not bool(self.players.index(player)))]]['circle'] = 0
        if shape == 'triangle':
            self.redraw_map(self.board.triangle, player, shape)
            self.player_scores[self.players[int(not bool(self.players.index(player)))]]['triangle'] = 0
        if shape == 'square':
            self.redraw_map(self.board.square, player, shape)
            self.player_scores[self.players[int(not bool(self.players.index(player)))]]['square'] = 0
        print(f'{player} captured {shape}')

    def score(self, player):
        total_circle = len(self.board.circle)
        total_triangle = len(self.board.triangle)
        total_square = len(self.board.square)
        player_1_score = 0
        player_2_score = 0
        captured = False
        if self.player_scores['player1']['circle'] >= total_circle/2 and self.player_scores['player1']['circle'] != total_circle:
            player_1_score += total_circle*5
            self.player_scores['player1']['circle'] = total_circle
            self.capturing_shape('circle', player)
            captured = True
        else:
            player_1_score += self.player_scores['player1']['circle'] * 5
        if self.player_scores['player1']['triangle'] >= total_triangle/2 and self.player_scores['player1']['triangle'] != total_triangle:
            player_1_score += total_triangle * 3
            self.player_scores['player1']['triangle'] = total_triangle
            self.capturing_shape('triangle', player)
            captured = True
        else:
            player_1_score += self.player_scores['player1']['triangle'] * 3
        if self.player_scores['player1']['square'] >= total_square/2 and self.player_scores['player1']['square'] != total_square:
            self.player_scores['player1']['square'] = total_square
            self.capturing_shape('square', player)
            captured = True
            player_1_score += total_square * 2
        else:
            player_1_score += self.player_scores['player1']['square'] * 2

        if self.player_scores['player2']['circle'] >= total_circle / 2 and self.player_scores['player2']['circle'] != total_circle:
            player_2_score += total_circle * 5
            self.player_scores['player2']['circle'] = total_circle
            self.capturing_shape('circle', player)
            captured = True
        else:
            player_2_score += self.player_scores['player2']['circle'] * 5

        if self.player_scores['player2']['triangle'] >= total_triangle / 2 and self.player_scores['player2']['triangle'] != total_triangle:
            player_2_score += total_triangle * 3
            self.player_scores['player2']['triangle'] = total_triangle
            self.capturing_shape('triangle', player)
            captured = True
        else:
            player_2_score += self.player_scores['player2']['triangle'] * 3

        if self.player_scores['player2']['square'] >= total_square / 2 and self.player_scores['player2']['square'] != total_square:
            player_2_score += total_square * 2
            self.player_scores['player2']['square'] = total_square
            self.capturing_shape('square', player)
            captured = True
        else:
            player_2_score += self.player_scores['player2']['square'] * 2
        print(f"player1: {player_1_score},  player2: {player_2_score}")
        return {'player1': player_1_score,  'player2': player_2_score}, captured

    def play(self):
        players = ['player1', 'player2']
        player = 0

        while len(self.board.legal_move_edges()) > 0:
            box_added = self.selection(players[player])
            unstable = True
            while unstable:
                scores, unstable = self.score(players[player])
                print(self.player_scores)

            if not box_added:
                if player == 0:
                    player = 1
                else:
                    player = 0
            else:
                print('You won a box!!!')
            self.board.show_board(scores, players[player])
        return 0


Play()
