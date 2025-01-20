from controller import Controller
from browser_controller import BrowserController
from ixbrowser_local_api import IXBrowserClient
import logging
import time
import tkinter as tk
import tkinter.messagebox as messagebox
from results_handler import ResultsHandler

class ExcelController(Controller):
    def __init__(self):
        super().__init__()
        self.process_links = self._process_links

    def _process_links(self, message, links_per_profile=3):
        """Process links directly from interface"""
        suspended_profiles = set()
        results_handler = ResultsHandler()
        
        # Track results
        open_links = []
        closed_links = []
        question_links = []
        
        try:
            # Initialize IX Browser client with different port
            client = IXBrowserClient(target='127.0.0.1', port=53200)
            client.show_request_log = False
            
            # Get and sort profiles
            profiles = client.get_profile_list(page=1, limit=100)
            if profiles is None:
                logging.error(f'Error getting profile list: {client.message}')
                return
            
            profile_ids = [profile['profile_id'] for profile in profiles]
            profile_ids.sort()
            
            # Get links from interface
            remaining_links = self.links
            
            # Process each profile in order
            for i, profile_id in enumerate(profile_ids):
                if self.is_cancelled:
                    return
                
                while self.is_paused:
                    time.sleep(1)
                    if self.is_cancelled:
                        return
                
                if profile_id in suspended_profiles:
                    logging.info(f"Skipping suspended profile {profile_id}")
                    continue
                
                # Calculate batch size - either 3 or whatever is left
                batch_size = min(links_per_profile, len(remaining_links))
                if batch_size == 0:
                    logging.info("No more links to process")
                    return
                
                logging.info(f"[{i+1}/{len(profile_ids)}] Profile {profile_id} processing {batch_size} links")
                
                # Take only the links we'll process in this batch
                current_batch = remaining_links[:batch_size]
                remaining_links = remaining_links[batch_size:]  # Update remaining links
                
                # Process the batch with current profile
                result = client.open_profile(profile_id, cookies_backup=True, load_extensions=True)
                if result is None:
                    logging.error(f'Error opening profile {profile_id}')
                    continue
                
                browser = BrowserController()
                links_processed = 0
                
                try:
                    browser.initialize_browser(profile_id)
                    
                    # Process each link in current batch
                    for index, link in enumerate(current_batch, 1):
                        logging.info(f"Processing link {index}/{batch_size} with profile {profile_id}")
                        
                        try:
                            result = browser.send_message_to_group(link, message)
                            if result['status'] == 'permanent_skip':
                                if result['reason'] == 'Profile not logged in':
                                    suspended_profiles.add(profile_id)
                                    break
                                elif result['reason'] == 'Group requires admin approval':
                                    closed_links.append(link)
                                elif result['reason'] == 'Group has security question':
                                    question_links.append(link)
                                elif result['reason'] == 'Link expired or no permission':
                                    closed_links.append(link)
                            elif result['status'] == 'success':
                                open_links.append(link)
                            
                            links_processed += 1
                            time.sleep(5)  # Sleep after each link
                            
                        except Exception as e:
                            logging.error(f"Error on link {index}/{batch_size}: {str(e)}")
                            
                finally:
                    if browser:
                        logging.info(f"Closing profile {profile_id} after processing {links_processed}/{batch_size} links")
                        browser.close_browser()
                        close_result = client.close_profile(profile_id)
                        if close_result is None:
                            logging.error(f'Error closing profile {profile_id}')
                        browser = None
                
                # Add 15 seconds sleep before next profile
                if i < len(profile_ids) - 1 and remaining_links:  # Don't sleep after last profile or if no links left
                    logging.info("Waiting 15 seconds before next profile...")
                    time.sleep(15)
            
            # Save results after processing all links
            results_handler.save_results(open_links, closed_links, question_links)
            
            logging.info("Processing complete. Results saved to CSV.")
            
        except Exception as e:
            logging.error(f"General error: {str(e)}")
            # Save results even if there's an error
            results_handler.save_results(open_links, closed_links, question_links)
            logging.info("Results saved to CSV (after error)")
            raise

    def run(self):
        """Main execution method"""
        try:
            self.root.mainloop()
        except Exception as e:
            logging.error(f"Error in run method: {str(e)}")
            raise

if __name__ == "__main__":
    app = ExcelController()
    app.run() 