from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from ixbrowser_local_api import IXBrowserClient
import time
import logging
from selenium.webdriver.common.keys import Keys
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains
from browser_actions import BrowserActions
from profile_manager import ProfileManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class BrowserController:
    def __init__(self):
        self.driver = None
        self.current_profile_id = None
        self.logger = logging.getLogger(__name__)
        self.ix_client = IXBrowserClient(target='127.0.0.1', port=53200)
        self.ix_client.show_request_log = False

    def get_profiles(self):
        """Get list of available profiles"""
        try:
            profiles = self.ix_client.get_profile_list(page=1, limit=100)
            if profiles is None:
                self.logger.error(f"Failed to get profiles: {self.ix_client.message}")
                raise Exception(f"Failed to get profiles: {self.ix_client.message}")
            return profiles
        except Exception as e:
            self.logger.error(f"Failed to get profiles: {str(e)}")
            raise Exception(f"Failed to get profiles: {str(e)}")

    def initialize_browser(self, profile_id=None):
        """Initialize browser with specific profile or first available"""
        try:
            if not profile_id:
                profiles = self.get_profiles()
                if not profiles:
                    self.logger.error("No profiles available")
                    raise Exception("No profiles available")
                profile_id = profiles[0]['profile_id']

            self.current_profile_id = profile_id
            self.logger.info(f"Initializing browser with profile ID: {profile_id}")
            
            # Open profile with IX Browser
            result = self.ix_client.open_profile(
                profile_id, 
                cookies_backup=False,
                load_profile_info_page=False
            )
            
            if result is None:
                self.logger.error(f"Failed to open profile: {self.ix_client.message}")
                raise Exception(f"Failed to open profile: {self.ix_client.message}")

            # Configure Selenium to connect to the running browser
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", result['debugging_address'])
            
            # Connect Selenium to the browser
            self.driver = webdriver.Chrome(
                service=Service(result['webdriver']), 
                options=chrome_options
            )
            self.logger.info("Browser initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize browser: {str(e)}")
            raise Exception(f"Failed to initialize browser: {str(e)}")

    def send_message_to_group(self, link, message):
        """Send message to a GroupMe group"""
        try:
            self.logger.info(f"Navigating to group: {link}")
            self.driver.get(link)
            time.sleep(3)
            
            # Check login status using ProfileManager
            profile_mgr = ProfileManager(self.driver, self.logger)
            if not profile_mgr.check_login_status():
                self.close_browser()
                return {
                    'status': 'permanent_skip',
                    'reason': 'Profile not logged in',
                    'link': link
                }

            # Handle group actions using BrowserActions
            browser_actions = BrowserActions(self.driver, self.logger)
            
            # Try joining group
            join_result = browser_actions.join_group(link)
            if join_result['status'] != 'success':
                return {**join_result, 'link': link}
            
            # Send message
            send_result = browser_actions.send_message(message)
            return {**send_result, 'link': link}
            
        except Exception as e:
            self.logger.error(f"General error: {str(e)}")
            return {
                'status': 'retry',
                'reason': str(e),
                'link': link
            }

    def close_browser(self):
        """Close the browser and profile properly"""
        try:
            if self.current_profile_id:
                self.logger.info(f"Closing profile {self.current_profile_id}")
                # First close the browser
                if self.driver:
                    try:
                        self.driver.quit()
                    except:
                        pass
                    self.driver = None
                
                # Then close the profile using IX Browser API
                result = self.ix_client.close_profile(self.current_profile_id)
                if result is None:
                    self.logger.warning(f"Failed to close profile: {self.ix_client.message}")
                else:
                    self.logger.info(f"Successfully closed profile {self.current_profile_id}")
                
                self.current_profile_id = None
                
        except Exception as e:
            self.logger.warning(f"Error while closing profile: {str(e)}")
        finally:
            self.driver = None
            self.current_profile_id = None
            self.logger.info("Browser cleanup completed") 