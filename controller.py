import networkx as nx
from functionality import func1, func2, func3, func4, func5

def functionality(id, graph: nx.Graph, N: int = None, **kwargs):
        """
        This method acts as an interface to all the functionalities for the backend implementation.
        :parameter id: The id of the requested functionality.
        :parameter graph: The graph to use for the functionalities.
        :parametert N: The number of top nodes to consider to build a subgraph to work on. If not passed, the
            functionalities will work on the complete graph.
        :parameter kwargs: Additional keyword arguments which are then passed to the specific functionalities.
        """
        if id == 1:
            return func1(graph, kwargs['graph_name'])
        elif id == 2:
            return func2(graph, kwargs['node'], kwargs['graph_name'])
        elif id == 3:
            return func3(graph, kwargs['authors_a'], kwargs['a_1'], kwargs['a_n'], N)
        elif id == 4:
            return func4(graph, kwargs['source'], kwargs['sink'], kwargs['top_n'])
        elif id == 5:
            return func5(graph, N, kwargs['paper1'], kwargs['paper2'])
        else:
            raise ValueError('There is no functionality for the chosen id.')