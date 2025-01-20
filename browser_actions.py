from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time
import logging
from message_sender import MessageSender
from delay_utils import random_delay, click_delay, profile_switch_delay

class BrowserActions:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.message_sender = MessageSender(driver, logger)

    def join_group(self, link):
        """Handle group joining logic"""
        try:
            random_delay()  # Keep longer delay before looking for button
            self.logger.info("Looking for group action button...")
            
            # Check for expired link message
            try:
                continue_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="group-preview"]/div[3]/div[2]/button'))
                )
                if continue_button.text.strip().upper() == "CONTINUE TO GROUPME":
                    self.logger.warning("Link is expired or no permission to join")
                    return {
                        'status': 'permanent_skip',
                        'reason': 'Link expired or no permission'
                    }
            except:
                pass  # Not an expired link, continue normal flow
            
            # First try the button with span
            try:
                action_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="group-preview"]/div[3]/div[4]/button/span'))
                )
                if action_button.text.strip().upper() == "PENDING":
                    self.logger.warning("Group is closed with pending approval, skipping...")
                    return {
                        'status': 'permanent_skip',
                        'reason': 'Group requires admin approval'
                    }
            except:
                # If no span, try the regular button
                action_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="group-preview"]/div[3]/div[4]/button'))
                )
            
            button_text = action_button.text.strip().upper()
            
            if button_text == "VIEW":
                self.logger.info("Already a member, clicking View...")
                click_delay()  # Shorter delay for clicking
                action_button.click()
                time.sleep(3)
                return {'status': 'success'}
            else:  # Assume JOIN
                self.logger.info("Join button found, attempting to join...")
                click_delay()  # Shorter delay for clicking
                action_button.click()
                time.sleep(3)
                
                # Check for security question
                if self._check_security_question():
                    return {
                        'status': 'permanent_skip',
                        'reason': 'Group has security question'
                    }
                
                return self._verify_membership(link)
                
        except Exception as e:
            self.logger.error(f"Error with group action button: {str(e)}")
            return {
                'status': 'retry',
                'reason': str(e)
            }

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
        """Send message using MessageSender"""
        return self.message_sender.send_message(message)

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