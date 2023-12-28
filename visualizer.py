
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import pandas as pd

def plot_shortest_walk(graph, path):
    # Create a figure for the plot
    plt.figure(figsize=(8, 4))
    
    # Generate positions for each node
    pos = nx.spring_layout(graph)
    
    # Draw the full graph (lightly in the background)
    nx.draw_networkx_nodes(graph, pos, node_color='blue', alpha=0.3)
    nx.draw_networkx_edges(graph, pos, alpha=0.3)
    nx.draw_networkx_labels(graph, pos)
    
    # Extract the subgraph for the path
    subgraph = graph.subgraph(path)
    
    # Draw the nodes and edges of the path
    nx.draw_networkx_nodes(subgraph, pos, node_size=300, node_color='red')
    nx.draw_networkx_edges(subgraph, pos, edgelist=list(zip(path, path[1:])), edge_color='green', width=2)
    
    # Add edge labels to show the order of the walk
    edge_labels = {(path[i], path[i+1]): i+1 for i in range(len(path)-1)}
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels, label_pos=0.5, font_color='green')

    # Set plot details
    plt.title('Shortest Ordered Walk with Edge Identifiers')
    plt.axis('off')
    plt.show()

def get_papers_for_shortest_walk(G, path):
    # Initialize an empty list to hold the papers (edges) in the walk
    papers_in_walk = []

    # Iterate through the path and find the papers connecting each consecutive pair of authors
    for i in range(len(path) - 1):
        start_author = path[i]
        end_author = path[i + 1]
        
        # Retrieve the papers (or collaborations) associated with the edge
        # This assumes you have an attribute for each edge that lists the associated paper(s)
        # Adjust the attribute name as per your graph's data
        papers = G[start_author][end_author].get('titles', 'Unknown Paper')
        
        # If multiple papers are found, you might want to handle them here
        # For simplicity, we're assuming it's a single identifier
        papers_in_walk.append((start_author, end_author, papers))

    return papers_in_walk

def plot_graphs(original_graph, modified_graph, authorA, authorB, separating_edges):
    fig, axes = plt.subplots(1, 2, figsize=(24, 12))  # 1 row, 2 columns

    # Common position for both subplots
    pos = nx.spring_layout(original_graph)
    
    # Plotting the original graph
    plt.sca(axes[0])
    nx.draw_networkx_nodes(original_graph, pos, node_size=700, node_color="lightblue")
    nx.draw_networkx_edges(original_graph, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(original_graph, pos)
    nx.draw_networkx_nodes(original_graph, pos, nodelist=[authorA, authorB], node_size=700, node_color="limegreen")
    axes[0].set_title("Original Graph")

    # Plotting the graph after removing links
    plt.sca(axes[1])
    nx.draw_networkx_nodes(modified_graph, pos, node_size=700, node_color="lightblue")
    nx.draw_networkx_edges(modified_graph, pos, edgelist=modified_graph.edges, width=1.0, alpha=0.5)
    nx.draw_networkx_edges(modified_graph, pos, edgelist=separating_edges, edge_color="red", width=2)
    nx.draw_networkx_labels(modified_graph, pos)
    nx.draw_networkx_nodes(modified_graph, pos, nodelist=[authorA, authorB], node_size=700, node_color="limegreen")
    axes[1].set_title("Graph After Removing Minimum Cut Links")

    plt.tight_layout()
    plt.show()

def print_communities_table(final_communities):
    # Prepare the data for the DataFrame
    community_data = {"Community": [], "Papers": []}
    for idx, community in enumerate(final_communities):
        community_data["Community"].append(idx)
        community_data["Papers"].append(', '.join(community))
    
    # Create the DataFrame and print it
    df = pd.DataFrame(community_data)
    print(df)
def plot_original_graph(graph):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    plt.title("Original Graph")
    plt.show()
def plot_graph_with_communities(graph, final_communities):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    
    # Generate a color palette for communities
    color_map = plt.cm.get_cmap('hsv', len(final_communities))
    
    for idx, community in enumerate(final_communities):
        nx.draw_networkx_nodes(graph, pos, nodelist=list(community), node_color=[color_map(idx)] * len(community))
    nx.draw_networkx_edges(graph, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(graph, pos)
    
    plt.title("Graph Showing Communities")
    plt.show()
def plot_final_graph_and_identify_papers(graph, final_communities, paper1, paper2):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    
    # Draw all nodes and edges
    nx.draw_networkx_nodes(graph, pos, node_size=200, node_color='lightgrey')
    nx.draw_networkx_edges(graph, pos, edge_color='gray')
    
    # Highlight communities of Paper_1 and Paper_2
    for idx, community in enumerate(final_communities):
        if paper1 in community or paper2 in community:
            color = 'red' if paper1 in community else 'green'
            nx.draw_networkx_nodes(graph, pos, nodelist=list(community), node_color=color)
    
    nx.draw_networkx_labels(graph, pos)
    
    plt.title(f"Final Graph with Communities of Paper {paper1} (Red) and Paper {paper2} (Green)")
    plt.show()
