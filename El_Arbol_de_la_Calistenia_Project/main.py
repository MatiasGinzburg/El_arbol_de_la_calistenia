import customtkinter as ctk
import networkx as nx
import json
from networkx.readwrite import json_graph
from views.templates.full_view import FullView
from views.templates.detail_view import DetailView
import os
import shutil

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Window Configuration
        self.title("El Arbol de la Calistenia")
        self.geometry("1100x800")
        self.configure(fg_color="white") 
        
        self.history = []  # This stores the sequence of node_ids visited

        self.current_user = None
        self.full_graph = None
        self.current_view = None

        # Start with the Login Screen
        self.show_login_screen()


    def login_user(self, username):
        if not username: return
        
        self.current_user = username
        # This is the full path to the user's specific file
        user_path = f"Data/users/{username}.json"
        default_path = "Data/matrizEjercicios-full.json"

        os.makedirs("Data/users", exist_ok=True)

        if not os.path.exists(user_path):
            # If new user, copy from the main Data folder to the users folder
            shutil.copy(default_path, user_path)
            print(f"Created new profile for {username}")

        # Pass the full path we just built
        self.full_graph = self.setup_initial_data(user_path)
        self.show_full_view()

    def save_user_data(self):
        """Call this whenever a node is edited!"""
        if self.current_user and self.full_graph:
            filename = f"Data/users/{self.current_user}.json"
            data = json_graph.node_link_data(self.full_graph)
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)

    def setup_initial_data(self, path):
        """Creates the master Directed Graph from a provided path."""
        with open(path, "r") as f: # Removed f"Data/{filename}.json"
            data = json.load(f)
            G = json_graph.node_link_graph(data)
        return G

    def clear_current_view(self):
        """Removes the existing template from the window to save memory."""
        if self.current_view:
            self.current_view.destroy()

    def show_full_view(self):
        """Switches the UI to the 'Full Tree' template."""
        self.clear_current_view()
        self.history = [] 
        # We pass self.show_detail_view as a 'callback' 
        # so the template can tell us when a node is clicked
        self.current_view = FullView(
            master=self, 
            G=self.full_graph, 
            on_node_click=self.show_detail_view
        )
        self.current_view.pack(fill="both", expand=True)

    def show_detail_view(self, node_id):
        """Standard navigation: Adds current node to history and shows detail."""
        # If we are already in a detail view, save the OLD node to history 
        # before switching to the NEW one.
        if isinstance(self.current_view, DetailView):
            self.history.append(self.current_view.node_id)

        self._render_detail(node_id)

    def show_login_screen(self):
        self.clear_current_view()
        from views.templates.login_view import LoginView
        self.current_view = LoginView(master=self, on_login=self.login_user)
        self.current_view.pack(fill="both", expand=True)

    def go_back(self):
        """The logic for the Back button."""
        if not self.history:
            # If history is empty, we go all the way back to the full map
            self.show_full_view()
        else:
            # Pop the last node from the stack and render it
            previous_node = self.history.pop()
            self._render_detail(previous_node)

    def _render_detail(self, node_id):
        """Internal helper to actually draw the DetailView."""
        self.clear_current_view()
        
        # Logic to get ancestors/subgraph
        ancestors = nx.ancestors(self.full_graph, node_id)
        nodes_to_keep = {node_id} | ancestors
        sub_graph = self.full_graph.subgraph(nodes_to_keep)
        node_data = self.full_graph.nodes[node_id]

        self.current_view = DetailView(
            master=self,
            node_id=node_id,
            node_data=node_data,
            sub_graph=sub_graph,
            on_back_click=self.go_back, # Now links to go_back logic
            on_node_click=self.show_detail_view
        )
        self.current_view.pack(fill="both", expand=True)

    

if __name__ == "__main__":
    # Set the appearance theme
    ctk.set_appearance_mode("light")
    
    app = MainApp()
    app.mainloop()