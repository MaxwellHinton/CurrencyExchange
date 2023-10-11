from math import log
from math import exp

# Currency graph class containing nodes, edges, and a currency index.

class CurrencyGraph:
    def __init__(self, exchange_rates):
        self.V = len(exchange_rates) #Vertices
        self.exchange_rates = exchange_rates
        self.currency_index = {0: 'A', 1: 'B', 2: 'C', 3: 'D'} #for conversion during printing

        # Set the graphs Nodes.
        self.nodes = list(range(self.V))

        # Initially set the source to None so that it can be changed later.
        self.source = None
        
        
        # Set the graph's edges ignoring any edge to itself.
        # Each edge represents the directed connection from u to v with weight w.
        # Weight w is defined as the -log(exchange rate).
        self.edges = []
        for i in range(self.V):
            for j in range(self.V):
                if i != j:
                    self.edges.append((i, j, -log(exchange_rates[i][j])))
    

    # Bellman-ford returns the distance values from the source to all nodes,
    # the predeccesors, and a flag indicating if a negative cycle is present.
    def bellman_ford(self, source):

        # Empty distance list created.
        dist = [float('inf')] * self.V
        dist[source] = 0

        # Empty list of predecessors created.
        pred = [None] * self.V

        negative_cycle = False

        # Set source node
        if source < 0 or source >= self.V:
            raise ValueError("Invalid source index")
        
        self.source = source
        pred[source] = None

        # 'Relax' all edges. Start the iteration up to V - 1 times.
        for _ in range(self.V - 1):

            for edge in self.edges:
                u, v, weight = edge

                if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    pred[v] = u


        # Check for negative cycles. Updating the flag if found.
        for edge in self.edges:
            u, v, weight = edge
            if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                negative_cycle = True
                break
            
        return dist, pred, negative_cycle


    # Function to obtain the path that yields the best conversion rate from currency X, to currency Y.
    def best_rate(self, source, destination):

        # Invoke the bellman algorithm to obtain the shortest paths and predecessors.
        dist, pred, negative_cycle = self.bellman_ford(source)

        if negative_cycle:
            print("Negative cycle has been detected. The best rate can still be computed.")

        # Convert the weight back into a rate
        best_rate = exp(-dist[destination])
        path = self.get_path(pred, source, destination)

        return best_rate, path

    
        
    # Print function for information about the graph.
    def print_graph(self):
        
        print("The following Graph has: ")
        print("Nodes:")
        print(self.nodes)

        print("\nEdges: ")
        for edge in self.edges:
            print(f"{edge[0]} -> {edge[1]} Weight = {edge[2]:.6f}")

        print()

    def get_path(self, pred, source, destination):
        path = []

        while destination is not None and destination != source:
            path.append(self.currency_index[destination])  # Convert the index to currency label
            destination = pred[destination]

        if destination is None:
            print("Path not found.")
            return []

        path.append(self.currency_index[source])  # Add the source node to the path
        path.reverse()

        return path

# Test cases
# Adjacency matrixes with exchange rates.
exchange_rates1 = [
    [1, 0.651, 0.581],
    [1.531, 1, 0.952],
    [1.711, 1.049, 1]
]

exchange_rates2 = [
    [1, 0.745, 0.670, 1.560],
    [1.341, 1, 1.300, 1.080],
    [1.493, 0.769, 1, 0.890],
    [0.641, 0.926, 1.124, 1]
]

exchange_rates3 = [
    [1, 0.832, 1.6982],
    [1.201, 1, 1.419],
    [0.591, 0.704, 1]
]

def print_all(graph, best_rate, path):
        print("The following Graph has: ")
        print("Nodes:")
        print(graph.nodes)

        print("\nEdges: ")
        for edge in graph.edges:
            print(f"{edge[0]} -> {edge[1]} Weight = {edge[2]:.6f}")

        print()

        source = path[0]
        destination = path[-1]

        print(f"The best rate for the conversion from {source} to {destination} is: {best_rate}")
        print(f"The path to obtain this rate is: {path}")

graph1 = CurrencyGraph(exchange_rates1)
#graph2 = CurrencyGraph(exchange_rates2)
#graph3 = CurrencyGraph(exchange_rates3)

#graph1.print_graph()
#graph2.print_graph()
#graph3.print_graph()


best_rate, path = graph1.best_rate(0, 1)

print_all(graph1, best_rate, path)


