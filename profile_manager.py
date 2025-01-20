import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class ProfileManager:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.current_profile_id = None

    def check_login_status(self):
        """Check if profile is logged in and not banned"""
        try:
            # Load chats page to check status
            self.logger.info("Checking profile status...")
            self.driver.get("https://web.groupme.com/chats")
            time.sleep(3)
            
            try:
                # First try to find login button
                login_button = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="sign-in-container"]/div/div[2]/form/button'))
                )
                self.logger.error(f"Profile {self.current_profile_id} is not logged in or is banned")
                return False
            except:
                # If no login button, check for either chats or home icon
                try:
                    WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="tray"]/div[1]/div[1]/button/span[2]'))
                    )
                    self.logger.info("Profile is logged in (chats visible)")
                    return True
                except:
                    try:
                        WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/aside/div[1]/button/svg/path'))
                        )
                        self.logger.info("Profile is logged in (home icon visible)")
                        return True
                    except:
                        self.logger.error(f"Profile {self.current_profile_id} status check failed")
                        return False
                
        except Exception as e:
            self.logger.error(f"Error checking profile status: {str(e)}")
            return False 