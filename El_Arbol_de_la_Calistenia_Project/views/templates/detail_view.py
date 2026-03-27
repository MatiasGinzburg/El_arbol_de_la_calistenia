import customtkinter as ctk
from views.components.graph_canvas import GraphCanvas

class DetailView(ctk.CTkFrame):
    def __init__(self, master, node_id, node_data, sub_graph, on_back_click, on_node_click, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)

        self.node_id = node_id  # Store this so main.py can see it
 
        self.on_node_click = on_node_click # Store the jump function
        self.on_back_click = on_back_click

        # 1. Header Section
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=10)
        

        self.back_btn = ctk.CTkButton(
            self.header, 
            text="← Back", 
            command=self.on_back_click # This now points to MainApp.go_back
        )
        self.back_btn.pack(side="left")


        self.title = ctk.CTkLabel(self.header, text=f"Node: {node_id}", font=("Arial", 20, "bold"))
        self.title.pack(side="left", padx=20)

        # 2. Info Section (Where you'll add more "stuff" later)
        self.info_panel = ctk.CTkFrame(self, fg_color="#f9f9f9", corner_radius=10)
        self.info_panel.pack(fill="x", padx=20, pady=5)
        
        self.reps_label = ctk.CTkLabel(self.info_panel, text=f"Max Reps: {node_data.get('reps', '0')}")
        self.reps_label.pack(pady=10)


        # Update the Canvas initialization
        self.canvas = GraphCanvas(
            master=self, 
            on_node_selected=self.handle_jump # Use a local handler
        )
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)
        self.canvas.display_graph(sub_graph)

    def handle_click(self, node_id):
        """
        This is an internal middle-man. 
        It receives the click from the Canvas and sends it up to MainApp.
        """
        if self.on_node_click:
            self.on_node_click(node_id)

    def handle_jump(self, new_node_id):
        """When a node in the SUBGRAPH is clicked, jump to its Detail View."""
        if self.on_node_click:
            self.on_node_click(new_node_id)