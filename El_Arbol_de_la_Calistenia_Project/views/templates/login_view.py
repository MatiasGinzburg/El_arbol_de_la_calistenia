import customtkinter as ctk

class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        
        # Center the login box
        self.container = ctk.CTkFrame(self, fg_color="#f9f9f9", corner_radius=20)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.container, text="Welcome to the Tree", font=("Arial", 24, "bold")).pack(pady=20, padx=40)
        
        self.username_entry = ctk.CTkEntry(self.container, placeholder_text="Enter Username...", width=250)
        self.username_entry.pack(pady=10)
        
        # Bind "Enter" key to the login function for a professional feel
        self.username_entry.bind("<Return>", lambda e: on_login(self.username_entry.get()))

        self.start_btn = ctk.CTkButton(
            self.container, 
            text="Start Training", 
            command=lambda: on_login(self.username_entry.get()),
            fg_color="#1fb6ff", hover_color="#1991cc"
        )
        self.start_btn.pack(pady=20)