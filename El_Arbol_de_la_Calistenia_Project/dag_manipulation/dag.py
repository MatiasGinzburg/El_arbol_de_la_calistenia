import networkx as nx
import matplotlib.pyplot as plt

def get_pos(G):
    # 1. Group nodes by their topological generation (layer)
    layers = list(nx.topological_generations(G))
    
    pos = {}
    for layer_idx, nodes in enumerate(layers):
        # 2. Spread nodes out horizontally centered around x=0
        for node_idx, node in enumerate(nodes):
            # FIXED: Changed ':' to '=' for dictionary assignment
            pos[node] = (node_idx - len(nodes) / 2, layer_idx)
            
    return pos

def get_untangled_pos(G):
    # 1. Get layers
    layers = list(nx.topological_generations(G))
    pos = {}
    
    # 2. Initial horizontal positions for the first layer
    for i, node in enumerate(layers[0]):
        pos[node] = (i, 0)

    # 3. Sweep through layers to minimize crossings (Downwards)
    for i in range(1, len(layers)):
        current_layer = layers[i]
        
        # For each node, find the average x-position of its predecessors
        barycenters = []
        for node in current_layer:
            parents = list(G.predecessors(node))
            if parents:
                avg_x = sum(pos[p][0] for p in parents) / len(parents)
            else:
                avg_x = 0
            barycenters.append((node, avg_x))
        
        # Sort nodes by their barycenter to determine new X order
        barycenters.sort(key=lambda x: x[1])
        
        # Assign new centered positions
        layer_width = len(current_layer)
        for idx, (node, _) in enumerate(barycenters):
            pos[node] = (idx - layer_width / 2, i)
            
    return pos

def get_closest_generation_edges(G):
    # 1. Compute the transitive reduction
    # This returns a new graph with the minimum edges to maintain reachability
    TR_edges = set(nx.transitive_reduction(G).edges())
    
    # 2. Return the edges as a list of tuples
    return TR_edges




if __name__ == "__main__":
    test = 'edges'
    if test == 'pos':
        # Test here different options to decide wich oe is better
        G = nx.gnp_random_graph(10, 0.2, directed=True)
        DAG = nx.DiGraph([(u, v) for (u, v) in G.edges() if u < v]) # Ensure it's a DAG

        pos = get_pos(DAG)

        nx.draw(DAG, pos, with_labels=True, node_color='lightblue', 
                arrowsize=20, node_size=800)
        plt.show()

        pos = get_untangled_pos(DAG)

        nx.draw(DAG, pos, with_labels=True, node_color='lightblue', 
                arrowsize=20, node_size=800)
        plt.show()

        # pos = nx.drawing.nx_pydot.graphviz_layout(G, prog='dot')

        # nx.draw(DAG, pos, with_labels=True, node_color='lightblue', 
        #         arrowsize=20, node_size=800)
        # plt.show()


    if test == 'edges':
    # --- Example Usage ---
        G = nx.gnp_random_graph(10, 0.2, directed=True)
        DAG = nx.DiGraph([(u, v) for (u, v) in G.edges() if u < v]) # Ensure it's a DAG
        #DAG = nx.DiGraph([(1,2),(1,3),(2,4),(3,4),(1,4)])
        pos = get_untangled_pos(DAG)

        nx.draw(DAG,pos, with_labels=True, node_color='lightblue', 
                arrowsize=20, node_size=800)

        plt.show()

        TR_edges = get_closest_generation_edges(DAG)
        

        nx.draw(DAG, pos,edgelist=TR_edges, with_labels=True, node_color='lightblue', 
                arrowsize=20, node_size=800)
        plt.show()
