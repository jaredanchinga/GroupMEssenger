import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ProfileManager:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.current_profile_id = None

    def check_login_status(self):
        """Check if profile is logged in"""
        try:
            login_button = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="sign-in-container"]/div/div[2]/form/button'))
            )
            
            self.logger.error(f"Profile {self.current_profile_id} is not logged in")
            return False
                
        except:
            self.logger.info("Profile is properly logged in")
            return True 