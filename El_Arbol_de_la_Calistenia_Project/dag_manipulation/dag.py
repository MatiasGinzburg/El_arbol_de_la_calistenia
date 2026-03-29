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


def assign_colors_from_atribute_old(G,atribute,v_min, color_low='red',color_high='blue'):
    """ paint the node color_low if the atribute is lower or equal than v_min and color_high otherwise"""
    colors = []
    reps = nx.get_node_attributes(G, atribute)#, default=0) #dictionary - keys = nodes, value = value of the atribute
    for node in G.nodes():        
        colors.append(color_high if reps[node] > v_min else color_low)
    
    return colors

def assign_colors_from_atribute(G,atribute,v_min, v_max=None ,color_low='red',color_standard='blue', color_high='green'): #I can improve this a lot
    """ paint the node color_low if the atribute is lower or equal than v_min and color_high otherwise"""
    colors = []
    values = nx.get_node_attributes(G, atribute)#, default=0) #dictionary - keys = nodes, value = value of the atribute
    
    if v_max == None: # there are two colors 
        for node in G.nodes():        
            colors.append(color_standard if values[node] > v_min else color_low)
    
    elif isinstance(v_max, str):
        try:    
            values_max = nx.get_node_attributes(G, v_max)
        except:
            raise ValueError("v_max is not a valid atribute from the graph")
        for node in G.nodes():
            if values[node]>=values_max[node]:
                colors.append(color_high)
            elif values[node]>v_min:
                colors.append(color_standard)
            else:
                colors.append(color_low)
    elif isinstance(v_max, int) or isinstance(v_max, float) :
        for node in G.nodes():
            if values[node]>=v_max:
                colors.append(color_high)
            elif values[node]>v_min:
                colors.append(color_standard)
            else:
                colors.append(color_low)    
    else:
        raise ValueError("v_max should be None, str , float or int")
        colors = None

    return colors



def add_max_incomig_edge_attribute(G, weight_key='weight', attr_name='max_input'):
    """
    For each node, finds the maximum value of a specific attribute 
    among all incoming edges and saves it as a node attribute.
    """
    for node in G.nodes():
        # Get all values from edges pointing to this node
        in_edge_values = [data.get(weight_key, 0) for _, _, data in G.in_edges(node, data=True)]
        
        # Calculate max (defaults to 0 if no incoming edges exist)
        max_val = max(in_edge_values) if in_edge_values else 0
        
        # Assign the value to the node
        G.nodes[node][attr_name] = max_val

def add_max_outgoing_edge_attribute(G, weight_key='weight', attr_name='max_input'):
    """
    For each node, finds the maximum value of a specific attribute 
    among all incoming edges and saves it as a node attribute.
    """
    for node in G.nodes():
        # Get all values from edges pointing to this node
        out_edge_values = [data.get(weight_key, 0) for _, _, data in G.out_edges(node, data=True)]
        
        # Calculate max (defaults to 0 if no incoming edges exist)
        max_val = max(out_edge_values) if out_edge_values else 0
        
        # Assign the value to the node
        G.nodes[node][attr_name] = max_val


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
