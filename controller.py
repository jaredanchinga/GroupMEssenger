import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import logging
import os
import threading

class LogHandler(logging.Handler):
    """Custom logging handler that writes to tkinter text widget"""
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        try:
            msg = self.format(record)
            def append():
                self.text_widget.configure(state='normal')
                self.text_widget.insert('end', msg + '\n')
                self.text_widget.see('end')  # Scroll to end
                self.text_widget.configure(state='disabled')
            # Schedule the update on the main thread
            self.text_widget.after(0, append)
        except Exception:
            self.handleError(record)

class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GroupMe Automation")
        self.root.geometry("800x600")  # Made window bigger for logs
        
        # Control flags
        self.is_paused = False
        self.is_cancelled = False
        self.excel_path = None  # Store selected Excel path
        
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left frame for message input
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Title
        title_label = ttk.Label(
            left_frame, 
            text="GroupMe Advertisement Automation",
            font=('Helvetica', 12, 'bold')
        )
        title_label.pack(pady=10)
        
        # Excel File Selection Frame
        excel_frame = ttk.Frame(left_frame)
        excel_frame.pack(fill=tk.X, pady=5)
        
        self.excel_label = ttk.Label(
            excel_frame,
            text="No Excel file selected",
            font=('Helvetica', 9),
            wraplength=300
        )
        self.excel_label.pack(side=tk.LEFT, padx=5)
        
        excel_button = ttk.Button(
            excel_frame,
            text="Select Excel File",
            command=self.select_excel_file
        )
        excel_button.pack(side=tk.RIGHT, padx=5)
        
        # Advertisement Message
        message_label = ttk.Label(
            left_frame, 
            text="Paste your advertisement message below:",
            font=('Helvetica', 10)
        )
        message_label.pack(pady=5)
        
        self.message_text = tk.Text(left_frame, height=10, width=40)
        self.message_text.pack(pady=10, fill=tk.X)
        
        # Buttons frame
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(pady=20)
        
        # Start Button
        self.start_button = ttk.Button(
            button_frame, 
            text="Start Automation", 
            command=self.start,
            style='Accent.TButton'
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Pause Button
        self.pause_button = ttk.Button(
            button_frame, 
            text="Pause", 
            command=self.toggle_pause,
            state=tk.DISABLED
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel Button
        self.cancel_button = ttk.Button(
            button_frame, 
            text="Cancel", 
            command=self.cancel,
            state=tk.DISABLED
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(
            left_frame,
            text="Ready to start",
            font=('Helvetica', 9)
        )
        self.status_label.pack(pady=10)

        # Right frame for logs
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Log Label
        log_label = ttk.Label(
            right_frame,
            text="Activity Log:",
            font=('Helvetica', 10, 'bold')
        )
        log_label.pack(pady=(0, 5))
        
        # Log Display
        self.log_display = scrolledtext.ScrolledText(
            right_frame,
            height=30,
            width=50,
            font=('Courier', 9),
            bg='black',
            fg='white',
            wrap=tk.WORD  # Add word wrapping
        )
        self.log_display.pack(fill=tk.BOTH, expand=True)
        self.log_display.configure(state='disabled')

        # Set up logging to text widget with error handling
        try:
            log_handler = LogHandler(self.log_display)
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            log_handler.setFormatter(formatter)
            
            # Remove any existing handlers
            root_logger = logging.getLogger()
            for handler in root_logger.handlers[:]:
                root_logger.removeHandler(handler)
                
            # Add our handler and set level
            root_logger.addHandler(log_handler)
            root_logger.setLevel(logging.INFO)
            
            # Test log
            logging.info("Logging system initialized")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize logging: {str(e)}")

        self.process_links = None  # Will be set by ExcelController

    def select_excel_file(self):
        """Open file dialog to select Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx")],
            initialdir=os.getcwd()
        )
        
        if file_path:
            self.excel_path = file_path
            # Show only filename in label
            filename = os.path.basename(file_path)
            self.excel_label.config(text=f"Selected: {filename}")
            logging.info(f"Excel file selected: {filename}")
            
            # Enable start button only if Excel is selected
            self.start_button.config(state=tk.NORMAL)
        else:
            self.excel_path = None
            self.excel_label.config(text="No Excel file selected")
            self.start_button.config(state=tk.DISABLED)

    def start(self):
        """Start automation only if Excel file is selected"""
        if not self.excel_path:
            messagebox.showerror("Error", "Please select an Excel file first")
            return
            
        message = self.message_text.get("1.0", tk.END).strip()
        if message:
            # Enable control buttons
            self.pause_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.NORMAL)
            self.start_button.config(state=tk.DISABLED)
            
            self.status_label.config(text="Processing...")
            self.message = message
            
            # Start automation in a separate thread to keep UI responsive
            self.automation_thread = threading.Thread(
                target=self.run_automation,
                args=(message,),
                daemon=True
            )
            self.automation_thread.start()
        else:
            messagebox.showerror("Error", "Please enter an advertisement message")

    def run_automation(self, message):
        """Run the automation in a separate thread"""
        try:
            if self.process_links is None:
                raise Exception("Automation not properly initialized")
                
            # Run the actual automation
            self.process_links(message)
            
            # Update UI when done
            self.root.after(0, self.automation_completed)
        except Exception as e:
            # Update UI on error
            self.root.after(0, lambda: self.automation_error(str(e)))

    def automation_completed(self):
        """Called when automation is complete"""
        self.status_label.config(text="Automation completed")
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)
        messagebox.showinfo("Complete", "Automation has finished!")

    def automation_error(self, error_message):
        """Called when automation encounters an error"""
        self.status_label.config(text="Error occurred")
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)
        messagebox.showerror("Error", f"An error occurred: {error_message}")

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.config(text="Resume")
            self.status_label.config(text="Paused")
        else:
            self.pause_button.config(text="Pause")
            self.status_label.config(text="Processing...")

    def cancel(self):
        if messagebox.askyesno("Confirm Cancel", "Are you sure you want to cancel the automation?"):
            self.is_cancelled = True
            self.root.destroy()

    def get_message(self):
        self.message = None
        self.root.mainloop()
        return self.message 