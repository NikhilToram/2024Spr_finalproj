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
        self.label_edge_dict = {'player1': False, 'player2': False, 'unplayed': True, 'unplayable': False}
        self.dim = self.select_dimension()
        self.edge_number_dict = {}
        self.edge_number_dict_r = {}
        self.board, self.positions, self.circle, self.triangle, self.square, self.initial_nodes, self.edge_numbers = self.create_base_board()

    def legal_move_edges(self, default_board):
        legal_moves = []
        for edge in nx.edges(default_board if default_board else self.board):
            if default_board[edge[0]][edge[1]]['EdgeType'] == 'unplayed':
                legal_moves.append(edge)
        return legal_moves

    def select_dimension(self):
        option = (input(f'Please enter the integer (n) dimension of the (nxn) grid you want from 3 to 15.'))
        try:
            return [int(option)+1, int(option)+1]
        except ValueError:
            print(f'You have chosen an invalid input. '
                  f'Please enter the number corresponding to the size of game you want to play. \ni.e., 1, 2, or 3.')
            return self.select_dimension()
    def create_base_board(self):
        regular_lattice = nx.grid_2d_graph(self.dim[0], self.dim[1])
        shapes = ['o', '^', 's']
        total_cells = self.dim[0]*self.dim[1]
        circle_num = int(0.2*total_cells)
        triangle_num = int(0.3*total_cells)
        square_num = total_cells-circle_num-triangle_num
        pattern = shapes[0]*(circle_num) + shapes[1]*(triangle_num) + shapes[2]*(square_num)
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
        i = 0
        self.edge_numbers = self.legal_move_edges(regular_lattice)
        print(self.edge_numbers)
        for edge in regular_lattice.edges():
            if edge in self.edge_numbers:

                nx.set_edge_attributes(regular_lattice, i, name='EdgeNumber')
                self.edge_number_dict[edge] = i
                self.edge_number_dict_r[i] = edge
                i += 1
                print(f"for edge connecting {edge}\n\tEdgeType is: {regular_lattice[edge[0]][edge[1]]['EdgeType']}"
                      f"\n\tEdgeNumber is: {regular_lattice[edge[0]][edge[1]]['EdgeNumber']}")
            else:
                print(f"for edge connecting {edge}\n\tEdgeType is: {regular_lattice[edge[0]][edge[1]]['EdgeType']}")

        EdgeType = nx.get_edge_attributes(regular_lattice, 'EdgeType').values()
        NodeShape = list(nx.get_node_attributes(regular_lattice, 'NodeShape').values())
        #print(NodeShape)
        nx.draw_networkx(regular_lattice, pos=pos, with_labels=False, node_color='darkgrey', node_size=50,
                         edge_color=[self.color_dict[Edge] for Edge in EdgeType], nodelist = initial_nodes,
                         node_shape= 'o',
                         font_size=5, style=[self.style_dict[Edge] for Edge in EdgeType])
        nx.draw_networkx_edge_labels(regular_lattice, pos, edge_labels=self.edge_number_dict,
                                     font_color='black', font_size=([12 if self.dim[0] < 6 else 8 if self.dim[0]<=9 else 5][0]), font_weight='bold', rotate=0)
        nx.draw_networkx_nodes(regular_lattice, pos, nodelist=circle, node_shape='o', label=False, node_color='purple',
                               node_size=[200 if self.dim[0] < 6 else 75 if self.dim[0]>9 else 100])
        nx.draw_networkx_nodes(regular_lattice, pos, nodelist=triangle, node_shape='^',label=False, node_color='green',
                               node_size=[200 if self.dim[0] < 6 else 75 if self.dim[0]>9 else 100])
        nx.draw_networkx_nodes(regular_lattice, pos, nodelist=square, node_shape='s',label=False, node_color='navy',
                               node_size=[200 if self.dim[0] < 6 else 75 if self.dim[0]>9 else 100])
        plt.title("Regular 2d")
        plt.figure(dpi=1000)
        plt.show()
        return regular_lattice, pos, circle, triangle, square, initial_nodes, self.edge_numbers

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
        nx.draw_networkx(self.board, pos=self.positions, with_labels=False, node_color='darkgrey', node_size=50,
                         edge_color=[self.color_dict[Edge] for Edge in EdgeType],
                         nodelist=self.initial_nodes,node_shape='o',
                         font_size=5, style=[self.style_dict[Edge] for Edge in EdgeType])
        nx.draw_networkx_edge_labels(self.board, self.positions,
                                     edge_labels={edge: self.edge_number_dict[edge] for edge in self.edge_numbers if self.label_edge_dict[self.board[edge[0]][edge[1]]['EdgeType']]},
                                     #edge_labels=self.edge_number_dict,
                                     font_color='black', font_size=([12 if self.dim[0] < 6 else 8 if self.dim[0]<=9 else 5][0]), font_weight='bold', rotate=0)
        nx.draw_networkx_nodes(self.board, self.positions, nodelist=self.circle, label=False, node_shape='o',
                               node_color='purple', node_size=[200 if self.dim[0] < 6 else 75 if self.dim[0]>9 else 100])
        nx.draw_networkx_nodes(self.board, self.positions, nodelist=self.triangle, label=False, node_shape='^',
                               node_color='green', node_size=[200 if self.dim[0] < 6 else 75 if self.dim[0]>9 else 100])
        nx.draw_networkx_nodes(self.board, self.positions, nodelist=self.square, label=False, node_shape='s',
                               node_color='navy', node_size=[200 if self.dim[0] < 6 else 75 if self.dim[0]>9 else 100])
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
        # print(f'The available moves are as follows:')
        # for edge in self.board.edge_number_dict.keys():
            # if edge in legal_moves:
            #     print(f'{self.board.edge_number_dict[edge]}')

        selection = int(input('Make a move. Enter the edge number of the move you want to play: '))
        return self.board.edge_number_dict_r[selection]
        # Todo: If input > max(self.board.edge_number_dict_r[selection]) -> try again

    def selection(self, player):
        still_legal_moves = self.board.legal_move_edges(self.board.board)

        move = self.ask_for_selection(player, still_legal_moves)
        try:
            if move in still_legal_moves:
                self.board.board[move[0]][move[1]]['EdgeType'] = player
            else:
                print("That edge has already been played! Try again!")
                self.selection(player)
        except KeyError or ValueError:
            print("That edge doesn't exist! Try again!")
            self.selection(player)

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
        # print(neighbors)
        # try:
        #     if self.board.board[neighbors[0]][neighbors[1]]['EdgeType'] in ['player1', 'player2']:
        #         valid_connection_counter += 1
        # except KeyError:
        #     pass
        # try:
        #     if self.board.board[neighbors[1]][neighbors[2]]['EdgeType'] in ['player1', 'player2']:
        #         valid_connection_counter += 1
        # except KeyError:
        #     pass
        # try:
        #     if self.board.board[neighbors[2]][neighbors[3]]['EdgeType'] in ['player1', 'player2']:
        #         valid_connection_counter += 1
        # except KeyError:
        #     pass
        # try:
        #     if self.board.board[neighbors[0]][neighbors[3]]['EdgeType'] in ['player1', 'player2']:
        #         valid_connection_counter += 1
        # except KeyError:
        #     pass
        # try:
        #     if self.board.board[neighbors[0]][neighbors[2]]['EdgeType'] in ['player1', 'player2']:
        #         valid_connection_counter += 1
        # except KeyError:
        #     pass
        # try:
        #     if self.board.board[neighbors[1]][neighbors[3]]['EdgeType'] in ['player1', 'player2']:
        #         valid_connection_counter += 1
        # except KeyError:
        #     pass
        try:
            for pair in [(0, 1), (1, 2), (2, 3), (0, 3), (0, 2), (1, 3)]:
                if self.board.board[neighbors[pair[0]]][neighbors[pair[1]]]['EdgeType'] in ['player1', 'player2']:
                    valid_connection_counter += 1
        except KeyError:
            pass

        if valid_connection_counter == 4:
            return True
        else:
            return False

    def advanced_box(self, player):
        boxed = False
        # for node in self.board.circle:
        #     neighbours = nx.neighbors(self.board.board, node)
        #     if node in self.score_tracker.keys():
        #         pass
        #     else:
        #         if self.neighbors_boxed(neighbours):
        #             self.score_tracker[node] = 'circle'
        #             self.player_scores[player]['circle'] += 1
        #             boxed = True
        #
        # for node in self.board.triangle:
        #     neighbours = nx.neighbors(self.board.board, node)
        #     if node in self.score_tracker.keys():
        #         pass
        #     else:
        #         if self.neighbors_boxed(neighbours):
        #             self.score_tracker[node] = 'triangle'
        #             self.player_scores[player]['triangle'] += 1
        #             boxed = True
        #
        # for node in self.board.square:
        #     neighbours = nx.neighbors(self.board.board, node)
        #     if node in self.score_tracker.keys():
        #         pass
        #     else:
        #         if self.neighbors_boxed(neighbours):
        #             self.score_tracker[node] = 'square'
        #             self.player_scores[player]['square'] += 1
        #             boxed = True
        shape_functions = {'triangle': self.board.triangle, 'square': self.board.square, 'circle': self.board.circle}
        for shape in shape_functions.keys():
            for node in shape_functions[shape]:
                neighbours = nx.neighbors(self.board.board, node)
                if node in self.score_tracker.keys():
                    pass
                else:
                    if self.neighbors_boxed(neighbours):
                        self.score_tracker[node] = shape
                        self.player_scores[player][shape] += 1
                        boxed = True
        return boxed

    def redraw_map(self, nodes, player, shape):
        for node in nodes:
            self.score_tracker[node] = shape
            neighbors = list(nx.neighbors(self.board.board, node))
            try:
                for pair in [(0, 1), (1, 2), (2, 3), (0, 3), (0, 2), (1, 3)]:
                    self.board.board[neighbors[pair[0]]][neighbors[pair[1]]]['EdgeType'] = player
            except KeyError:
                pass
            # try:
            #     self.board.board[neighbors[1]][neighbors[2]]['EdgeType'] = player
            # except KeyError:
            #     pass
            # try:
            #     self.board.board[neighbors[2]][neighbors[3]]['EdgeType'] = player
            # except KeyError:
            #     pass
            # try:
            #     self.board.board[neighbors[0]][neighbors[3]]['EdgeType'] = player
            # except KeyError:
            #     pass
            # try:
            #     self.board.board[neighbors[0]][neighbors[2]]['EdgeType'] = player
            # except KeyError:
            #     pass
            # try:
            #     self.board.board[neighbors[1]][neighbors[3]]['EdgeType'] = player
            # except KeyError:
            #     pass

    def capturing_shape(self, shape, player):
        shape_functions = {'triangle': self.board.triangle, 'square': self.board.square, 'circle': self.board.circle}
        self.redraw_map(shape_functions[shape], player, shape)
        self.player_scores[self.players[int(not bool(self.players.index(player)))]][shape] = 0
        # if shape == 'circle':
        #     self.redraw_map(self.board.circle, player, shape)
        #     self.player_scores[self.players[int(not bool(self.players.index(player)))]]['circle'] = 0
        # if shape == 'triangle':
        #     self.redraw_map(self.board.triangle, player, shape)
        #     self.player_scores[self.players[int(not bool(self.players.index(player)))]]['triangle'] = 0
        # if shape == 'square':
        #     self.redraw_map(self.board.square, player, shape)
        #     self.player_scores[self.players[int(not bool(self.players.index(player)))]]['square'] = 0
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

        while len(self.board.legal_move_edges(self.board.board)) > 0:
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
class AI_player:
    def __init__(self):
        self.game = Play()
        self.score = self.game.player_scores

        self.depth = self.difficulty()

    def difficulty(self):
        diff = input("Type Easy (0), Medium (1), or Hard (2) for computer skill level:")
        try:
            diff = int(diff)
        except TypeError:
            diff = diff.lower()
        try:
            if diff == 'easy' or diff == 0:
                depth = 3
            elif diff == 'medium' or diff == 1:
                depth = 4
            elif diff == 'hard' or diff == 2:
                depth = 5
            return depth
        except ValueError:
            return self.difficulty()

    def alpha_beta(self):
        return self.depth

    def MiniMax(self, board: Board, depth_play, moves: list):
        # find the minimum of the scores
        # find the maximum
        player = 'player2'
        maximum = -20000
        for move in moves:
            move_heuristic = self.heuristic(player, move)
            if move_heuristic> maximum:
                maximum = move_heuristic


    # def alpha_beta(self):
    #
    #
    # def heuristic(self):
    #     return (-1*self.score['player1'])+self.score['player2']
    #
    #


