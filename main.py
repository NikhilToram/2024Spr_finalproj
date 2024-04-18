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
    plt.clf()
    def legal_move_edges(self, default_board):
        """
        This function calculates the valid moves for the game
        :param default_board: dummy variable
        :return:
        """
        legal_moves = []
        for edge in nx.edges(default_board if default_board else self.board):
            if default_board[edge[0]][edge[1]]['EdgeType'] == 'unplayed':
                legal_moves.append(edge)
        return legal_moves

    def select_dimension(self):
        """
        Asks user for dimension n for nxn board
        :return:
        """
        option = (input(f'Please enter the integer (n) dimension of the (nxn) grid you want from 3 to 15.'))
        try:
            return [int(option)+1, int(option)+1]
        except ValueError:
            print(f'You have chosen an invalid input.'
                  f'Please enter the number corresponding to the size of game you want to play. \ni.e., 1, 2, or 3.')
            return self.select_dimension()
    def create_base_board(self):
        """
        This function creates the original game board which will be updated throughout the game in other functions.
        This is only responsible for the original board (before any gameplay)
        :return: board
        """
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

        i = 0
        self.edge_numbers = self.legal_move_edges(regular_lattice)
        # print(self.edge_numbers)
        for edge in regular_lattice.edges():
            if edge in self.edge_numbers:

                nx.set_edge_attributes(regular_lattice, i, name='EdgeNumber')
                self.edge_number_dict[edge] = i
                self.edge_number_dict_r[i] = edge
                i += 1

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
        plt.figure(dpi=500)
        plt.show()
        return regular_lattice, pos, circle, triangle, square, initial_nodes, self.edge_numbers


    def show_board(self, scores: dict, player):
        """
        This function is the board updating function. It creates a new board after every move.
        :param scores: Current player scores
        :param player: current player
        :return:
        """
        EdgeType = nx.get_edge_attributes(self.board, 'EdgeType').values()
        NodeShape = list(nx.get_node_attributes(self.board, 'NodeShape').values())
        #print(NodeShape)
        nx.draw_networkx(self.board, pos=self.positions, with_labels=False, node_color='darkgrey', node_size=50,
                         edge_color=[self.color_dict[Edge] for Edge in EdgeType],
                         nodelist=self.initial_nodes,node_shape='o',
                         font_size=5, style=[self.style_dict[Edge] for Edge in EdgeType])
        nx.draw_networkx_edge_labels(self.board, self.positions,
                                     edge_labels={edge: self.edge_number_dict[edge] for edge in self.edge_numbers if
                                                  self.label_edge_dict[self.board[edge[0]][edge[1]]['EdgeType']]},
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


class Play():
    def __init__(self, board=Board(), opponent=False):
        self.board = board
        self.score_tracker = {}
        self.player_scores = {'player1': {'circle': 0, 'triangle': 0, 'square': 0},
                              'player2': {'circle': 0, 'triangle': 0, 'square': 0}}
        self.players = ['player1', 'player2']
        self.current_player = self.players[0]
        self.box_counts = {player: 0 for player in self.players}
        if opponent == False:
            self.mode = self.opponent()
            self.start = self.play()
        else:
            self.mode = opponent

        self.difficulty = None

    def ask_for_selection(self, player, legal_moves):
        """
        This function asks the user for the move they'd like to play
        :param player: current player
        :param legal_moves: the valid moves at the turn when this is called
        :return:
        """
        selection = int(input('Make a move. Enter the edge number of the move you want to play: '))
        return self.board.edge_number_dict_r[selection]
        # Todo: If input > max(self.board.edge_number_dict_r[selection]) -> try again

    def selection(self, player):
        """
        This function makes the move that was specified in self.ask_for_selection(). If an edge is selected that has
        already been played, the user will be prompted to pick a new edge.
        :param player: current player
        :return:
        """
        if self.mode == 'H' or player == 'player1':
            still_legal_moves = self.board.legal_move_edges(self.board.board)

            move = self.ask_for_selection(player, still_legal_moves)
            try:
                if move in still_legal_moves:
                    self.board.board[move[0]][move[1]]['EdgeType'] = player
                else:
                    print("\nThat edge has already been played! Try again!")
                    self.selection(player)
            except KeyError or ValueError:
                print("\nThat edge doesn't exist! Try again!")
                self.selection(player)
                # TODO: Needs to be fixed
            #return self.advanced_box(player)
        elif self.mode == 'C' and player == 'player2':
            move, _ = self.AI.MiniMax(self.board.board, self.difficulty,
                                      moves=self.board.legal_move_edges(self.board.board))
            print(f'Ai move: {move}')
            self.board.board[move[0]][move[1]]['EdgeType'] = player
        return self.advanced_box(player)

    def neighbors_boxed(self, neighbors):
        """
        This function determines if a box has been made
        :param neighbors: edge neighbors
        :return: bool
        """
        valid_connection_counter = 0
        neighbors = list(neighbors)
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
        """
        Determines what shape has been boxed in.
        :param player: current player
        :return:
        """
        boxed = False
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
        """
        This function remaps the board by assigning a box to a player once it has been captured
        :param nodes:
        :param player:
        :param shape:
        :return:
        """
        for node in nodes:
            self.score_tracker[node] = shape
            neighbors = list(nx.neighbors(self.board.board, node))
            try:
                for pair in [(0, 1), (1, 2), (2, 3), (0, 3), (0, 2), (1, 3)]:
                    self.board.board[neighbors[pair[0]]][neighbors[pair[1]]]['EdgeType'] = player
            except KeyError:
                pass

    def capturing_shape(self, shape, player):
        """
        This function calls self.redraw_map() and self.player_scores()
        :param shape:
        :param player:
        :return:
        """
        shape_functions = {'triangle': self.board.triangle, 'square': self.board.square, 'circle': self.board.circle}
        self.redraw_map(shape_functions[shape], player, shape)
        self.player_scores[self.players[int(not bool(self.players.index(player)))]][shape] = 0
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

    def opponent(self):
        opp = (input('To play against the computer, enter C. To play against a human opponent, type H.')).upper()
        try:
            if opp == 'C':
                self.mode = 'C'
                self.AI = AI_player()
                self.difficulty = self.AI.depth

            elif opp == 'H':
                self.mode = 'H'
        except ValueError:
            opp = self.opponent()
        return opp

    def play(self, moves=[]):
        if len(moves) == 0:
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
            print(f'{"Player 1" if scores["player1"]>scores["player2"] else "Player 2"} wins!')
            return 0
        else:
            players = ['player1', 'player2']
            player = 1
            for move in moves:
                self.board[move[0]][move[1]]['EdgeType'] = player
                box_added = self.advanced_box(players[player])
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
            # print(f'{"Player 1" if scores["player1"] > scores["player2"] else "Player 2"} wins!')
            return scores


class AI_player:
    def __init__(self):
        # self.score = player_scores

        self.depth = self.difficulty()

    def difficulty(self):
        diff = input("To set computer skill level, type the number associated with the desired difficulty:"
                     "\nEasy: 0"
                     "\nMedium: 1"
                     "\nHard: 2")
        try:
            diff = int(diff)
        except TypeError:
            diff = diff.lower()
        try:
            if diff == 0:
                depth = 3
            elif diff == 1:
                depth = 4
            elif diff == 2:
                depth = 5
            return depth
        except ValueError:
            return self.difficulty()

    def alpha_beta(self):
        return self.depth

    def MiniMax(self, board: Board, depth_play, moves: list, played_moves=[]):
        # todo: currently the program runs on an assumption of alternating turn, add functionality to check for and
        #  accommodate the possibility of repeating turns.
        # find the minimum of the scores
        # find the maximum
        player = 'player2'
        maximum = -20000
        played_moves.append('')
        best_move = None
        #moves_copy = moves.copy()
        #print(f'minimax: depth_play: {depth_play}, moves: {moves}')
        if depth_play < 2 or len(moves) == 1:
            for move in moves:
                played_moves[-1] = move
                move_heuristic = self.heuristic(board, player, played_moves)
                if move_heuristic > maximum:
                    maximum = move_heuristic
                    best_move = move
            return best_move
        else:
            for move in moves:
                moves_copy = moves.copy()
                played_moves[-1] = move
                moves_copy.remove(move)
                _, move_heuristic = self.Minimum(board, depth_play-1, moves_copy, played_moves)
                if move_heuristic > maximum:
                    maximum = move_heuristic
                    best_move = move, maximum
            return best_move

    def Minimum(self, board: Board, depth_play, moves: list, played_moves: list):
        player = 'player1'
        minimum = 20000
        played_moves.append('')
        best_move = moves[0]
        #moves_copy = moves.copy()
        #print(f'Minimum: depth_play: {depth_play}, moves: {moves}')
        if depth_play < 2 or len(moves) == 1:
            for move in moves:
                played_moves[-1] = move
                move_heuristic = self.heuristic(board, player, played_moves)
                if move_heuristic < minimum:
                    minimum = move_heuristic
                    best_move = move
            return best_move, minimum
        else:
            for move in moves:
                moves_copy = moves.copy()
                played_moves[-1] = move
                moves_copy.remove(move)
                _, move_heuristic = self.Maximum(board, depth_play-1, moves_copy, played_moves)
                if move_heuristic < minimum:
                    minimum = move_heuristic
                    best_move = move, minimum
            return best_move, minimum

    def Maximum(self, board: Board, depth_play, moves: list, played_moves: list):
        player = 'player2'
        maximum = -20000
        played_moves.append('')
        best_move = None
        #print(f'Maximum: depth_play: {depth_play}, moves: {moves}')
        if depth_play < 2 or len(moves) == 1:
            for move in moves:
                played_moves[-1] = move
                move_heuristic = self.heuristic(board, player, played_moves)
                if move_heuristic > maximum:
                    maximum = move_heuristic
                    best_move = move
            return best_move, maximum
        else:
            for move in moves:
                moves_copy = moves.copy()
                played_moves[-1] = move
                moves_copy.remove(move)
                _, move_heuristic = self.Minimum(board, depth_play-1, moves_copy, played_moves)
                if move_heuristic > maximum:
                    maximum = move_heuristic
                    best_move = move, maximum
            return best_move, maximum

    # def heuristic_idea_test(self, board: Board, player, moves):
    #     todo: modify the play method in the Play class like in the above class to start at a custom player and play a predefined moves
    def heuristic(self, board: Board, player, moves):
        play_AI = Play(board, opponent='C')
        print(moves)
        self.score = play_AI.play(moves)
        return(-1 * self.score['player1']) + self.score['player2']

Play()


