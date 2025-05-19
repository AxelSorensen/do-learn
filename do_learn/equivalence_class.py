import numpy as np
import networkx as nx
import graphviz
from IPython.display import display
import matplotlib.pyplot as plt

class EquivalenceClass:
    def __init__(self, graphs, probabilities=None):
        """
        :param graphs: List of CausalGraph instances.
        :param probabilities: Optional list of floats representing the probability of each graph.
        """
        if probabilities is None:
            probabilities = [1.0 / len(graphs)] * len(graphs)
        else:
            assert len(graphs) == len(probabilities), "Each graph must have a probability"
            assert abs(sum(probabilities) - 1.0) < 1e-6, "Probabilities must sum to 1"

        self.graphs = graphs
        self.probabilities = probabilities

    def display_all(self):
        """Displays all graphs with their associated probabilities using consistent layout."""
        layout = 'dot'  # or 'circo', 'neato', etc.
        for i, (graph, prob) in enumerate(zip(self.graphs, self.probabilities)):
            print(f"Graph {i + 1} - P = {prob:.2f}")
            graph.display()


    def filter_graphs(self, keep_edges=None, remove_edges=None, update_graphs=False):
        """
        Filters graphs by removing graphs with any `remove_edges` and/or keeping
        only graphs that contain all `keep_edges`.

        :param keep_edges: List of (source, target) tuples to retain graphs that contain all of them.
        :param remove_edges: List of (source, target) tuples to discard graphs that contain any of them.
        :param update_graphs: If True, update self.graphs and self.probabilities with filtered ones.
        :raises ValueError: If no graphs match the criteria after filtering.
        """
        filtered = list(zip(self.graphs, self.probabilities))

        if remove_edges:
            filtered = [
                (g, p) for g, p in filtered
                if not any(g.has_edge(*edge) for edge in remove_edges)
            ]

        if keep_edges:
            # Only keep edges that appear in at least one graph to avoid pointless filtering
            valid_keep_edges = [
                edge for edge in keep_edges
                if any(g.has_edge(*edge) for g, _ in filtered)
            ]

            if not valid_keep_edges:
                print("⚠️ Warning: None of the requested `keep_edges` exist in any graph.")

            filtered = [
                (g, p) for g, p in filtered
                if all(g.has_edge(*edge) for edge in valid_keep_edges)
            ]

        if not filtered:
            raise ValueError("Filtering removed all graphs; check 'keep' and 'remove' edge criteria.")

        if update_graphs:
            self.graphs, self.probabilities = zip(*filtered)
            self.graphs = list(self.graphs)
            total = sum(self.probabilities)
            self.probabilities = [p / total for p in self.probabilities]

        return filtered



    def display_essential_graph(self):
        """Displays the essential graph summarizing edge consistency across all DAGs using NetworkX + Matplotlib."""
        total = len(self.graphs)
        all_nodes = set().union(*[g.nodes for g in self.graphs])

        # Count directed edge frequencies
        edge_counts = {}
        for g in self.graphs:
            for u in g.nodes:
                for v in g.nodes:
                    if u == v:
                        continue
                    edge_counts.setdefault((u, v), 0)
                    if g.has_edge(u, v):
                        edge_counts[(u, v)] += 1

        G = nx.DiGraph()
        G.add_nodes_from(all_nodes)

        seen = set()
        edge_styles = {}
        for (u, v), uv_count in edge_counts.items():
            if (v, u) in seen:
                continue
            seen.add((u, v))
            seen.add((v, u))
            vu_count = edge_counts.get((v, u), 0)

            if uv_count == total and vu_count == 0:
                G.add_edge(u, v)
                edge_styles[(u, v)] = 'solid'
            elif vu_count == total and uv_count == 0:
                G.add_edge(v, u)
                edge_styles[(v, u)] = 'solid'
            elif uv_count + vu_count == total:
                G.add_edge(u, v)
                edge_styles[(u, v)] = 'solid_undirected'
            elif uv_count > 0 and vu_count > 0:
                G.add_edge(u, v)
                edge_styles[(u, v)] = 'dashed_undirected'
            elif uv_count > 0:
                G.add_edge(u, v)
                edge_styles[(u, v)] = 'dashed'
            elif vu_count > 0:
                G.add_edge(v, u)
                edge_styles[(v, u)] = 'dashed'

        # Layout
        pos = nx.spring_layout(G, seed=42)

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
        nx.draw_networkx_labels(G, pos)

        # Draw edges by style
        for style in ['solid', 'dashed', 'solid_undirected', 'dashed_undirected']:
            edgelist = [e for e, s in edge_styles.items() if s == style]
            if not edgelist:
                continue

            if 'undirected' in style:
                nx.draw_networkx_edges(
                    G, pos, edgelist=edgelist, arrows=False, 
                    style='solid' if 'solid' in style else 'dashed'
                )
            else:
                nx.draw_networkx_edges(
                    G, pos, edgelist=edgelist,
                    style='solid' if 'solid' in style else 'dashed', arrowsize=20, arrowstyle='-|>', min_target_margin=12,
                    arrows=True
                )

        plt.axis('off')
        plt.title(f"Essential Graph - {len(self.graphs)} possible DAGs")
        plt.show()
        # How to displau the number of graphs in the essential graph
    

