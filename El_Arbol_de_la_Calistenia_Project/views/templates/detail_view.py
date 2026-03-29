import customtkinter as ctk
from views.components.graph_canvas import GraphCanvas
from tkinter import messagebox
from dag_manipulation.dag import add_max_outgoing_edge_attribute, assign_colors_from_atribute


class DetailView(ctk.CTkFrame):
    def __init__(self, master, node_id, node_data, sub_graph, on_back_click, on_node_click, on_save_reps, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)

        self.sub_graph = sub_graph
        add_max_outgoing_edge_attribute(self.sub_graph, weight_key='weight', attr_name='max_requirement') 

        self.colors = assign_colors_from_atribute(sub_graph,atribute='reps', v_min=0, v_max='max_requirement' ,color_low='red',color_standard='blue', color_high='green')

        self.node_idx = list(self.sub_graph.nodes()).index(node_id) # thi is the index in the list of colors asocuated to the head node node_id

        self.colors[self.node_idx] = 'red' if sub_graph.nodes[node_id]['reps']==0 else 'green' 


        self.node_id = node_id  # Store this so main.py can see it
 
        self.on_node_click = on_node_click # Store the jump function
        self.on_back_click = on_back_click
        self.on_save_reps = on_save_reps # Store the save function

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

        # 2. Info Section 
        self.info_panel = ctk.CTkFrame(self, fg_color="#f9f9f9", corner_radius=10)
        self.info_panel.pack(fill="x", padx=20, pady=5)
        
        # Label
        self.reps_label = ctk.CTkLabel(self.info_panel, text=f"Max Reps: {node_data.get('reps')}")# , '0')}")
        self.reps_label.pack(pady=10)

        # Input Field (Entry)
        self.reps_entry = ctk.CTkEntry(self.info_panel, width=100)
        self.reps_entry.insert(0, str(node_data.get('reps', '0'))) # Show current value
        self.reps_entry.pack(side="left", padx=10)
        self.reps_entry.bind("<Return>",lambda event: self.handle_save())

        # Save Button
        self.save_btn = ctk.CTkButton(
            self.info_panel, 
            text="Save Changes", 
            width=120,
            fg_color="#27ae60", # Green for "Success/Save"
            command=self.handle_save
        )
        self.save_btn.pack(side="left", padx=20)

        # Update the Canvas initialization
        self.canvas = GraphCanvas(
            master=self, 
            on_node_click = self.on_node_click
            #on_node_click=self.handle_jump # old
        )
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)
        self.canvas.display_graph(sub_graph, self.colors)


    
    def handle_save(self):
        user_input = self.reps_entry.get()
        try:
            new_reps = int(user_input)
            self.on_save_reps(self.node_id, new_reps)
            self.reps_label.configure(text=f"Max Reps: {new_reps}")
            #new
            self.colors[self.node_idx] = 'red' if new_reps==0 else 'green' 
            self.canvas.display_graph(self.sub_graph,self.colors) 

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter an integer number for repetitions.")
            self.reps_entry.focus_set() # Puts the cursor back in the box for them

    def update_display(self, sub_graph, selected_node): #old
        colors = []
        for node in sub_graph.nodes():
            # 1. The main selected node is always blue (or your choice)
            if node == selected_node:
                colors.append("#1fb6ff")
                continue

            reps = int(sub_graph.nodes[node].get('reps', 0))
            
            # 2. Check the edge requirement
            # We look for the edge: node -> selected_node
            try:
                # Assuming your edge has an attribute 'weight' or 'req'
                # Replace 'weight' with whatever name you use in your JSON
                requirement = int(self.master.full_graph[node][selected_node].get('weight', 5))
            except KeyError:
                requirement = 999 # Safety if no direct edge exists

            if reps >= requirement:
                colors.append("#27ae60") # GREEN (Mastered)
            elif reps > 0:
                colors.append("#1fb6ff") # BLUE (Started)
            else:
                colors.append("#ff4b4b") # RED (Locked)

        self.canvas.display_graph(sub_graph, node_colors=colors)