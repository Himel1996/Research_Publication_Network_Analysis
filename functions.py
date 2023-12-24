import matplotlib.pyplot as plt
import networkx as nx

def visualize_subgraph(df,citation_graph):

    subgraph_nodes = set()

    for index, row in df.head(12).iterrows():
        subgraph_nodes.add(row['id'])

        references = str(row['references'])
        
        # Check for NaN or empty string
        if references and references != 'nan':
            references = references.split(';')

            # Add edges to the graph
            for reference in references:
                # Check that the reference is inside the df, ignore the rest
                if int(reference) in df['id'].values:
                    subgraph_nodes.add(int(reference))


    subgraph_nodes = list(subgraph_nodes)
    subgraph = citation_graph.subgraph(subgraph_nodes)


    # Set up Matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))

    # Draw the subgraph
    pos = nx.kamada_kawai_layout(subgraph)
    nx.draw(subgraph, pos, with_labels=False, node_size=15, edge_color='gray', alpha=0.8, ax=ax)

    # Customize the plot
    ax.set_title(f'Subgraph Visualization ({len(subgraph_nodes)} nodes)')
    ax.set_xlabel('X-axis label')
    ax.set_ylabel('Y-axis label')

    return fig, ax
