import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class GraphCanvas(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # . Create the Matplotlib Figure
        # facecolor matches a typical dark theme background
        self.figure, self.ax = plt.subplots(figsize=(5, 5), facecolor='white')#242424
        self.ax.set_facecolor('white')
        
        # . Integrate Matplotlib with Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # . We create one hidden text box that we move around
        self.annot = self.ax.annotate(
            "", xy=(0,0), xytext=(15, 15),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="#1fb6ff", ec="white", alpha=0.9),
            arrowprops=dict(arrowstyle="->", color='white'),
            color="white", fontweight='bold'
        )
        self.annot.set_visible(False)
        # . Bind the motion event
        self.canvas.mpl_connect("motion_notify_event", self.on_hover)
        
        self.node_collection = None
        self.pos = None
        self.G = None

    def display_graph(self, G):
        """Renders the NetworkX graph G using its 'pos' attributes."""
        self.G = G
        
        # STEP 1: Clear the axis once at the very beginning
        self.ax.clear() 
        
        # STEP 2: IMPORTANT - Re-add the tooltip to the axis
        # Matplotlib's clear() removes the annotation we created in __init__
        self.ax.add_artist(self.annot)
        self.annot.set_visible(False)

        # Get positions
        self.pos = nx.get_node_attributes(G, 'pos')

        # STEP 3: Draw Edges first so they are behind the nodes
        nx.draw_networkx_edges(
            G, self.pos, ax=self.ax, 
            edge_color='#555555', width=2
        )

        # STEP 4: Draw Nodes and STORE them in self.node_collection
        # Do NOT call self.ax.clear() after this!
        self.node_collection = nx.draw_networkx_nodes(
            G, self.pos, ax=self.ax, 
            node_color='blue',  
            node_size=2000,
            node_shape="s" # Square
        )

        # STEP 5: Draw Labels on top of everything
        nx.draw_networkx_labels(
            G, self.pos, ax=self.ax,
            font_size=10,
            font_color='black',
            font_weight='bold'
        )

        
        # Clean up the UI
        self.ax.axis('off')
        
        # STEP 6: Refresh the canvas
        self.canvas.draw()


    def update_annot(self, ind):
        """Updates the position and text of the tooltip."""
        # Get the index of the node being hovered
        node_idx = list(self.G.nodes())[ind["ind"][0]]
        node_data = self.G.nodes[node_idx]
        
        # Get position of the node
        pos = self.pos[node_idx]
        self.annot.xy = pos
        
        # Set text (You can show any attribute here!)
        text = f"{node_idx}\nMax reps: {node_data.get('reps', 'No details')}"
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.9)

    def on_hover(self, event):
        """Logic to detect if the mouse is over a node."""
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            # Check if the mouse cursor contains any nodes
            cont, ind = self.node_collection.contains(event)
            if cont:
                self.update_annot(ind)
                self.annot.set_visible(True)
                self.canvas.draw_idle() # Redraw only if necessary
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.canvas.draw_idle()