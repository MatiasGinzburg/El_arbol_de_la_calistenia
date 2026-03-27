import pandas as pd
import networkx as nx
import numpy as np
import json
from networkx.readwrite import json_graph

# 1. Load the data from a csv 
file_name = "matrizEjercicios-full"
matriz_ejercicios = pd.read_csv(file_name+'.csv', index_col=0)


# 2. Create the Directed Graph
# NetworkX interprets rows as 'source' and columns as 'target'

# Replace Nan with 0 so NetworkX ignores them
matriz_masked = matriz_ejercicios.replace(np.nan, 0)

# Create the graph (it will only create edges for non 0 values)
G = nx.from_pandas_adjacency(matriz_masked, create_using=nx.DiGraph)


# There should be no cycles in the graph, we check this

# 5. Find and print cycles (we dont want any cycle)
cycles = list(nx.simple_cycles(G))


if not cycles:
	print("The graph is a Directed Acyclic Graph (DAG) - No cycles found.")
	layers = list(nx.topological_generations(G)) # Stratifies a DAG into generations

	#Assign the position of each node (Is this the best vissual way to distribute them ?)
	pos = {node: (node_idx - len(nodes) / 2, layer_idx) 
	       for layer_idx, nodes in enumerate(layers) 
	       for node_idx, node in enumerate(nodes)}

	
	nx.set_node_attributes(G, pos, 'pos')

	reps = {node: 0 for node in G.nodes()}

	nx.set_node_attributes(G, reps, 'reps')

	# Save
	data = json_graph.node_link_data(G)
	with open(file_name+".json", "w") as f:
	    json.dump(data, f)
	print("Saved in ", file_name+".json")
# Load
# with open("[file_name].json", "r") as f:
#     data = json.load(f)
#     G = json_graph.node_link_graph(data)

else: # If there are cycles
    print(f"Found {len(cycles)} closed circles (cycles):")
    for i, cycle in enumerate(cycles, 1):
        # We append the first node to the end to visually show the 'loop'
        print(f"Cycle {i}: {' -> '.join(map(str, cycle))} -> {cycle[0]}")
