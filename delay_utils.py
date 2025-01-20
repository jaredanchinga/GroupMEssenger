import time
import random

def random_delay():
    """Fixed 5 second delay for page loads"""
    time.sleep(5)

def click_delay():
    """Shorter random delay between 3-5 seconds for clicking actions"""
    delay = random.uniform(3, 5)
    time.sleep(delay)

def profile_switch_delay():
    """15 second delay for profile switching"""
    time.sleep(15) 