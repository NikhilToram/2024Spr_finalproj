import networkx as nx
import matplotlib.pyplot as plt


def ask_for_selection():
    node1, node2 = input('Make a move. Enter in the format: node1, node2')
    return selection(node1, node2)


def selection(board: nx.Graph, node1:int, node2: int, player) -> nx.Graph:
    already_played = []
    color = {'player1': 'red', 'player2': 'lightskyblue'}
    if tuple(sorted(node1, node2)) in already_played:
        print("This move has already been played. Please try again.")
        ask_for_selection()
    else:
        already_played.append(tuple(sorted(node1, node2)))
        edge_list = [(node1, node2)]
        all_node_positions = nx.get_node_attributes(board, 'pos')
        selected_node_pos = {node1: all_node_positions[node1],
                             node2: all_node_positions[node2]}
        nx.draw_networkx_edges(G=board, pos=selected_node_pos, edgelist=edge_list, edge_color=color[player])
        return plt.show()