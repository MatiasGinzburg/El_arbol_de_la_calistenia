import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import numpy as np
import webbrowser
from threading import Timer

# 1. Load your data 
matriz_ejercicios = pd.read_csv('matrizEjercicios-full.csv', index_col=0)


# 2. Create the Directed Graph
# NetworkX interprets rows as 'source' and columns as 'target'

# Replace Nan with 0 so NetworkX ignores them
matriz_masked = matriz_ejercicios.replace(np.nan, 0)


# Create the graph (it will only create edges for non 0 values)
G = nx.from_pandas_adjacency(matriz_masked, create_using=nx.DiGraph)

# 5. Find and print cycles (we dont want any cycle)
cycles = list(nx.simple_cycles(G))

if not cycles:
    print("The graph is a Directed Acyclic Graph (DAG) - No cycles found.")
else:
    print(f"Found {len(cycles)} closed circles (cycles):")
    for i, cycle in enumerate(cycles, 1):
        # We append the first node to the end to visually show the 'loop'
        print(f"Cycle {i}: {' -> '.join(map(str, cycle))} -> {cycle[0]}")


layers = list(nx.topological_generations(G))
pos = {node: (node_idx - len(nodes) / 2, layer_idx) 
       for layer_idx, nodes in enumerate(layers) 
       for node_idx, node in enumerate(nodes)}

# 2. Initialize the Dash App # Done by gemini, no idea how it works
app = Dash(__name__)

app.layout = html.Div([
    html.H2("Interactive Exercise Dependency Map"),
    html.P("Click a square to see only its prerequisites (ancestors)."),
    dcc.Graph(id='network-graph', style={'height': '80vh'}),
    html.Button("Reset View", id='reset-btn', n_clicks=0)
])

@app.callback(
    Output('network-graph', 'figure'),
    Input('network-graph', 'clickData'),
    Input('reset-btn', 'n_clicks')
)
def update_graph(clickData, n_clicks):
    # Determine which nodes to display
    nodes_to_show = list(G.nodes())
    
    # If a node was clicked, find its ancestors
    if clickData:
        target_node = clickData['points'][0]['text']
        # nx.ancestors returns all nodes that have a path TO the target
        nodes_to_show = list(nx.ancestors(G, target_node)) + [target_node]

    # Filter the edges to show
    edge_x, edge_y = [], []
    for edge in G.edges():
        if edge[0] in nodes_to_show and edge[1] in nodes_to_show:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

    # Create the Edges trace
    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='#888'),
                            hoverinfo='none', mode='lines')

    # Create the Nodes trace (Squares)
    node_x = [pos[node][0] for node in nodes_to_show]
    node_y = [pos[node][1] for node in nodes_to_show]
    
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text',
        text=nodes_to_show, textposition="bottom center",
        marker=dict(symbol='square', size=30, color='SkyBlue', line_width=2),
        hoverinfo='text'
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        plot_bgcolor='white'
                    ))
    return fig

def open_browser():
    # This opens your default browser at the local address
    webbrowser.open_new("http://127.0.0.1:8050/")


if __name__ == '__main__':
    # Start a timer to open the browser after 2 seconds
    Timer(2, open_browser).start()
    
    app.run(debug=True, use_reloader=False)