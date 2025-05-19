import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class CausalGraph(nx.DiGraph):
    """
    A class representing a causal graph using NetworkX's DiGraph.
    This class allows for the representation of nodes and edges,
    sampling from the graph, and performing interventions.
    """

    def __init__(self, nodes,edges=None,default_values=None):
        super().__init__()
        self.add_nodes_from(nodes)
        if edges is not None:
            self.add_edges_from(edges)

        self.parents = {n: [] for n in nodes}
        for p, c in self.edges:
            self.parents[c].append(p)
        self.reset(default_values)


    def sample(self, interventions=None):
        # Start with the current state
        values = self.state.copy()

        if not interventions:
            return values

        # Apply interventions
        for node, val in interventions.items():
            values[node] = val

        # Track visited to avoid cycles
        visited = set()

        # Initialize queue with directly intervened nodes
        queue = list(interventions.keys())

        while queue:
            current = queue.pop(0)
            visited.add(current)

            # For each child of the current node
            for child in self.successors(current):
                if child in interventions:
                    continue  # Skip if it's an intervened node

                # Only update if all parents have values
                parent_vals = [values[p] for p in self.parents[child] if p in values]
                if parent_vals:
                    # Example rule: average of parents
                    values[child] = sum(parent_vals) / len(parent_vals)

                if child not in visited:
                    queue.append(child)

        return values
    def reset(self,default_values=None):
      self.state = default_values.copy() if default_values else {n: 0 for n in self.nodes}

    def do(self, target, value=None):
        """Compute and return the sum of two numbers.

        Args:
            a (float): A number representing the first addend in the addition.
            b (float): A number representing the second addend in the addition.

        Returns:
            float: A number representing the arithmetic sum of `a` and `b`.
    """

        if value is None:
            value = np.random.rand()
        # Capture the state before the intervention
        pre_dist = self.state.copy()

        # Perform the intervention
        post_dist = self.sample({target: value})

        # Calculate the difference (absolute change)
        diff = {target: {n: abs(post_dist[n] - pre_dist[n]) for n in pre_dist if n != target}}

        self.state = post_dist.copy()

        return {'pre': pre_dist, 'post':post_dist, 'diff':diff}

    def display(self):
        """Visualizes the graph using NetworkX and Matplotlib."""
        plt.figure(figsize=(8, 5))
        pos = nx.circular_layout(self)  # You can choose other layouts like nx.shell_layout, nx.circular_layout, etc.

        nx.draw(self, pos, with_labels=True, node_size=700, node_color='skyblue', arrowsize=20, arrowstyle='-|>')
        plt.title("Causal Graph")
        plt.show()

        import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Test(nx.DiGraph):
    """
    A class representing a causal graph using NetworkX's DiGraph.
    This class allows for the representation of nodes and edges,
    sampling from the graph, and performing interventions.
    """

    def __init__(self, nodes,edges=None,default_values=None):
        super().__init__()
        self.add_nodes_from(nodes)
        if edges is not None:
            self.add_edges_from(edges)

        self.parents = {n: [] for n in nodes}
        for p, c in self.edges:
            self.parents[c].append(p)
        self.reset(default_values)


    def sample(self, interventions=None):
        # Start with the current state
        values = self.state.copy()

        if not interventions:
            return values

        # Apply interventions
        for node, val in interventions.items():
            values[node] = val

        # Track visited to avoid cycles
        visited = set()

        # Initialize queue with directly intervened nodes
        queue = list(interventions.keys())

        while queue:
            current = queue.pop(0)
            visited.add(current)

            # For each child of the current node
            for child in self.successors(current):
                if child in interventions:
                    continue  # Skip if it's an intervened node

                # Only update if all parents have values
                parent_vals = [values[p] for p in self.parents[child] if p in values]
                if parent_vals:
                    # Example rule: average of parents
                    values[child] = sum(parent_vals) / len(parent_vals)

                if child not in visited:
                    queue.append(child)

        return values
    def reset(self,default_values=None):
      self.state = default_values.copy() if default_values else {n: 0 for n in self.nodes}

    def do(self, target, value=None):
        """Compute and return the sum of two numbers.

        Args:
            a (float): A number representing the first addend in the addition.
            b (float): A number representing the second addend in the addition.

        Returns:
            float: A number representing the arithmetic sum of `a` and `b`.
    """

        if value is None:
            value = np.random.rand()
        # Capture the state before the intervention
        pre_dist = self.state.copy()

        # Perform the intervention
        post_dist = self.sample({target: value})

        # Calculate the difference (absolute change)
        diff = {target: {n: abs(post_dist[n] - pre_dist[n]) for n in pre_dist if n != target}}

        self.state = post_dist.copy()

        return {'pre': pre_dist, 'post':post_dist, 'diff':diff}

    def display(self):
        """Visualizes the graph using NetworkX and Matplotlib."""
        plt.figure(figsize=(8, 5))
        pos = nx.circular_layout(self)  # You can choose other layouts like nx.shell_layout, nx.circular_layout, etc.

        nx.draw(self, pos, with_labels=True, node_size=700, node_color='skyblue', arrowsize=20, arrowstyle='-|>')
        plt.title("Causal Graph")
        plt.show()