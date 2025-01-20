from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

class LoginTester:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def test_login_status(self):
        """Test if profile is logged in and not banned"""
        try:
            self.logger.info("Testing login status...")
            self.driver.get("https://web.groupme.com/chats")
            time.sleep(5)  # Wait 5 seconds after loading URL
            
            try:
                # Check for login button with explicit wait and click
                login_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="sign-in-container"]/div/div[2]/form/button'))
                )
                
                # Try clicking login button with multiple methods
                try:
                    self.logger.info("Found login button, attempting to login...")
                    login_button.click()
                except:
                    try:
                        self.logger.info("Trying JavaScript click...")
                        self.driver.execute_script("arguments[0].click();", login_button)
                    except:
                        self.logger.error("Failed to click login button")
                        return False
                        
                time.sleep(5)  # Wait to see if login succeeds
                
                # Check if we got to chats after login attempt
                try:
                    WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="tray"]/div[1]/div[1]/button/span[2]'))
                    )
                    self.logger.info("Login successful")
                    return True
                    
                except:
                    self.logger.error("Login failed - account likely banned")
                    return False
                    
            except:
                # No login button found, check if already in chats
                try:
                    WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="tray"]/div[1]/div[1]/button/span[2]'))
                    )
                    self.logger.info("Already logged in")
                    return True
                    
                except:
                    self.logger.error("Failed to verify chat access")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error testing login status: {str(e)}")
            return False 