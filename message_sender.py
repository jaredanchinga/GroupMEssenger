from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time
import logging
from delay_utils import random_delay, click_delay

class MessageSender:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def send_message(self, message):
        """Send message to group"""
        try:
            random_delay()  # Keep longer delay before finding input
            message_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id, 'message-composer-')]"))
            )
            
            self.logger.info("Found message input, attempting to send message...")
            pyperclip.copy(message)
            click_delay()  # Shorter delay before clicking
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