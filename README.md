# GroupMe Messenger

A Python-based automation tool for GroupMe messaging using Selenium WebDriver and IX Browser.

## Features

- Automated message sending to multiple GroupMe groups
- Excel-based link management
- GUI interface for easy operation
- Profile management for multiple accounts
- Automated group joining capabilities
- Pause/Resume functionality
- Detailed logging system

## Requirements

- Python 3.7+
- IX Browser
- Chrome WebDriver
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/jaredanchinga/GroupMEssenger.git
   cd GroupMEssenger
   ```
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Install IX Browser and ensure it's properly configured

## Usage

1. Create an Excel file using create_excel.py:
   ```bash
   python create_excel.py
   ```

2. Add your GroupMe group links to the 'links' sheet in the created Excel file

3. Run the application:
   ```bash
   python main_app.py
   ```

4. Select your Excel file, enter your message, and start the automation

## Project Structure

- `main_app.py`: Main application entry point
- `controller.py`: Main application controller
- `browser_controller.py`: Browser automation logic
- `excel_handler.py`: Excel file management
- `gui.py`: GUI implementation
- `profile_manager.py`: IX Browser profile management
- `browser_actions.py`: Browser interaction implementations

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
