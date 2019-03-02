import networkx as nx
from graph import *

def heuristics_():
    pass

if __name__ == "__main__":
    graph = nx.Graph()

    import_graph_from(graph=graph, path="../graph-generator/graph.txt")
    
    write_graph(graph)