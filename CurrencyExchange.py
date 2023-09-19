from math import log

#Currency graph class containing nodes, edges, and a currency index.

class CurrencyGraph:
    def __init__(self, exchange_rates):
        self.n = len(exchange_rates)
        self.exchange_rates = exchange_rates
        self.currency_index = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}

        #Set the graphs Nodes.
        self.nodes = [self.currency_index[i] for i in range(self.n)]
        
        #Set the graph's edges ignoring any edge to itself.
        #Each edge represents the directed connection from u to v with weight w.
        self.edges = []
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    self.edges.append((self.currency_index[i], self.currency_index[j], -log(exchange_rates[i][j])))


    #Print function for information about the graph.
    def print_graph(self):
        
        print("The following Graph has: ")
        print("Nodes:")
        print(self.nodes)

        print("\nEdges: ")
        for edge in self.edges:
            print(f"{edge[0]} -> {edge[1]} Weight = {edge[2]:.6f}")

        print()


#Test cases as adjacency matrices.
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

graph1 = CurrencyGraph(exchange_rates1)
graph2 = CurrencyGraph(exchange_rates2)
graph3 = CurrencyGraph(exchange_rates3)

graph1.print_graph()
graph2.print_graph()
graph3.print_graph()


def bellman_ford(exchange_rate, source):
    pass 
