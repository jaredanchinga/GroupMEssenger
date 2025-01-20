import tkinter as tk
from tkinter import ttk, scrolledtext

class GroupMeGUI:
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("GroupMe Automation")
        self.window.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # Group Links Section
        links_frame = ttk.LabelFrame(self.window, text="Group Links", padding="10")
        links_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.links_text = scrolledtext.ScrolledText(links_frame, height=10)
        self.links_text.pack(fill="both", expand=True)
        
        # Advertisement Message Section
        message_frame = ttk.LabelFrame(self.window, text="Advertisement Message", padding="10")
        message_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.message_text = scrolledtext.ScrolledText(message_frame, height=5)
        self.message_text.pack(fill="both", expand=True)
        
        # Control Buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        self.start_button = ttk.Button(button_frame, text="Start Automation", 
                                     command=self.controller.start_automation)
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", 
                                    command=self.controller.stop_automation)
        self.stop_button.pack(side="left", padx=5)
        
        # Status Label
        self.status_label = ttk.Label(self.window, text="Status: Ready")
        self.status_label.pack(pady=5)

    def get_links(self):
        return self.links_text.get("1.0", tk.END).strip().split("\n")

    def get_message(self):
        return self.message_text.get("1.0", tk.END).strip()

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")
        self.window.update()

    def run(self):
        self.window.mainloop() 