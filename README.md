# GroupMe Messenger

A Python-based automation tool for GroupMe messaging using Selenium WebDriver and IX Browser.

## Features

- Automated message sending to multiple GroupMe groups
- GUI interface for easy operation
- Profile management for multiple accounts
- Automated group joining capabilities
- Pause/Resume functionality
- Detailed logging system
- CSV results tracking

## Installation Options

### Option 1: Executable Version (Recommended for Windows Users)
1. Download the latest release from:
   ```
   https://github.com/jaredanchinga/GroupMEssenger/releases/latest
   ```
2. Extract the ZIP file to your preferred location
3. Install IX Browser and ensure it's properly configured
4. Run `GroupMessenger_v1.0.1.exe`

## Profile Setup (Important)
1. Create multiple profiles in IX Browser
2. For each profile:
    - Log into GroupMe account
    - Enable "Save Login" in browser settings
    - Test login by closing and reopening profile
3. Recommended: Set up at least 3-5 profiles
4. Note: Having multiple logged-in profiles helps maintain operation if one gets logged out

## Usage

1. Run the application
2. Paste your GroupMe group links (one per line)
3. Enter your message
4. Click Start to begin automation
5. Use Pause/Resume as needed

## System Requirements

- Windows 10 or later (for .exe version)
- IX Browser installed
- 4GB RAM minimum
- Internet connection

## Project Structure

- `main_app.py`: Main application entry point
- `controller.py`: Main application controller
- `browser_controller.py`: Browser automation logic
- `browser_actions.py`: Browser interaction implementations
- `message_sender.py`: Message sending functionality
- `login_tester.py`: Profile login verification
- `delay_utils.py`: Timing and delay management
- `results_handler.py`: CSV results storage
- `profile_manager.py`: IX Browser profile management
- `gui.py`: GUI implementation

## License

MIT License

Copyright (c) 2025 Jared Anchinga

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 
