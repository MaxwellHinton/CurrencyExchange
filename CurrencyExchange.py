from math import log
from math import exp

# Currency graph class containing nodes, edges, and a currency index.

# Decimal precision is set to 6.
PRECISION = 6

class CurrencyGraph:
    def __init__(self, exchange_rates):
        self.V = len(exchange_rates) #Vertices
        self.exchange_rates = exchange_rates
        self.negative_cycle = False

        # Set the graphs Nodes.
        self.vertices = list(range(self.V))

        # Initially set the source to None so that it can be changed later.
        self.source = None
        
        # Set the graph's edges ignoring any edge to itself.
        # Each edge represents the directed connection from u to v with weight w.
        # Weight w is defined as the -log(exchange rate), rounded to 6 decimal places.
        self.edges = []
        for i in range(self.V):
            for j in range(self.V):
                if i != j:
                    weight = round(-log(exchange_rates[i][j]), PRECISION)
                    self.edges.append((i, j, weight))
    

    # Bellman-ford returns the distance values from the source to all nodes,
    # the predeccesors, and a flag indicating if a negative cycle is present.
    def bellman_ford(self, source):

        # Empty distance list created.
        dist = [float('inf')] * self.V
        dist[source] = 0

        # Empty list of predecessors created.
        pred = [None] * self.V

        # Cycle variable for arbitrage cycles.
        cycle = None

        # Set source node
        if source < 0 or source >= self.V:
            raise ValueError("Invalid source index")
        
        self.source = source
        pred[source] = None

        # 'Relax' all edges. Start the iteration up to V - 1 times.
        for _ in range(self.V - 1):

            for edge in self.edges:
                u, v, weight = edge
                
                future_dist = round(dist[u] + weight, PRECISION)
                current_dist = round(dist[v], PRECISION)

                if dist[u] != float('inf') and future_dist < current_dist:
                    dist[v] = future_dist
                    pred[v] = u

        # Check for negative cycles. Updating the flag if found.
        for edge in self.edges:

            u, v, weight = edge
            future_dist = round(dist[u] + weight, PRECISION)
            current_dist = round(dist[v], PRECISION)

            if dist[u] != float('inf') and future_dist < current_dist:

                self.negative_cycle = True   

                 
                cycle = [v]

                # Create a visited set to avoid inf loop.
                visited = set() 

                while u not in visited:
                    visited.add(u)
                    u = pred[u]
                    cycle.append(u)

                    if u == v:
                        break

                cycle.reverse()
                print(f"Cycle: {cycle}")
                # First arbitrage cycle ends the loop.
                break 
            
        return dist, pred, cycle

    def print_arbitrage_cycle(self, cycle):

        print("\nArbitrage cycle: ")
        if cycle:
            print(" -> ".join(map(str, cycle[::-1])))

    # Detects arbitrage by calling the bellman-ford method.
    def detect_arbitrage(self, source):

        # Check all vertices for arbitrage cycles.
        #for source in range(self.V):
        _, _, cycle = self.bellman_ford(source)

        if self.negative_cycle:
            self.print_arbitrage_cycle(cycle)
        else:
            print("No arbitrage cycle was detected.")
                

    def get_best_rate_and_path(self, source, destination):

        # Source and destination exist check
        if not 0 <= source < self.V or not 0 <= destination < self.V:
            raise ValueError("Invalid source or desination index.")
        
        distances, preds, _ = self.bellman_ford(source)

        if self.negative_cycle:
            print("Best rate can not be calculated due to a present negative cycle.\n")
            return None, None

        # Calculate the best conversion rate
        print(f"\nCalculating the best rate from: {str(source)} to {str(destination)}.")

        best_rate = round(exp(-distances[destination]), 6)
        print("Best rate: " + str(best_rate))

        path = self.get_path(preds, source, destination)
        print("Path: ", path)

        return best_rate, path


    # Get path function retraces the predecessors.
    # This function is only called for the non-negative cycle path.
    def get_path(self, pred, source, destination):
        path = []

        while destination is not None and destination != source:
            path.append(str(destination))
            destination = pred[destination]

        if destination is None:
            print("Path not found.")
            return []

        path.append(str(source))  # Add the source node to the path and reverse the order.
        path.reverse()

        return path
    
    # Print function for information about the graph
    def print_graph(self):
        
        print("The following Graph has: ")
        print("Vertices:")
        print(self.vertices)

        print("\nEdges: ")
        for edge in self.edges:
            print(f"{edge[0]} -> {edge[1]} Weight = {edge[2]:.6f}")

        print()

# Test cases
# Adjacency matrixes that CONTAIN a negative cycle.

exchange_rates1 = [
    [1, 0.651, 0.581],
    [1.531, 1, 0.952],
    [1.711, 1.049, 1]
] 


exchange_rates3 = [
    [1, 0.8, 0.7],  
    [1.2, 1, 0.85], 
    [1.4, 1.15, 1]   
]

# Non-negative cycle examples.
exchange_rates4 = [
    [1, 0.85, 0.75, 1.4],
    [1.18, 1, 0.88, 1.65],
    [1.33, 1.14, 1, 1.87],
    [0.71, 0.61, 0.53, 1]
]

graph4 = CurrencyGraph(exchange_rates4)
graph4.print_graph()
graph4.detect_arbitrage(0)
graph4.get_best_rate_and_path(0, 3)

graph1 = CurrencyGraph(exchange_rates1)
graph1.print_graph()
graph1.detect_arbitrage(0)

no_negative_cycle_graph = CurrencyGraph(exchange_rates3)
no_negative_cycle_graph.print_graph()
best_rate, path = no_negative_cycle_graph.get_best_rate_and_path(1,2)     # Should retrieve the best rate and path as it exists.
no_negative_cycle_graph.detect_arbitrage(0)                               # No arbitrage cycle should be detected






