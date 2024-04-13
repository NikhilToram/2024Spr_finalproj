import math

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import math

# G = nx.icosahedral_graph()
# # pos = nx.planar_layout(G)
# pos = nx.kamada_kawai_layout(G)
# nx.draw(G, pos=pos, with_labels=True, node_color='skyblue', node_size=150, font_size=12, font_weight='bold', edge_color='gray')
# # plt.show()
#
# # H = nx.truncated_tetrahedron_graph()
# # H = nx.tetrahedral_graph()
# # pos = nx.planar_layout(H)
# # nx.draw(H, pos=pos, with_labels=True, node_color='skyblue', node_size=150, font_size=12, font_weight='bold', edge_color='gray')
# # plt.show()
# # X = nx.hexagonal_lattice_graph(1,1)
#
# #
# # # # Draw the graph
# # # nx.draw(C, pos=pos, with_labels=True, node_color='skyblue', node_size=150, font_size=12, font_weight='bold', edge_color='gray')
# # # plt.title("Tetrahedral Graph")
# # # plt.show()
# #
# # G = nx.Graph()
# # G.add_nodes_from([0,1,2,3])
# # G.add_edge(1,3, length = (math.sqrt(6)))
# # G.add_edge(1,2, length = (math.sqrt(6)))
# # G.add_edge(1,0, length = (math.sqrt(6)))
# # G.add_edge(0,2, length = 2)
# # G.add_edge(0,3, length = 2)
# # G.add_edge(2,3, length = 2)
# #
# # pos = nx.planar_layout(G)
# # nx.draw(G, pos)
# # nx.draw(G, pos, with_labels= True, node_color='skyblue', node_size=150, font_size=12, font_weight='bold', edge_color='gray')
# # nx.draw_networkx_edge_labels(G, pos)
# # plt.show()
#
# G = nx.Graph()
# G.add_nodes_from(range(0,9))
# G.add_edge(0,1,length=2)
# G.add_edge(1,2,length=2)
# G.add_edge(2,3,length=2)
# G.add_edge(3,4,length=2)
# G.add_edge(4,5,length=2)
# G.add_edge(5,0,length=2)
# G.add_edge(5,6,length=0.726)
# G.add_edge(1,7,length=0.726)
# G.add_edge(3,8,length=0.726)
# G.add_edge(2,7,length=1.754)
# G.add_edge(0,7,length=1.754)
# G.add_edge(0,6,length=1.754)
# G.add_edge(4,6,length=1.754)
# G.add_edge(4,8,length=1.754)
# G.add_edge(8,2,length=1.754)
# G.add_edge(6,8,length=2.208)
# G.add_edge(7,8,length=2.208)
# G.add_edge(6,7,length=2.208)
#
# pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels= True, node_color='skyblue', node_size=150, font_size=12, font_weight='bold', edge_color='gray')
# # nx.draw_networkx_edge_labels(G, pos)
# # plt.show()
#
#
# T1 = nx.Graph()
# T1.add_nodes_from([0, 1, 9, 10])
# height = math.sqrt(2/3)*2
# T1.add_edge(10,9, length = height)
# T1.add_edge(9,1, length = height)
# T1.add_edge(0,9, length = height)
# T1.add_edge(0,1, length = 2)
# T1.add_edge(0,10, length = 2)
# T1.add_edge(10,1, length = 2)
# pos = nx.planar_layout(T1)
# nx.draw(T1, pos, with_labels= True, node_color='skyblue', node_size=150, font_size=12, font_weight='bold', edge_color='gray')
#
# GT1 = nx.compose(G,T1)
# pos = nx.spring_layout(GT1)
# nx.draw(GT1, pos, with_labels= True, node_color='skyblue', node_size=150, font_size=12, font_weight='bold', edge_color='gray')
# # plt.show()
#
# T2 = nx.Graph()
# T2.add_nodes_from([1, 2, 11, 12])
# height = math.sqrt(2/3)*2
# T2.add_edge(11,2, length = height)
# T2.add_edge(11,1, length = height)
# T2.add_edge(11,12, length = height)
# T2.add_edge(1,2, length = 2)
# T2.add_edge(2,12, length = 2)
# T2.add_edge(12,1, length = 2)
# pos = nx.planar_layout(T2)
# nx.draw(T2, pos, with_labels = True, node_color='skyblue', node_size=150, font_size=12, font_weight='bold', edge_color='gray')
#
# GT1T2 = nx.compose(GT1,T2)
# pos = nx.spring_layout(GT1T2)
# nx.draw(GT1T2, pos, with_labels= True, node_color='skyblue', node_size=150, font_size=12, font_weight='bold', edge_color='gray')
# # plt.show()
#
# H = nx.Graph()
# H.add_nodes_from([10, 1, 12, 21, 22, 23, 24, 25, 26])
# H.add_edge(10, 1,length=2)
# H.add_edge(10,21,length=2)
# H.add_edge(21,22,length=2)
# H.add_edge(22,23,length = 2)
# H.add_edge(23,12,length=2)
# H.add_edge(12,1,length=2)
# H.add_edge(10,25,length=0.726)
# H.add_edge(22,24,length=0.726)
# H.add_edge(12,26,length=0.726)
# H.add_edge(21,25,length=1.754)
# H.add_edge(21,24,length=1.754)
# H.add_edge(24,23, length=1.754)
# H.add_edge(23,26,length=1.754)
# H.add_edge(26,1, length=1.754)
# H.add_edge(1,25,length=1.754)
# H.add_edge(25,24,length=2.208)
# H.add_edge(24,26, length=2.208)
# H.add_edge(26,25,length=2.208)
# pos = nx.spring_layout(H)
# nx.draw(H, pos, with_labels= True, node_color='skyblue', node_size=150, font_size=12, font_weight='bold', edge_color='gray')
#
# GT1T2H = nx.disjoint_union(GT1T2,H)
# pos = nx.spring_layout(GT1T2H)
# nx.draw(GT1T2H, pos, with_labels= False, node_color='skyblue', node_size=150, font_size=12, font_weight='bold', edge_color='gray')
# plt.show()
#
# # T1 = nx.Graph()
# # T1.add_nodes_from([0, 1, 9, 10])
# # height = math.sqrt(2/3)*2
# # T1.add_edge(10,9, length = height)
# # T1.add_edge(9,1, length = height)
# # T1.add_edge(0,9, length = height)
# # T1.add_edge(0,1, length = 2)
# # T1.add_edge(0,10, length = 2)
# # T1.add_edge(10,1, length = 2)
# # pos = nx.planar_layout(T1)
# # nx.draw(T1, pos, with_labels= True, node_color='skyblue', node_size=150, font_size=12, font_weight='bold', edge_color='gray')
# # nx.draw_networkx_edge_labels(T1, pos)
# # plt.show()




import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import LineString

def pointed_star():
    # Number of outer nodes (points of the star)
    n = 5

    # Create a complete graph for the outer nodes
    outer_star = nx.complete_graph(n)

    # Create a star graph for the central hub
    hub = nx.star_graph([0])

    # Combine the hub and the outer nodes
    pointed_star = nx.compose(hub, outer_star)

    # Set positions for the nodes in the outer star
    outer_positions = nx.circular_layout(outer_star)

    # Set positions for the central hub
    hub_position = {0: (0, 0)}

    # Merge positions
    positions = {**hub_position, **outer_positions}

    # Set the positions in the graph
    nx.set_node_attributes(pointed_star, positions, 'pos')

    # List to store intersection nodes to be added
    intersection_nodes = []

    # Iterate through all pairs of adjacent edges to find intersection points
    for u, v in pointed_star.edges():
        for x, y in pointed_star.edges():
            if (u, v) != (x, y):
                # Create LineString objects from the edge endpoints
                line1 = LineString([pointed_star.nodes[u]['pos'], pointed_star.nodes[v]['pos']])
                line2 = LineString([pointed_star.nodes[x]['pos'], pointed_star.nodes[y]['pos']])
                # Check if the two edges intersect
                intersection = line1.intersection(line2)
                if intersection.is_empty:
                    continue
                # If intersection is a point, add it to the list
                if intersection.geom_type == 'Point':
                    intersection_nodes.append((intersection.x, intersection.y))

    # Add intersection nodes to the graph
    for node in intersection_nodes:
        pointed_star.add_node(node, pos=node)

    # Relabel nodes
    nx.relabel_nodes(pointed_star, {(0.3090169521873281, 0.9510565683560541): 5}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.8090170564954595, 0.587785261505403): 6}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.11803401806840924, 0.36327126674823906): 7}, copy=False)
    nx.relabel_nodes(pointed_star, {(0.3090170091047043, 0.22451397931316094): 8}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.809016996890813, -0.5877853211100496): 9}, copy=False)
    nx.relabel_nodes(pointed_star, {(0.30901704428157445, -0.22451399804788014): 10}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.11803392502284099, -0.36327128532288977): 11}, copy=False)
    nx.relabel_nodes(pointed_star, {(0.3090171011989445, -0.9510565087514076): 12}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.3819660075375347, 6.783278650309795e-09): 13}, copy=False)

    # Remove nodes and edges
    nodes_to_remove = [9, 5, 12, 6, (1.0, 0.0)]
    edges_to_remove = [(1, 2), (1, 0), (0, 4), (4, 3), (3, 2), (1, 4), (3, 1), (4, 2), (1, 9), (3, 1), (2, 0), (1, 4), (9, 0), (0, 3)]
    pointed_star.remove_nodes_from(nodes_to_remove)
    pointed_star.remove_edges_from(edges_to_remove)

    pointed_star.add_edge(2,7)
    pointed_star.add_edge(2,13)
    pointed_star.add_edge(1,7)
    pointed_star.add_edge(1,8)
    pointed_star.add_edge(8,0)
    pointed_star.add_edge(0,10)
    pointed_star.add_edge(10,4)
    pointed_star.add_edge(4,11)
    pointed_star.add_edge(11,3)
    pointed_star.add_edge(3,13)

    # Print edges with the nodes they are connecting
    print("Edges:")
    for edge in pointed_star.edges():
        print(f"Edge: {edge}, Nodes: {edge[0]}, {edge[1]}")

    # Visualize the graph
    plt.figure(figsize=(8, 8))
    pos = nx.get_node_attributes(pointed_star, 'pos')
    nx.draw_networkx(pointed_star, pos, with_labels=True, node_color='skyblue', node_size=1000, font_size=12)
    nx.draw_networkx_edges(pointed_star, pos, edge_color='black')  # Draw edges
    plt.title("Pointed Star Lattice with Nodes at Intersections")
    return plt.show()

pointed_star()


def pointed_star_with_2_pentagons():
     # Number of outer nodes (points of the star)
    n = 5

    # Create a complete graph for the outer nodes
    outer_star = nx.complete_graph(n)

    # Create a star graph for the central hub
    hub = nx.star_graph([0])

    # Combine the hub and the outer nodes
    pointed_star = nx.compose(hub, outer_star)

    # Set positions for the nodes in the outer star
    outer_positions = nx.circular_layout(outer_star)

    # Set positions for the central hub
    hub_position = {0: (0, 0)}

    # Merge positions
    positions = {**hub_position, **outer_positions}

    # Set the positions in the graph
    nx.set_node_attributes(pointed_star, positions, 'pos')

    # List to store intersection nodes to be added
    intersection_nodes = []

    # Iterate through all pairs of adjacent edges to find intersection points
    for u, v in pointed_star.edges():
        for x, y in pointed_star.edges():
            if (u, v) != (x, y):
                # Create LineString objects from the edge endpoints
                line1 = LineString([pointed_star.nodes[u]['pos'], pointed_star.nodes[v]['pos']])
                line2 = LineString([pointed_star.nodes[x]['pos'], pointed_star.nodes[y]['pos']])
                # Check if the two edges intersect
                intersection = line1.intersection(line2)
                if intersection.is_empty:
                    continue
                # If intersection is a point, add it to the list
                if intersection.geom_type == 'Point':
                    intersection_nodes.append((intersection.x, intersection.y))

    # Add intersection nodes to the graph
    for node in intersection_nodes:
        pointed_star.add_node(node, pos=node)

    # Relabel nodes
    nx.relabel_nodes(pointed_star, {(0.3090169521873281, 0.9510565683560541): 5}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.8090170564954595, 0.587785261505403): 6}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.11803401806840924, 0.36327126674823906): 7}, copy=False)
    nx.relabel_nodes(pointed_star, {(0.3090170091047043, 0.22451397931316094): 8}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.809016996890813, -0.5877853211100496): 9}, copy=False)
    nx.relabel_nodes(pointed_star, {(0.30901704428157445, -0.22451399804788014): 10}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.11803392502284099, -0.36327128532288977): 11}, copy=False)
    nx.relabel_nodes(pointed_star, {(0.3090171011989445, -0.9510565087514076): 12}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.3819660075375347, 6.783278650309795e-09): 13}, copy=False)

    # Remove nodes and edges
    nodes_to_remove = [9, 5, 12, 6, (1.0, 0.0)]
    edges_to_remove = [(1, 2), (1, 0), (0, 4), (4, 3), (3, 2), (1, 4), (3, 1), (4, 2), (1, 9), (3, 1), (2, 0), (1, 4),
                       (9, 0), (0, 3)]
    pointed_star.remove_nodes_from(nodes_to_remove)
    pointed_star.remove_edges_from(edges_to_remove)

    pointed_star.add_edge(2, 7)
    pointed_star.add_edge(2, 13)
    pointed_star.add_edge(1, 7)
    pointed_star.add_edge(1, 8)
    pointed_star.add_edge(8, 0)
    pointed_star.add_edge(0, 10)
    pointed_star.add_edge(10, 4)
    pointed_star.add_edge(4, 11)
    pointed_star.add_edge(11, 3)
    pointed_star.add_edge(3, 13)

    # # Print edges with the nodes they are connecting
    # print("Edges:")
    # for edge in pointed_star.edges():
    #     print(f"Edge: {edge}, Nodes: {edge[0]}, {edge[1]}")
    #
    # # Visualize the graph
    # plt.figure(figsize=(8, 8))
    pos_star = nx.get_node_attributes(pointed_star, 'pos')
    nx.draw_networkx(pointed_star, pos_star, with_labels=True, node_color='skyblue', node_size=1000, font_size=12)
    # nx.draw_networkx_edges(pointed_star, pos_star, edge_color='black')  # Draw edges
    # plt.title("Pointed Star Lattice with Nodes at Intersections")
    # plt.show()

    # Define the positions of the existing nodes
    positions = {
        0: (1.0, 0.0),
        1: (0.30901695, 0.95105657),
        8: (0.3090170091047043, 0.22451397931316094),
    }

    # Calculate the distance between nodes 1 and 8
    distance_18 = math.sqrt((positions[1][0] - positions[8][0]) ** 2 + (positions[1][1] - positions[8][1]) ** 2)
    angle = math.atan2(positions[0][1] - positions[1][1], positions[0][0] - positions[1][0]) - math.atan2(
        positions[8][1] - positions[1][1], positions[8][0] - positions[1][0])

    # Calculate the distance between nodes 1 and 0
    distance = math.sqrt((positions[1][0] - positions[0][0]) ** 2 + (positions[1][1] - positions[0][1]) ** 2)

    # Calculate the angle between edge (1, 8) and the x-axis
    angle_18 = math.atan2(positions[8][1] - positions[1][1], positions[8][0] - positions[1][0])

    # Calculate the coordinates of node 14 to form a regular pentagon
    x_14 = positions[8][0] + distance * math.cos(angle)
    y_14 = positions[8][1] + distance * math.sin(angle)

    # Calculate the angle between edge (1, 0) and the x-axis
    angle_10 = math.atan2(positions[0][1] - positions[1][1], positions[0][0] - positions[1][0])

    # Calculate the coordinates of node 15 to form a regular pentagon
    x_15 = positions[0][0] + distance_18 * math.cos(angle_10)
    y_15 = positions[0][1] + distance_18 * math.sin(angle_10)

    # Define positions of nodes 14 and 15
    additional_positions = {
        14: (x_14 - .25, y_14 + .25),  # Adjust y-coordinate to be above other nodes
        15: (x_15, -y_15),  # Adjust y-coordinate to be above other nodes
    }

    # Create a new graph
    G = nx.Graph()

    # Add nodes
    G.add_nodes_from(positions.keys())
    G.add_nodes_from(additional_positions.keys())

    # Add edges to form a regular pentagon
    pentagon_edges = [(0, 8), (1, 8), (1, 14), (14, 15), (15, 0)]
    G.add_edges_from(pentagon_edges)

    # Combine positions
    positions.update(additional_positions)

    C = nx.compose(G, pointed_star)
    pos = {0: (1.0, 0.0),
           1: (0.30901695, 0.95105657),
           8: (0.3090170091047043, 0.22451397931316094),
           14: (1.0100736353166142, 1.1654969519440987),
           15: (1.427051022134677, 0.5877853014287399),
           2: (-0.80901706, 0.58778526),
           3: (-0.809017, -0.58778532),
           4: (0.3090171, -0.95105651),
           7: (-0.11803401806840924, 0.36327126674823906),
           8: (0.3090170091047043, 0.22451397931316094),
           10: (0.30901704428157445, -0.22451399804788014),
           11: (-0.11803392502284099, -0.36327128532288977),
           13: (-0.3819660075375347, 6.783278650309795e-09)}
    nx.draw(C,pos = pos, with_labels=True, node_color='skyblue', node_size=500, font_size=12)
    positions2 = {
         0: (1.0, 0.0),
         10: (0.30901704428157445, -0.22451399804788014),
         4: (0.3090171, -0.95105651),
    }
    x140_transform = positions[14][0] - positions[0][0]
    y140_transform = positions[14][1] - positions[0][1]
    y1415_transform = positions[14][1] - positions[15][1]
    x1415_transform = positions[14][0] - positions[15][0]

    # Calculate the coordinates of node 14 to form a regular pentagon
    x_16 = pos_star[0][0] - x1415_transform
    y_16 = pos_star[0][1] - y1415_transform

    x_17 = pos_star[0][0] - x140_transform
    y_17 = pos_star[0][1] - y140_transform

    additional_positions = {
         16: (x_16, y_16),  # Adjust y-coordinate to be above other nodes
         17: (x_17, y_17),  # Adjust y-coordinate to be above other nodes
    }

    # Create a new graph
    G2 = nx.Graph()

    # Add nodes
    G2.add_nodes_from(positions2.keys())
    G2.add_nodes_from(additional_positions.keys())

    # Add edges to form a regular pentagon
    pentagon_edges = [(0, 10), (10, 4), (4, 17), (17, 16), (16, 0)]
    G2.add_edges_from(pentagon_edges)

    # Combine positions
    positions2.update(additional_positions)

    D = nx.compose(G2, C)
    pos = {0: (1.0, 0.0),
            1: (0.30901695, 0.95105657),
            8: (0.3090170091047043, 0.22451397931316094),
            14: (1.0100736353166142, 1.1654969519440987),
            15: (1.427051022134677, 0.5877853014287399),
            2: (-0.80901706, 0.58778526),
            3: (-0.809017, -0.58778532),
            4: (0.3090171, -0.95105651),
            7: (-0.11803401806840924, 0.36327126674823906),
            8: (0.3090170091047043, 0.22451397931316094),
            10: (0.30901704428157445, -0.22451399804788014),
            11: (-0.11803392502284099, -0.36327128532288977),
            13: (-0.3819660075375347, 6.783278650309795e-09),
            16: (1.4169773868180628, -0.5777116505153589),
            17: (0.9899263646833858, -1.1654969519440987)}

    nx.draw(D, pos=pos, with_labels=True, node_color='skyblue', node_size=500, font_size=12)
    return plt.show()

pointed_star_with_2_pentagons()



def better_code():
    # Number of outer nodes (points of the star)
    n = 5

    # Create a complete graph for the outer nodes
    outer_star = nx.complete_graph(n)

    # Create a star graph for the central hub
    hub = nx.star_graph([0])

    # Combine the hub and the outer nodes
    pointed_star = nx.compose(hub, outer_star)

    # Set positions for the nodes in the outer star
    outer_positions = nx.circular_layout(outer_star)

    # Set positions for the central hub
    hub_position = {0: (0, 0)}

    # Merge positions
    positions = {**hub_position, **outer_positions}

    # Set the positions in the graph
    nx.set_node_attributes(pointed_star, positions, 'pos')

    # List to store intersection nodes to be added
    intersection_nodes = []

    # Iterate through all pairs of adjacent edges to find intersection points
    for u, v in pointed_star.edges():
        for x, y in pointed_star.edges():
            if (u, v) != (x, y):
                # Create LineString objects from the edge endpoints
                line1 = LineString([pointed_star.nodes[u]['pos'], pointed_star.nodes[v]['pos']])
                line2 = LineString([pointed_star.nodes[x]['pos'], pointed_star.nodes[y]['pos']])
                # Check if the two edges intersect
                intersection = line1.intersection(line2)
                if intersection.is_empty:
                    continue
                # If intersection is a point, add it to the list
                if intersection.geom_type == 'Point':
                    intersection_nodes.append((intersection.x, intersection.y))

    # Add intersection nodes to the graph
    for node in intersection_nodes:
        pointed_star.add_node(node, pos=node)

    # Relabel nodes
    nx.relabel_nodes(pointed_star, {(0.3090169521873281, 0.9510565683560541): 5}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.8090170564954595, 0.587785261505403): 6}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.11803401806840924, 0.36327126674823906): 7}, copy=False)
    nx.relabel_nodes(pointed_star, {(0.3090170091047043, 0.22451397931316094): 8}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.809016996890813, -0.5877853211100496): 9}, copy=False)
    nx.relabel_nodes(pointed_star, {(0.30901704428157445, -0.22451399804788014): 10}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.11803392502284099, -0.36327128532288977): 11}, copy=False)
    nx.relabel_nodes(pointed_star, {(0.3090171011989445, -0.9510565087514076): 12}, copy=False)
    nx.relabel_nodes(pointed_star, {(-0.3819660075375347, 6.783278650309795e-09): 13}, copy=False)

    # Remove nodes and edges
    nodes_to_remove = [9, 5, 12, 6, (1.0, 0.0)]
    edges_to_remove = [(1, 2), (1, 0), (0, 4), (4, 3), (3, 2), (1, 4), (3, 1), (4, 2), (1, 9), (3, 1), (2, 0), (1, 4),
                       (9, 0), (0, 3)]
    pointed_star.remove_nodes_from(nodes_to_remove)
    pointed_star.remove_edges_from(edges_to_remove)

    pointed_star.add_edge(2, 7)
    pointed_star.add_edge(2, 13)
    pointed_star.add_edge(1, 7)
    pointed_star.add_edge(1, 8)
    pointed_star.add_edge(8, 0)
    pointed_star.add_edge(0, 10)
    pointed_star.add_edge(10, 4)
    pointed_star.add_edge(4, 11)
    pointed_star.add_edge(11, 3)
    pointed_star.add_edge(3, 13)

    nx.relabel_nodes(pointed_star,mapping={7:5,8:6,10:7,11:8,13:9})
    # Print edges with the nodes they are connecting
    print("Edges:")
    for edge in pointed_star.edges():
        print(f"Edge: {edge}, Nodes: {edge[0]}, {edge[1]}")

    # Visualize the graph
    plt.figure(figsize=(8, 8))
    pos_star = nx.get_node_attributes(pointed_star, 'pos')
    # nx.draw_networkx(pointed_star, pos_star, with_labels=True, node_color='skyblue', node_size=1000, font_size=12)
    # nx.draw_networkx_edges(pointed_star, pos_star, edge_color='black')  # Draw edges
    # plt.title("Pointed Star Lattice with Nodes at Intersections")
    # return plt.show()

    x18 = pos_star[1][0]-pos_star[8][0]
    y18 = pos_star[1][1]-pos_star[8][1]
    x80 = pos_star[8][0] - pos_star[0][0]
    y80 = pos_star[8][1] - pos_star[0][1]
    x313 = pos_star[13][0]-pos_star[3][0]
    y313 = pos_star[13][1]-pos_star[3][1]
    x311 = pos_star[3][0]-pos_star[11][0]
    y311 = pos_star[11][1]-pos_star[3][1]
    x411 = pos_star[11][0] - pos_star[4][0]
    y411 = pos_star[11][1] - pos_star[4][1]

    additional_positions = {
        14: (pos_star[1][0]+x313-(.5*x80),pos_star[1][1]+y313-(y80)),
        15: (pos_star[0][0]+x313,pos_star[0][1]+y313),
        16: (pos_star[0][0]+x18,pos_star[0][1]-y18),
        17: (pos_star[4][0]+x80,pos_star[4][1]+y80),
    }
    pentagon_edges = [(0, 15), (15, 14), (14, 1), (4, 17), (17, 16), (16, 0)]
    pointed_star.add_edges_from(pentagon_edges)

    pos_star.update(additional_positions)
    nx.draw(pointed_star,pos_star, with_labels=True, node_color='skyblue', node_size=50, font_size=12)
    plt.show()
better_code()