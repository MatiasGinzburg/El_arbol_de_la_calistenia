import customtkinter as ctk
from views.components.graph_canvas import GraphCanvas
from dag_manipulation.dag import assign_colors_from_atribute # new 


class FullView(ctk.CTkFrame):
    def __init__(self, master, G, on_node_click, **kwargs):
        # We set fg_color to white to match your professional theme
        super().__init__(master, fg_color="white", **kwargs)
        
        self.on_node_click = on_node_click # Store the callback from main.py
        self.G = G
        #New
        self.node_colors = assign_colors_from_atribute(G, atribute='reps',v_min=0, color_low='red',color_standard='blue')

        # 1. Header / Welcome Section
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=40, pady=(30, 10))

        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Your Knowledge Map", 
            font=("Arial", 28, "bold"),
            text_color="#333333"
        )
        self.title_label.pack(side="left")

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="Click a node to dive into its details and descendants.", 
            font=("Arial", 14),
            text_color="#777777"
        )
        self.subtitle_label.pack(padx=40, anchor="w")

        # 2. The Graph Section
        self.canvas = GraphCanvas( 
            master=self, 
            on_node_click=self.on_node_click 
        )
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)

        # 3. Initial Render
        self.canvas.display_graph(self.G, self.node_colors)


    def update_display(self): # old
        colors = []
        for node in self.G.nodes():
            reps = int(self.G.nodes[node].get('reps', 0))
            colors.append("#1fb6ff" if reps > 0 else "#ff4b4b") # Blue vs Red
        
        self.canvas.display_graph(self.G, node_colors=colors)

    def set_colors(self): # New
        self.colors = []
        for node in self.G.nodes():
            reps = int(self.G.nodes[node].get('reps', 0))
            self.colors.append("#1fb6ff" if reps > 0 else "#ff4b4b") # Blue vs Red
        


