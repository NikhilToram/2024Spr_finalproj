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
        # plt.show()
        return regular_lattice, pos, circle, triangle, square, initial_nodes

    def draw_board(self, selected_edge=None):
        screen = pygame.display.set_mode((800, 600), RESIZABLE)
        screen.fill((255, 255, 255))

        buffer = pygame.Surface((800, 600))
        buffer.fill((255, 255, 255))

        # Draw lines and shapes to the off-screen buffer with colors corresponding to the player
        for edge in self.board.edges():
            start_pos = (int(self.positions[edge[0]][0] * 50) + 400, int(self.positions[edge[0]][1] * 50) + 300)
            end_pos = (int(self.positions[edge[1]][0] * 50) + 400, int(self.positions[edge[1]][1] * 50) + 300)
            color = self.color_dict[self.board[edge[0]][edge[1]]['EdgeType']]
            if edge == selected_edge:  # Change color for selected edge
                color = self.color_dict[self.current_player]
            pygame.draw.line(buffer, color, start_pos, end_pos, 3)

        for node in self.board.nodes():
            node_type = self.board.nodes[node]['NodeType']
            node_shape = self.board.nodes[node]['NodeShape']
            node_pos = (int(self.positions[node][0] * 50) + 400, int(self.positions[node][1] * 50) + 300)
            if node_type == 'shape':
                if node_shape == '^':
                    triangle_size = 10
                    triangle_vertices = [(node_pos[0], node_pos[1] - triangle_size),
                                         (node_pos[0] - triangle_size, node_pos[1] + triangle_size),
                                         (node_pos[0] + triangle_size, node_pos[1] + triangle_size)]
                    pygame.draw.polygon(buffer, self.color_dict[self.board.nodes[node]['NodeType']], triangle_vertices)
                elif node_shape == 'o':
                    pygame.draw.circle(buffer, self.color_dict[self.board.nodes[node]['NodeType']], node_pos, 10)
                elif node_shape == 's':
                    node_rect = pygame.Rect(node_pos[0] - 10, node_pos[1] - 10, 20, 20)
                    pygame.draw.rect(buffer, self.color_dict[self.board.nodes[node]['NodeType']], node_rect)
            else:
                pygame.draw.circle(buffer, (0, 0, 0), node_pos, 5)

        # Blit the off-screen buffer to the screen
        screen.blit(buffer, (0, 0))
        pygame.display.flip()

        # Wait for player input (mouse click)
        while True:
            for event in pygame.event.get():
                print("Event received:", event)
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button clicked
                        pos = pygame.mouse.get_pos()
                        print(pos)
                        selected_edge = self.get_selected_edge(pos)
                        print(selected_edge)
                        if selected_edge and selected_edge in self.board.legal_move_edges():
                            self.board.board[selected_edge[0]][selected_edge[1]]['EdgeType'] = self.current_player
                            self.box(selected_edge=selected_edge)
                            return self.draw_board(selected_edge)  # Update the display after a valid mouse click

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button clicked
                        pos = pygame.mouse.get_pos()
                        selected_edge = self.get_selected_edge(pos)
                        if selected_edge and selected_edge in self.legal_move_edges():
                            self.board.board[selected_edge[0]][selected_edge[1]]['EdgeType'] = self.current_player
                            self.box(selected_edge)
                            return self.draw_board(selected_edge)  # Update the display after a valid mouse click

    # def draw_board(self, selected_edge=None):
    #     screen = pygame.display.set_mode((800, 600), RESIZABLE)
    #     screen.fill((255, 255, 255))
    #
    #     buffer = pygame.Surface((800, 600))
    #     buffer.fill((255, 255, 255))
    #
    #     # Draw lines and shapes to the off-screen buffer
    #     for edge in self.board.edges():
    #         start_pos = (int(self.positions[edge[0]][0] * 50) + 400, int(self.positions[edge[0]][1] * 50) + 300)
    #         end_pos = (int(self.positions[edge[1]][0] * 50) + 400, int(self.positions[edge[1]][1] * 50) + 300)
    #         color = self.color_dict[self.board[edge[0]][edge[1]]['EdgeType']]
    #         if edge == selected_edge:  # Change color for selected edge
    #             color = self.color_dict[self.current_player]
    #         pygame.draw.line(buffer, color, start_pos, end_pos, 3)
    #
    #     for node in self.board.nodes():
    #         node_type = self.board.nodes[node]['NodeType']
    #         node_shape = self.board.nodes[node]['NodeShape']
    #         node_pos = (int(self.positions[node][0] * 50) + 400, int(self.positions[node][1] * 50) + 300)
    #         if node_type == 'shape':
    #             if node_shape == '^':
    #                 triangle_size = 10
    #                 triangle_vertices = [(node_pos[0], node_pos[1] - triangle_size),
    #                                      (node_pos[0] - triangle_size, node_pos[1] + triangle_size),
    #                                      (node_pos[0] + triangle_size, node_pos[1] + triangle_size)]
    #                 pygame.draw.polygon(buffer, self.color_dict[self.board.nodes[node]['NodeType']], triangle_vertices)
    #             elif node_shape == 'o':
    #                 pygame.draw.circle(buffer, self.color_dict[self.board.nodes[node]['NodeType']], node_pos, 10)
    #             elif node_shape == 's':
    #                 node_rect = pygame.Rect(node_pos[0] - 10, node_pos[1] - 10, 20, 20)
    #                 pygame.draw.rect(buffer, self.color_dict[self.board.nodes[node]['NodeType']], node_rect)
    #         else:
    #             pygame.draw.circle(buffer, (0, 0, 0), node_pos, 5)
    #
    #     # Blit the off-screen buffer to the screen
    #     screen.blit(buffer, (0, 0))
    #     pygame.display.flip()
    #
    #     # Wait for player input (mouse click)
    #     while True:
    #         for event in pygame.event.get():
    #             if event.type == QUIT:
    #                 pygame.quit()
    #                 quit()
    #             elif event.type == MOUSEBUTTONDOWN:
    #                 if event.button == 1:  # Left mouse button clicked
    #                     pos = pygame.mouse.get_pos()
    #                     selected_edge = self.get_selected_edge(pos)
    #                     if selected_edge and selected_edge in self.board.legal_move_edges():
    #                         self.board.board[selected_edge[0]][selected_edge[1]]['EdgeType'] = self.current_player
    #                         self.box(selected_edge=selected_edge)
    #                         return self.draw_board()  # Update the display after a valid mouse click

    def get_selected_edge(self, pos):
        # Iterate over the edges and find the edge closest to the mouse click
        print(self.board.edges())
        min_distance = 1000
        for edge in self.board.edges():
            print(edge)
            start_pos = self.positions[edge[0]]
            end_pos = self.positions[edge[1]]
            # Calculate the distance from the click position to the edge
            distance = abs((end_pos[1] - start_pos[1]) * pos[0] - (end_pos[0] - start_pos[0]) * pos[1] +
                           end_pos[0] * start_pos[1] - end_pos[1] * start_pos[0]) / \
                       ((end_pos[1] - start_pos[1]) ** 2 + (end_pos[0] - start_pos[0]) ** 2) ** 0.5
            # If the distance is within a certain threshold, consider it as a click on the edge
            print(distance)
            if distance < min_distance:  # You can adjust the threshold as needed
                print(edge)
                return edge
            else:
                return None


class Play:
    def __init__(self):
        self.board = Board()
        self.players = ['player1', 'player2']
        self.current_player = self.players[0]
        self.box_counts = {player: 0 for player in self.players}
        self.start = self.play()

    def play(self):
        pygame.init()
        selected_edge = None  # Variable to store the selected edge

        running = True
        while running:
            # Event handling loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button clicked
                        pos = pygame.mouse.get_pos()
                        selected_edge = self.selection(pos)  # Get the selected edge

            # If an edge is selected
            if selected_edge:
                if selected_edge in self.board.legal_move_edges():
                    self.board[selected_edge[0]][selected_edge[1]]['EdgeType'] = self.current_player
                    self.board.draw_board(selected_edge)  # Update display with selected edge
                    self.box(selected_edge)
                    self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
                    selected_edge = None  # Reset the selected edge for the next turn

            # Update the display
            self.board.draw_board()

            # Check game over condition
            if len(self.board.legal_move_edges()) == 0:
                running = False

    def selection(self, pos):
        # Wait for player input (mouse click)
        print("Mouse position:", pos)  # Print mouse position for debugging
        for edge in self.board.board.edges():
            start_pos = self.board.positions[edge[0]]
            end_pos = self.board.positions[edge[1]]
            if self.is_clicked(pos, start_pos, end_pos):
                return edge
        return None

    def is_clicked(self, pos, start_pos, end_pos):
        # Check if the position is within a certain distance from the edge
        threshold = 10  # Adjust this value as needed
        distance = abs((end_pos[1] - start_pos[1]) * pos[0] - (end_pos[0] - start_pos[0]) * pos[1] +
                       end_pos[0] * start_pos[1] - end_pos[1] * start_pos[0]) / \
                   ((end_pos[1] - start_pos[1]) ** 2 + (end_pos[0] - start_pos[0]) ** 2) ** 0.5
        return distance < threshold


Game = Play()
