# Question 1

# In this question, the goal is to pinpoint a node that plays a crucial role as a "connector" within the graph.
# To achieve this, we seek to identify the node with the highest degree, as it acts as a central point linking different parts of the graph together.
# The degree of a node represents the number of edges connected to it, making the node with the highest degree a significant connector.


# First we set the file path for the citation graph data
citation_file="citation_graph.txt"

# Next we find the node with the highest degree in the citation graph
# For this purpose we will work with second column and their count

n_nodes=$(awk '{print $2}' "$citation_file" | sort | uniq -c | sort -nr)

# Determine the node with the top degree directly using awk
top_degree_node=$(awk 'NR==1 {print $2}' <<< "$n_nodes")
top_degree=$(awk 'NR==1 {print $1}' <<< "$n_nodes")

# Results

echo "Connector Node: $top_degree_node, Node Degree: $top_degree"




# Question 2

# In this question, our objective is to examine the variation in citations among the graph nodes.

# To accomplish this, we focus on the second column, counting their occurrences. After sorting them, we calculate the range.

# Results

awk '{print $2}' "$citation_file" | sort -n | uniq -c | awk 'NR==1{min=$1; max=$1} {if($1<min) min=$1; if($1>max) max=$1} END{print "The range is between:", min, "and", max}'







# Question 3

# In this question, our aim is to determine the average length of the shortest paths among nodes in the citation graph.

# To accomplish this, we start by extracting edges from the citation file, constructing a directed graph using Python and NetworkX.

# We then identify the most substantial strongly connected component within the graph, emphasizing the interconnectedness of nodes.

# A subgraph is created, containing only the nodes within this significant component, facilitating a more focused analysis.

# Finally, the average shortest path length is computed for this subgraph using NetworkX functions.

short_path_avg=$(awk '{print $1, $2}' $citation_file | sort -u | python3 -c "
import networkx as nx
import sys

# Read edges and build a directed graph
graph = nx.DiGraph()
for line in sys.stdin:
    source, target = map(int, line.split())
    graph.add_edge(source, target)

# Identify the most substantial component
subs_component = max(nx.strongly_connected_components(graph), key=len)

# Create a subgraph with only the most substantial component
main_subs_component = graph.subgraph(subs_component)

# Compute the average shortest path length
short_path_avg = nx.average_shortest_path_length(main_subs_component)
print(f'{short_path_avg:.4f}')
")

# Results
echo "The Average Length of the Shortest Path Among Nodes: $short_path_avg"
