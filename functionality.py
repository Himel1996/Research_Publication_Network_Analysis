import networkx as nx
import numpy as np
import itertools
import networkx as nx
from collections import deque
from networkx.algorithms.flow import edmonds_karp
import random

def func1(graph, graph_name):
    # Calculate the basic properties
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    density = nx.density(graph)
    degree_dict = dict(graph.degree())
    average_degree = sum(degree_dict.values()) / num_nodes

    # Calculate degree distribution
    degrees = list(degree_dict.values())
    degree_distribution = np.histogram(degrees, bins=range(min(degrees), max(degrees) + 1))

    # Identify hubs: nodes with degree > 95th percentile of degrees
    percentile_95 = np.percentile(degrees, 95)
    hubs = [node for node, degree in degree_dict.items() if degree > percentile_95]

    # Determine if the graph is dense or sparse
    graph_type = 'dense' if density*100 >= 10 else 'sparse'

    return graph_name, num_nodes, num_edges, density, degree_distribution, average_degree, hubs, graph_type

def func2(graph, node, graph_name):
    # Ensure the node is in the graph
    if node not in graph:
        return f"Node {node} not found in {graph_name}."

    # Calculate centrality measures
    betweenness = nx.betweenness_centrality(graph).get(node)
    pagerank = nx.pagerank(graph).get(node)
    closeness = nx.closeness_centrality(graph).get(node)
    degree_centrality = nx.degree_centrality(graph).get(node)
    return graph_name, node, betweenness, pagerank, closeness, degree_centrality

#The Top N authors is selected on the basis of degree of nodes
def get_top_N_nodes(G, N):
    degree=dict(G.degree())
    top_n_nodes = sorted(degree.items(), key=lambda x:x[1], reverse=True)[:N]
    return top_n_nodes

def func3(G, authors_a, a_1, a_n, N):
    # Filter the graph to the top N nodes
    if N:
        top_nodes = get_top_N_nodes(G, N)  #this function is defined based on degree of nodes
        top_nodes_e0=[e[0] for e in top_nodes]
        G = G.subgraph(top_nodes_e0)
    
    # Check if initial and end nodes are in the graph
    if a_1 not in G or a_n not in G:
        return "There is no such path."
    
    # Initialize variables
    shortest_path = None
    shortest_length = float('inf')
    
    # Generate all possible orders to visit the nodes
    for order in itertools.permutations(authors_a):
        current_path = [a_1]
        current_length = 0
        
        # Traverse the graph in the specific order
        for node in order:
            if current_path[-1] == node:
                continue  # Skip if the next node is the same as the current
            try:
                # Find the shortest path to the next node in the order
                path = nx.shortest_path(G, source=current_path[-1], target=node)
                current_length += len(path) - 1  # Exclude the starting node from the count
                current_path.extend(path[1:])  # Append the path excluding the starting node
            except nx.NetworkXNoPath:
                break  # Exit if no path exists
        
        # Attempt to reach the final node
        try:
            final_path = nx.shortest_path(G, source=current_path[-1], target=a_n)
            current_length += len(final_path) - 1
            current_path.extend(final_path[1:])
            
            # Update the shortest path if the current one is shorter
            if current_length < shortest_length:
                shortest_length = current_length
                shortest_path = current_path
        except nx.NetworkXNoPath:
            continue
    
    # Return the result
    if shortest_path is None:
        return "There is no such path.", 0
    else:
        return shortest_path, shortest_length
    
def bfs_path(graph, start, end):
    # Basic BFS to find a path from start to end
    visited = set()
    queue = [(start, [start])]

    while queue:
        current, path = queue.pop(0)
        if current == end:
            return path

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None  # No path found

def bfs_shortest_ordered_walk(graph, start, end, preferred_authors, N):
    current_start = start
    complete_path = [start]

    # Traverse through each author in the preferred_authors list
    for author in preferred_authors:
        if author != current_start:  # Skip if the author is the same as the current start
            path_to_next = bfs_path(graph, current_start, author)

            if path_to_next is None or (N and len(complete_path) + len(path_to_next) - 1 > N):
                return None  # Path not found or exceeds N

            # Extend the complete path, avoiding duplication of the current start node
            complete_path.extend(path_to_next[1:])
            current_start = author

    # Final BFS from the last author in preferred_authors to end
    final_path = bfs_path(graph, current_start, end)
    if final_path is None or (N and len(complete_path) + len(final_path) - 1 > N):
        return None

    # Return the complete path including the final path
    return complete_path + final_path[1:]
def func3_GPT(graph, authors_a, a_1, a_n, N):
    path = bfs_shortest_ordered_walk(graph, a_1, a_n, authors_a, N)
    if path:
        # Return the path and its length
        return (path, len(path) - 1)
    else:
        return ("No path found", -1)



def func4(graph, source, sink, top_n):
    """
    Calculate the minimum cut between two nodes in a weighted or unweighted undirected graph using the Edmonds-Karp
    algorithm. It determines the maximum flow in the graph and utilizes BFS to identify reachable nodes from the source,
    which helps in finding the minimum cut set.
    :param graph: A NetworkX graph, either weighted undirected or unweighted undirected.
    :param source: Node identifier representing the source in the flow network.
    :param sink: Node identifier representing the sink in the flow network.
    :param top_n: The parameter to limit the analysis to the Top N nodes based on degree.
    :return: A tuple containing the number of edges in the minimum cut, the list of these edges, and the resulting
             graph after removing the edges in the cut-set.
    """
    # Determine if the graph is weighted or unweighted and adjust accordingly.
    if not nx.get_edge_attributes(graph, 'weight'):
        temp_graph = graph.copy()  # Create a copy to prevent modifications to the original graph
        nx.set_edge_attributes(temp_graph, 1, 'weight')  # Assign a default weight of 1 to all edges
        graph = temp_graph

    # Check if the source and sink are already disconnected.
    if not nx.has_path(graph, source, sink):
        print('No path exists between the two nodes; the graph is already segmented. No cuts needed.')
        return [0, [], graph]

    # If a limit is set, refine the graph to the top N most connected nodes.
    if top_n:
        significant_nodes = get_top_N_nodes(graph, top_n)  
        node_subset = [node[0] for node in significant_nodes]
        graph = graph.subgraph(node_subset)

    # Apply the Edmonds-Karp algorithm to find the residual network.
    residual_graph = edmonds_karp(graph, source, sink, 'weight')
    flows = nx.get_edge_attributes(residual_graph, 'flow')
    capacities = nx.get_edge_attributes(residual_graph, 'capacity')
    residual_capacities = {(u, v): capacities[(u, v)] - flows[(u, v)] for u, v in residual_graph.edges}

    # Use BFS to find all nodes reachable from the source in the residual graph.
    exploration_queue = deque([source])
    reachable = {source: True}
    while exploration_queue:
        current_node = exploration_queue.popleft()
        for adjacent in residual_graph.neighbors(current_node):
            if residual_capacities[(current_node, adjacent)] > 0 and not reachable.get(adjacent, False):
                reachable[adjacent] = True
                exploration_queue.append(adjacent)

    # Determine the cut sets based on the BFS exploration.
    partition_one = reachable.keys()
    partition_two = [node for node in graph.nodes if node not in partition_one]
    separating_edges = list(nx.edge_boundary(graph, partition_one, partition_two))

    # Return the size of the cut, the actual edges, and the modified graph.
    return len(separating_edges), separating_edges,\
          nx.subgraph_view(graph, filter_edge=lambda u, v: (u, v) not in separating_edges and (v, u) not in separating_edges)

def func5(G, N, paper1=None, paper2=None):
    # Make a copy of the graph
    G=G.copy()
    # Convert the directed graph to undirected
    G_undirected = G.to_undirected()

    # Calculate the degree centrality for each node and select the top N nodes
    degree_centrality = nx.degree_centrality(G_undirected)
    top_N_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:N]

    # Create a subgraph with the top N nodes
    G_top_N = G_undirected.subgraph(top_N_nodes)

    # Girvan-Newman Algorithm
    def girvan_newman_with_edge_removal_count(graph):
        G = graph.copy()
        communities = [tuple(nx.connected_components(G))]
        num_edges_removed = 0
        
        while G.number_of_edges() > 0:
            edge_betweenness = nx.edge_betweenness_centrality(G)
            max_edge = max(edge_betweenness, key=edge_betweenness.get)
            G.remove_edge(*max_edge)
            communities.append(tuple(nx.connected_components(G)))
            num_edges_removed += 1

        return communities, num_edges_removed

    # Apply the modified Girvan-Newman algorithm to the subgraph
    communities, min_edges_removed = girvan_newman_with_edge_removal_count(G_top_N)

    # Determine Community Membership
    if not paper1 or not paper2:
        # If papers are not provided, randomly select two for demonstration
        paper1, paper2 = random.sample(top_N_nodes, 2)

    community_of_paper_1 = community_of_paper_2 = None
    for idx, community in enumerate(communities[-1]):
        if paper1 in community:
            community_of_paper_1 = idx
        if paper2 in community:
            community_of_paper_2 = idx

    same_community = community_of_paper_1 == community_of_paper_2

    return {
        "community_of_paper_1": community_of_paper_1,
        "community_of_paper_2": community_of_paper_2,
        "same_community": same_community,
        "total_communities": len(communities[-1]),
        "min_edges_removed": min_edges_removed,
        "final_communities": communities[-1]
    }

