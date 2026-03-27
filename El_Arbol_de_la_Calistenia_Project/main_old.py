import customtkinter as ctk
import networkx as nx
import json
from networkx.readwrite import json_graph
from views.graph_canvas_old import GraphCanvas



def get_demo_graph(filename):
    with open(f"Data/{filename}.json", "r") as f:
        data = json.load(f)
        G = json_graph.node_link_graph(data)
    return G

app = ctk.CTk()
app.geometry("800x600")
app.title("Arbol de Calistenia")

# Initialize your view module
view = GraphCanvas(master=app)
view.pack(fill="both", expand=True)

# Show the graph
filename = "matrizEjercicios"
G = get_demo_graph(filename)
view.display_graph(G)

app.mainloop()