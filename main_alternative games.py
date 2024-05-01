import copy
import random
import networkx as nx
import matplotlib.pyplot as plt
import tqdm
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
        option = (input(f'Please enter the integer (n) dimension of the (nxn) grid you want from 3 to 15 (recommended range 3-6):'))
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
        pattern = (shapes[0] * circle_num) + (shapes[1] * triangle_num) + (shapes[2] * square_num)
        pattern = list(pattern)
        random.shuffle(pattern)
        pos = {(x, y): (y, -x) for x, y in regular_lattice.nodes()}
        nx.set_node_attributes(regular_lattice, 'game', name='NodeType')
        nx.set_node_attributes(regular_lattice, 'o', name='NodeShape')
        nx.set_edge_attributes(regular_lattice, 'unplayed', name='EdgeType')
        initial_nodes = list(copy.deepcopy(regular_lattice.nodes()))
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

        self.circle = circle
        self.triangle = triangle
        self.square = square

        return regular_lattice, pos, self.circle, self.triangle, self.square, initial_nodes, self.edge_numbers

    def show_board(self, scores: dict, player, indi_scores: dict):
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
        plt.figtext(0.5, 0.01, f'Player 1: {indi_scores["player1"]}\n'
                               f'Player 2: {indi_scores["player2"]}\n'
                               f'total: circle: {len(self.circle)}, '
                               f'triangle: {len(self.triangle)}, '
                               f'square: {len(self.square)}'
                    , wrap=True, horizontalalignment='center', fontsize=12)
        plt.figure(dpi=500)
        plt.show()


class Play():
    def __init__(self, board=Board(), opponent=None):
        self.board = board
        self.score_tracker = {}
        self.player_scores = {'player1': {'circle': 0, 'triangle': 0, 'square': 0},
                              'player2': {'circle': 0, 'triangle': 0, 'square': 0}}
        self.players = ['player1', 'player2']
        self.current_player = self.players[0]
        self.box_counts = {player: 0 for player in self.players}
        # self.circle = self.board.circle
        # self.triangle = self.board.triangle
        # self.square = self.board.square

        if opponent == None:
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
        if selection > ((((self.board.dim[0])*(self.board.dim[1]-1))*2)-1):
            while selection > ((((self.board.dim[0])*(self.board.dim[1]-1))*2)-1):
                selection = int(input("That move doesn't exist on this board. Try Again!"))
        return self.board.edge_number_dict_r[selection]

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
            except KeyError:
                print("\nThat edge doesn't exist! Try again!")
                self.selection(player)

        elif self.mode == 'C' and player == 'player2':
            move, _ = self.AI.MiniMax(copy.deepcopy(self.board), self.difficulty,
                                      moves=self.board.legal_move_edges(self.board.board))
            print(f'Ai move: {move}')
            # self.board.show_board({'player1': 0,  'player2': 0}, player)
            # input(f'')
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
        #print(f'{player} captured {shape}')

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
        #print(f"player1: {player_1_score},  player2: {player_2_score}")
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
            elif opp != 'H' or opp != 'C':
                opp = self.opponent()
        except ValueError:
            opp = self.opponent()
        return opp

    def play(self, moves=[]):
        scores = None
        if len(moves) == 0:
            players = ['player1', 'player2']
            player = 0
            second_turn = False
            while len(self.board.legal_move_edges(self.board.board)) > 0:
                box_added = self.selection(players[player])
                unstable = True
                while unstable:
                    scores, unstable = self.score(players[player])
                    # print(self.player_scores)

                #if not box_added or second_turn:
                if True:
                    second_turn = False
                    if player == 0:
                        player = 1
                    else:
                        player = 0
                else:
                    second_turn = True
                    # print('You won a box!!!')
                self.board.show_board(scores, players[player], self.player_scores)
            print(f'{"Player 1" if scores["player1"]>scores["player2"] else "Player 2"} wins!')
            return 0
        else:
            players = ['player1', 'player2']
            player = 1
            second_turn = False
            for move in moves:
                #print("test")
                self.board.board[move[0]][move[1]]['EdgeType'] = players[player]
                box_added = self.advanced_box(players[player])
                unstable = True
                while unstable:
                    scores, unstable = self.score(players[player])
                    #print(self.player_scores)
                    #print(f'scores{scores}')

                #if not box_added or second_turn:
                if True:
                    second_turn = False
                    if player == 0:
                        player = 1
                    else:
                        player = 0
                else:
                    second_turn = True
                    #print('You won a box!!!')
                #self.board.show_board(scores, players[player])
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
                     "\nHard: 2"
                     "\nYour Choice: ")
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

    def neighbors_boxed(self, board: Board, neighbors, count=4):
        """
        This function determines if a box has been made
        :param count:
        :param board:
        :param neighbors: edge neighbors
        :return: bool
        """
        valid_connection_counter = 0
        valid_connection_tracker = []
        neighbors = list(neighbors)

        try:
            for pair in [(0, 1), (1, 2), (2, 3), (0, 3), (0, 2), (1, 3)]:
                if board.board[neighbors[pair[0]]][neighbors[pair[1]]]['EdgeType'] in ['player1', 'player2']:
                    valid_connection_counter += 1
                else:
                    valid_connection_tracker.append((neighbors[pair[0]],neighbors[pair[1]]))
        except KeyError:
            pass

        if valid_connection_counter == count:
            return True, valid_connection_tracker
        else:
            return False, []

    def advanced_box_tracker(self, board: Board, length=True, count=4, get_moves = False):
        """
        Determines what shape has been boxed in.
        :param count:
        :param length:
        :param board:
        :param player: current player
        :return:
        """

        boxed = []
        good_moves_track = []
        shape_functions = {'triangle': board.triangle, 'square': board.square, 'circle': board.circle}
        for shape in shape_functions.keys():
            for node in shape_functions[shape]:
                neighbours = nx.neighbors(board.board, node)
                valid_check, good_moves = self.neighbors_boxed(board, neighbours, count=count)
                good_moves_track += good_moves
                if valid_check:
                    boxed.append(node)
        if get_moves:
            return good_moves_track
        if length:
            return len(boxed)
        else:
            return boxed

    def MiniMax(self, board: Board, depth_play, moves: list, played_moves=[]):
        # todo: currently the program runs on an assumption of alternating turn, add functionality to check for and
        #  accommodate the possibility of repeating turns.
        # find the minimum of the scores
        # find the maximum
        player = 'player2'
        maximum = -20000
        best_move = None
        good_moves = self.advanced_box_tracker(board, length=False, count=3, get_moves=True) # get any good boxes with 3 sides
        if len(good_moves):
            moves = good_moves
        else:
            good_moves = self.advanced_box_tracker(board, length=False, count=1,
                                                   get_moves=True)  # get any good boxes with 1 sides
            good_moves += self.advanced_box_tracker(board, length=False, count=0,
                                                   get_moves=True)  # get any good boxes with 0 sides
            bad_moves = self.advanced_box_tracker(board, length=False, count=2,
                                                    get_moves=True) # get bad moves i.e., 2 sides boxed
            good_moves = list(set(good_moves))
            for bad_move in bad_moves:
                if bad_move in good_moves:
                    good_moves.remove(bad_move)
                if (bad_move[1], bad_move[0]) in good_moves:
                    good_moves.remove((bad_move[1], bad_move[0]))
            if len(good_moves):
                return random.choice(good_moves), maximum
            else:
                pass

        #moves_copy = moves.copy()
        #print(f'minimax: depth_play: {depth_play}, moves: {moves}')
        box_count = self.advanced_box_tracker(board)
        if depth_play < 2 or len(moves) == 1:
            for move in moves:
                played_moves_updated = played_moves + [move]
                move_heuristic = self.heuristic(board, player, played_moves_updated)
                if move_heuristic > maximum:
                    maximum = move_heuristic
                    best_move = move
            # print(f'minimax Heuristic {maximum}')
            return best_move, maximum
        else:
            for move in tqdm.tqdm(moves, desc="Processing moves"):
                #print(f'\n\n\nMoves: {moves}, count: {len(moves)}\n\n\n')
                board_copy = copy.deepcopy(board)
                board_copy.board[move[0]][move[1]]['EdgeType'] = player
                moves_copy = moves.copy()
                played_moves_updated = played_moves + [move]
                moves_copy.remove(move)
                #if box_count == self.advanced_box_tracker(board_copy):
                if True:
                    _, move_heuristic = self.Minimum(board, depth_play - 1, moves_copy, played_moves_updated, board_copy, prev_min=maximum)
                else:
                    _, move_heuristic = self.Maximum(board, depth_play - 1, moves_copy, played_moves_updated, board_copy)
                #print(f'{move} heuristic {move_heuristic}')
                if move_heuristic > maximum:
                    maximum = move_heuristic
                    best_move = move
                #print(f'best move {best_move} max {maximum}')
            # print(f'minimax {maximum}')
            return best_move, maximum

    def Minimum(self, board: Board, depth_play, moves: list, played_moves: list, board_played: Board, prev_min=None):
        player = 'player1'
        minimum = 20000
        best_move = moves[0]
        box_count = self.advanced_box_tracker(board_played)

        #moves_copy = moves.copy()
        #print(f'Minimum: depth_play: {depth_play}, moves: {moves}')
        if depth_play < 2 or len(moves) == 1:
            for move in moves:
                played_moves_updated = played_moves + [move]
                move_heuristic = self.heuristic(board, player, played_moves_updated)
                if prev_min is not None:
                    if move_heuristic < prev_min:
                        return move, move_heuristic
                if move_heuristic < minimum:
                    minimum = move_heuristic
                    best_move = move
            # print(f'minimum Heuristic {minimum}')
            return best_move, minimum
        else:
            for move in moves:
                board_copy = copy.deepcopy(board_played)
                board_copy.board[move[0]][move[1]]['EdgeType'] = player
                moves_copy = moves.copy()
                played_moves_updated = played_moves + [move]
                moves_copy.remove(move)
                # if box_count == self.advanced_box_tracker(board_copy):
                if True:
                    _, move_heuristic = self.Maximum(board, depth_play - 1, moves_copy, played_moves_updated, board_copy, prev_max=minimum)
                else:
                    _, move_heuristic = self.Minimum(board, depth_play - 1, moves_copy, played_moves_updated, board_copy)
                if prev_min is not None:
                    if move_heuristic < prev_min:
                        return move, move_heuristic
                if move_heuristic < minimum:
                    minimum = move_heuristic
                    best_move = move
            # print(f'minimum {minimum}')
            return best_move, minimum

    def Maximum(self, board: Board, depth_play, moves: list, played_moves: list, board_played: Board, prev_max=None):
        player = 'player2'
        maximum = -20000
        best_move = None
        box_count = self.advanced_box_tracker(board_played)
        #print(f'Maximum: depth_play: {depth_play}, moves: {moves}')
        if depth_play < 2 or len(moves) == 1:
            for move in moves:
                played_moves_updated = played_moves + [move]
                move_heuristic = self.heuristic(board, player, played_moves_updated)
                # print(f'heuristics for {played_moves}: {move_heuristic}')
                if prev_max is not None:
                    if move_heuristic > prev_max:
                        return move, move_heuristic
                if move_heuristic > maximum:
                    maximum = move_heuristic
                    best_move = move
            # print(f'maximum Heuristic {maximum} for {best_move}')
            return best_move, maximum
        else:

            for move in moves:
                board_copy = copy.deepcopy(board_played)
                board_copy.board[move[0]][move[1]]['EdgeType'] = player
                moves_copy = moves.copy()
                played_moves_updated = played_moves + [move]
                moves_copy.remove(move)
                # if box_count == self.advanced_box_tracker(board_copy):
                if True:
                    _, move_heuristic = self.Minimum(board, depth_play-1, moves_copy, played_moves_updated, board_copy, prev_min=maximum)
                else:
                    _, move_heuristic = self.Maximum(board, depth_play - 1, moves_copy, played_moves_updated, board_copy)
                if prev_max is not None:
                    if move_heuristic > prev_max:
                        return move, move_heuristic
                if move_heuristic > maximum:
                    maximum = move_heuristic
                    best_move = move
            #print(f'maximum {maximum}')
            return best_move, maximum

    # def heuristic_idea_test(self, board: Board, player, moves):
    #     AI_play = Play(board)
    #     # todo: modify the play method in the Play class like in the above class to start at a custom player and play a predefined moves
    #     AI_play.play(moves)
    #     AI_play.score()
    def heuristic(self, board: Board, player, moves):
        board_copy = copy.deepcopy(board)
        play_AI = Play(board_copy, opponent='C')
        score = play_AI.play(moves)
        return score['player2'] - score['player1']

Play()


