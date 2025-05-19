import random
from do_learn import CausalGraph
import itertools
import networkx as nx
from copy import deepcopy

def generate_dag(num_nodes=5, edge_prob=0.3, default_values=None):
    """
    Generates a random DAG with a given number of nodes and edge probability.

    :param num_nodes: Number of nodes in the DAG.
    :param edge_prob: Probability of an edge between two nodes (after topological sort).
    :param default_values: Optional dict of default values for nodes.
    :return: CausalGraph object representing the DAG.
    """
    nodes = [f'X{i}' for i in range(num_nodes)]

    # Random topological order
    random_order = nodes.copy()
    random.shuffle(random_order)

    edges = []
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if random.random() < edge_prob:
                # Add edge from earlier to later node to keep it acyclic
                edges.append((random_order[i], random_order[j]))

    return CausalGraph(nodes=nodes, edges=edges, default_values=default_values)

def generate_all_dags(num_nodes, adjacency_list=None):
    """
    Generates all possible DAGs based on the given adjacency list. The adjacency list specifies directed edges.
    If no edge exists between two nodes, they are not connected by an edge.

    :param num_nodes: Number of nodes.
    :param adjacency_list: List of directed edges (tuples), e.g., [('X0', 'X1'), ('X1', 'X0')].
    :return: List of CausalGraph instances that are valid DAGs.
    """
    nodes = [f'X{i}' for i in range(num_nodes)]
    possible_edges = list(itertools.permutations(nodes, 2))  # All possible directed edges

    # If adjacency_list is provided, generate graphs based on the adjacency list
    if adjacency_list is not None:
        dags = []
        for edges_subset in itertools.product(*[[(u, v), (v, u)] for u, v in adjacency_list]):
            # Create a graph for the current combination of edges
            g = CausalGraph(nodes,edges_subset)

            # Check if it's a valid DAG
            if nx.is_directed_acyclic_graph(g):
                dags.append(g)
        return dags

    # Otherwise, generate all possible DAGs based on all possible edges
    dags = []
    for k in range(len(possible_edges) + 1):
        for edges_subset in itertools.combinations(possible_edges, k):
            g = CausalGraph(nodes,edges_subset)

            # Check if it's a valid DAG
            if nx.is_directed_acyclic_graph(g):
                dags.append(g)

    return dags

def diff_to_edge_list(diff):
    keep = []
    remove = []

    for node, edges in diff.items():
        for edge, value in edges.items():
            if value > 0:
                keep.append((node, edge))
            else:
                remove.append((node, edge))

    return keep, remove

def simulate_intervention(node,graph,equivalence_class):
  graph_copy = deepcopy(graph)
  intervention = graph_copy.do(node)


  keep,remove = diff_to_edge_list(intervention['diff'])

  graphs = equivalence_class.filter_graphs(keep,remove)

  return len(graphs)

def calculate_intervention_subclasses(equivalence_class):
    """
    Computes the average intervention effect for each node across a set of graphs
    in an equivalence class, using the global simulate_intervention function.

    :param equivalence_class: An object with a `.graphs` attribute (list of graphs).
    :return: Dictionary mapping node names to their average intervention effect.
    """
    all_subclasses = []

    for graph in equivalence_class.graphs:
        subclasses = [simulate_intervention(node, graph,equivalence_class) for node in graph.nodes]
        all_subclasses.append(subclasses)

    num_graphs = len(all_subclasses)
    average_by_node = [sum(col) / num_graphs for col in zip(*all_subclasses)]

    node_names = list(equivalence_class.graphs[0].nodes)
    return {node: avg for node, avg in zip(node_names, average_by_node)}