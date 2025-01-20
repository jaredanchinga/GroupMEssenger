import tkinter as tk
from tkinter import ttk, scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

class GroupMeBot:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("GroupMe Automation")
        self.window.geometry("800x600")
        
        # Create main containers
        self.create_widgets()
        
        # Initialize driver as None
        self.driver = None

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
        
        self.start_button = ttk.Button(button_frame, text="Start Automation", command=self.start_automation)
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_automation)
        self.stop_button.pack(side="left", padx=5)
        
        # Status Label
        self.status_label = ttk.Label(self.window, text="Status: Ready")
        self.status_label.pack(pady=5)

    def start_automation(self):
        # Get links and message
        links = self.links_text.get("1.0", tk.END).strip().split("\n")
        message = self.message_text.get("1.0", tk.END).strip()
        
        if not links or not message:
            self.update_status("Please provide both group links and message")
            return
            
        try:
            # Initialize IX browser
            options = webdriver.ChromeOptions()
            options.add_argument("--remote-debugging-port=9222")
            self.driver = webdriver.Chrome(options=options)
            
            # Process each link
            for link in links:
                if not link.strip():
                    continue
                    
                try:
                    self.update_status(f"Processing link: {link}")
                    
                    # Navigate to group
                    self.driver.get(link)
                    time.sleep(3)  # Wait for page load
                    
                    # Find and click message input
                    message_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[placeholder='Type a message...']"))
                    )
                    message_input.click()
                    message_input.send_keys(message)
                    
                    # Find and click send button
                    send_button = self.driver.find_element(By.CSS_SELECTOR, "button[title='Send Message']")
                    send_button.click()
                    
                    time.sleep(2)  # Wait between messages
                    
                except Exception as e:
                    self.update_status(f"Error processing link {link}: {str(e)}")
                    continue
            
            self.update_status("Automation completed")
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None

    def stop_automation(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
        self.update_status("Automation stopped")

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")
        self.window.update()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    bot = GroupMeBot()
    bot.run() 