import copy
import networkx as nx
import pygame

class Board:
    def __init__(self):
        self.style_dict = {'player1': 'solid', 'player2': 'solid', 'unplayed': 'dashed', 'unplayable': 'solid'}
        self.color_dict = {'player1': (255, 0, 0), 'player2': (173, 216, 230), 'unplayed': (0, 0, 0), 'unplayable': (255, 255, 255)}
        self.dim = self.select_dimension()
        self.board, self.positions = self.create_base_board()

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
        pos = {(x, y): (y * 100 + 50, x * 100 + 50) for x, y in regular_lattice.nodes()}
        nx.set_node_attributes(regular_lattice, 'game', name='NodeType')
        nx.set_node_attributes(regular_lattice, 'o', name='NodeShape')
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
                pos[(x+0.5, y+0.5)] = ((y+0.5) * 100 + 50, (x+0.5) * 100 + 50)
        return regular_lattice, pos

    def draw_board(self):
        # Calculate the dimensions of the board
        max_x = max(pos[0] for pos in self.positions.values())
        min_x = min(pos[0] for pos in self.positions.values())
        max_y = max(pos[1] for pos in self.positions.values())
        min_y = min(pos[1] for pos in self.positions.values())

        # Calculate the center of the board
        center_x = (max_x + min_x) / 2
        center_y = (max_y + min_y) / 2

        # Calculate the offset to center the board
        offset_x = 600 - center_x  # Half of the screen width is 600
        offset_y = 600 - center_y  # Assuming a square display

        screen = pygame.display.set_mode((800, 600))
        screen.fill((255, 255, 255))
        for edge in self.board.edges():
            # Adjust the positions based on the offset
            adjusted_start = (self.positions[edge[0]][0] + offset_x, self.positions[edge[0]][1] + offset_y)
            adjusted_end = (self.positions[edge[1]][0] + offset_x, self.positions[edge[1]][1] + offset_y)
            pygame.draw.line(screen, self.color_dict[self.board[edge[0]][edge[1]]['EdgeType']],
                             adjusted_start, adjusted_end, 3)
        for node in self.board.nodes():
            # Adjust the positions based on the offset
            adjusted_pos = (self.positions[node][0] + offset_x, self.positions[node][1] + offset_y)
            pygame.draw.circle(screen, (0, 0, 0), adjusted_pos, 20)
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
        return legal_moves[selection-1]

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
        players = ['player1', 'player2']
        player = 0
        while len(self.board.legal_move_edges())>0:
            box_added = self.selection(players[player])
            if not box_added:
                if player == 0:
                    player = 1
                else:
                    player = 0
        return 0

pygame.init()
Game = Play()