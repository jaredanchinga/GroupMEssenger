import sys
import time
from ixbrowser_local_api import IXBrowserClient

# Initialize the IX Browser client with explicit host and port
client = IXBrowserClient(target='127.0.0.1', port=53200)
client.show_request_log = False  # Disable debug logging

try:
    # Get all profiles with no pagination to see everything
    profiles = client.get_profile_list(page=1, limit=100)
    if profiles is None:
        print('Error getting profile list:')
        print('Error code:', client.code)
        print('Error message:', client.message)
        sys.exit(1)

    if len(profiles) == 0:
        print('No profiles found. Please create a profile first.')
        sys.exit(1)

    # Get list of profile IDs and sort them
    profile_ids = [profile['profile_id'] for profile in profiles]
    profile_ids.sort()  # Sort in ascending order

    # Process each profile ID in order
    for i, profile_id in enumerate(profile_ids):
        print(f'[{i+1}/{len(profile_ids)}] Attempting to open profile {profile_id}...')

        # Open the profile with default settings
        result = client.open_profile(
            profile_id,
            cookies_backup=True,
            load_extensions=True,
            load_profile_info_page=False,
            disable_extension_welcome_page=True
        )
        
        if result is None:
            print(f'Error opening profile {profile_id}')
            continue  # Skip to next profile if this one fails

        print('Waiting 120 seconds...')
        time.sleep(120)

        close_result = client.close_profile(profile_id)
        if close_result is None:
            print(f'Error closing profile {profile_id}')
            continue

    print("\nAll profiles have been processed!")

except Exception as e:
    print(f"Unexpected error occurred: {str(e)}")
    sys.exit(1) 