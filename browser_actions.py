from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time
import logging

class BrowserActions:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def join_group(self, link):
        """Handle group joining logic"""
        try:
            self.logger.info("Looking for group action button...")
            action_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="group-preview"]/div[3]/div[4]/button'))
            )
            button_text = action_button.text.strip().upper()
            
            if button_text == "PENDING":
                self.logger.warning("Group is closed with pending approval, skipping...")
                return {
                    'status': 'permanent_skip',
                    'reason': 'Group requires admin approval'
                }
            elif button_text == "VIEW":
                self.logger.info("Already a member, clicking View...")
                action_button.click()
                time.sleep(3)
                return {'status': 'success'}
            else:  # Assume JOIN
                # Try joining with limit detection
                return self._handle_join_button_with_limit_check(action_button, link)
                
        except Exception as e:
            self.logger.error(f"Error with group action button: {str(e)}")
            return {
                'status': 'retry',
                'reason': str(e)
            }

    def _handle_join_button_with_limit_check(self, action_button, link):
        """Handle joining with limit detection"""
        self.logger.info("Join button found, attempting to join...")
        
        # First attempt
        action_button.click()
        time.sleep(3)
        
        # Check if still on join button
        try:
            join_button = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="group-preview"]/div[3]/div[4]/button'))
            )
            if join_button.text.strip().upper() == "JOIN":
                self.logger.info("Join button still present, trying one more time...")
                
                # Second attempt
                join_button.click()
                time.sleep(3)
                
                # Check again
                try:
                    final_button = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="group-preview"]/div[3]/div[4]/button'))
                    )
                    if final_button.text.strip().upper() == "JOIN":
                        self.logger.warning("Profile has reached join limit!")
                        return {
                            'status': 'profile_limit',
                            'reason': 'Profile has reached join limit'
                        }
                except:
                    pass  # Button changed, continue normal flow
                    
        except:
            pass  # Button changed, continue normal flow
        
        # Continue with normal security check and membership verification
        if self._check_security_question():
            return {
                'status': 'permanent_skip',
                'reason': 'Group has security question'
            }
        
        return self._verify_membership(link)

    def _check_security_question(self):
        """Check if group has security question"""
        try:
            security_submit_button = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/button'))
            )
            self.logger.warning("Group has security question, skipping...")
            return True
        except:
            self.logger.info("Group does not have security question")
            return False

    def send_message(self, message):
        """Send message to group"""
        try:
            message_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id, 'message-composer-')]"))
            )
            
            self.logger.info("Found message input, attempting to send message...")
            pyperclip.copy(message)
            ActionChains(self.driver).click(message_input).perform()
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            time.sleep(1)
            message_input.send_keys(Keys.ENTER)
            time.sleep(2)
            
            self.logger.info("Message sent successfully to group")
            return {
                'status': 'success',
                'reason': 'Message sent successfully'
            }
            
        except Exception as e:
            self.logger.error(f"Error sending message: {str(e)}")
            return {
                'status': 'retry',
                'reason': str(e)
            } 

    def _verify_membership(self, link):
        """Verify successful group membership"""
        self.logger.info("Refreshing page to verify membership...")
        self.driver.get(link)
        time.sleep(3)
        
        # Verify VIEW button appears
        try:
            view_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="group-preview"]/div[3]/div[4]/button'))
            )
            if view_button.text.strip().upper() == "VIEW":
                self.logger.info("Successfully joined group, clicking View...")
                view_button.click()
                time.sleep(3)
                return {'status': 'success'}
            else:
                self.logger.warning("Join failed - View button not found after refresh")
                return {
                    'status': 'retry',
                    'reason': 'Failed to verify group membership'
                }
        except Exception as e:
            self.logger.warning(f"Failed to verify membership: {str(e)}")
            return {
                'status': 'retry',
                'reason': 'Failed to verify group membership'
            } 