import csv
from datetime import datetime
import os

class ResultsHandler:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_dir = "results"
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
    
    def save_results(self, open_links, closed_links, question_links):
        """Save results to CSV files with timestamp"""
        filename = f"groupme_results_{self.timestamp}.csv"
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Status', 'Link'])
            
            for link in open_links:
                writer.writerow(['Open', link])
            for link in closed_links:
                writer.writerow(['Closed', link])
            for link in question_links:
                writer.writerow(['Question', link])