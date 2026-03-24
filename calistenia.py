import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from itertools import combinations



matriz_ejericios = pd.read_csv('matrizEjercicios-full.csv',index_col=0)


print(matriz_ejericios)
relaciones = matriz_ejericios.isna() # Convierte la celdas vacias a TRUE y las celdas con numeros a FALSE

print(relaciones)
ejercicios_ordenados=[]

print("Escribirendo relaciones")
rSize = relaciones.size 
while relaciones.size>0:
    print(relaciones.size)
    print(relaciones)
    ejercicios = relaciones.columns
    relaciones2 = relaciones.all(axis=0) # devuelve una serie donde TRUE significa che todos son TRUE(otiginalmente vacio) y false significa que alguno es FALSE (El ejercicio tiene algun requisito)


    ejercicios_ordenados.append(ejercicios[relaciones2]) # Agrego los ejericcios que por ahora no tienen ningun ejericios_requisitos


    relaciones = relaciones.loc[~relaciones2,~relaciones2] # Me quedo solo con las filas y solumndas que que no puse en ejericicios
    rSize_new = relaciones.size
    if rSize == rSize_new:
        print("La matriz de ejercicios no es consistente, hay un loop de ejercicios")
        ejercicios_ordenados.append(relaciones.columns)
        print(ejercicios_ordenados)

        break
    else: rSize=rSize_new

ejercicios = matriz_ejericios.columns
relaciones = matriz_ejericios.notna()

print("Creando grafo")
# Create a graph object
G = nx.Graph()

# Add nodes
G.add_nodes_from(ejercicios)

ejericios_requisitos = {ej:[[],[]] for ej in ejercicios}
# Add edges
for l in range(1,len(ejercicios_ordenados)):
    for j in range(len(ejercicios_ordenados[l])):
        ej = ejercicios_ordenados[l][j]
        for lmin in range(l-1,-1,-1):
            for ej_base in ejercicios_ordenados[lmin]:
                if relaciones.loc[ej_base,ej]:
                    if ej_base in ejericios_requisitos[ej][1]:
                        pass
                    else:
                        G.add_edge(ej,ej_base)
                        ejericios_requisitos[ej][0].append(ej_base)
                        ejericios_requisitos[ej][1]=list(set(ejericios_requisitos[ej][1]+ejericios_requisitos[ej_base][0]+ejericios_requisitos[ej_base][1]))


# Draw the graph TEST 1
pos = nx.spring_layout(G)  # layout for placement
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800)
plt.show()



# Draw the graph TEST 2

def assign_pos(ejercicios_ordenados):
    pos = {}
    for l, layer in enumerate(ejercicios_ordenados):
        Nl = len(layer)
        for e, ejercicio in enumerate(layer):
            pos[ejercicio] = (e-Nl/2  , l)  
    return pos

pos = assign_pos(ejercicios_ordenados)

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800)
plt.show()


# Draw the graph TEST 5

def assign_y_positions(ejercicios_ordenados):
    """Return dict: node -> fixed y coordinate."""
    y_pos = {}
    for layer_idx, layer in enumerate(ejercicios_ordenados):
        for node in layer:
            y_pos[node] = layer_idx   # you may use +layer_idx if preferred
    return y_pos


def optimize_x_positions(G, ejercicios_ordenados):
    # All nodes in order:
    all_nodes = [node for layer in ejercicios_ordenados for node in layer]
    n = len(all_nodes)
    
    node_index = {node: i for i, node in enumerate(all_nodes)}
    
    # Initial guess (uniform spacing per layer)
    x0 = np.zeros(n)
    for layer in ejercicios_ordenados:
        k = len(layer)
        xs = np.linspace(0, k-1, k)
        for i, node in enumerate(layer):
            x0[node_index[node]] = xs[i]

    # Objective: minimize sum of (x_u - x_v)^2 over edges
    def objective(x):
        s = 0.0
        for u, v in G.edges():
            iu, iv = node_index[u], node_index[v]
            s += (x[iu] - x[iv]) ** 2
        return s

    # Small penalty for nodes in same layer collapsing into identical x
    def penalty_same_layer(x):
        p = 0.0
        for layer in ejercicios_ordenados:
            indices = [node_index[n] for n in layer]
            xs = x[indices]
            # encourage spread by adding penalty for closeness
            for i in range(len(xs)):
                for j in range(i+1, len(xs)):
                    p += 1.0 / (1e-6 + abs(xs[i] - xs[j]))
        return p * 0.001  # small weight so it only prevents collapse

    def objective_total(x):
        return objective(x) + penalty_same_layer(x)

    # Run optimization
    result = minimize(objective_total, x0)
    x_opt = result.x
    
    # Map back to node positions
    x_pos = {node: x_opt[node_index[node]] for node in all_nodes}

    return x_pos

y = assign_y_positions(ejercicios_ordenados)

x = optimize_x_positions(G, ejercicios_ordenados)
pos = {node: (x[node], y[node]) for node in G.nodes()}

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800)
plt.show()






