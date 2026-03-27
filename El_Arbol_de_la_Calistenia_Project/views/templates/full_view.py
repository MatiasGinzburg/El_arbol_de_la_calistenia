import customtkinter as ctk
from views.components.graph_canvas import GraphCanvas

class FullView(ctk.CTkFrame):
    def __init__(self, master, G, on_node_click, **kwargs):
        # We set fg_color to white to match your professional theme
        super().__init__(master, fg_color="white", **kwargs)
        
        self.on_node_click = on_node_click # Store the callback from main.py
        self.G = G

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
        # We pass 'self.handle_click' as the internal callback for the canvas
        self.canvas = GraphCanvas( 
            master=self, 
            on_node_selected=self.handle_click
        )
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)

        # 3. Initial Render
        self.canvas.display_graph(self.G)

    def handle_click(self, node_id):
        """
        This is an internal middle-man. 
        It receives the click from the Canvas and sends it up to MainApp.
        """
        if self.on_node_click:
            self.on_node_click(node_id)