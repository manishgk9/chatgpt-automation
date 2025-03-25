# ChatGPT Automation using Selenium and Python

## Watch the demo of this project:
https://github.com/user-attachments/assets/8b21a0d8-0bca-47e4-88e8-32e974dd506e

This project automates the process of interacting with ChatGPT through a web browser using Python, Selenium, and `undetected-chromedriver`. It simulates human-like interactions, manages the browser window, and handles prompts dynamically.

## Features

- **Automated Browsing**: Launches Chrome in an undetected mode to avoid detection.
- **Login Handling**: Automatically handles login popups and stays logged out.
- **Human-like Interaction**: Introduces random delays between actions to simulate human behavior.
- **Prompt Automation**: Sends prompts to ChatGPT and retrieves the responses.
- **Session Management**: Opens and closes the browser session cleanly, logging all actions.

## Requirements

- Python 3.x
- `pip` (for installing Python packages)

### Required Python Libraries

To run this project, install the required libraries using `pip`:

```bash
pip install undetected-chromedriver selenium fake_useragent pyautogui
````

## Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/chatgpt-automation.git
   cd chatgpt-automation
   ```

2. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the automation**:

   To start the automation script, execute:

   ```bash
   python chatgpt_automation.py
   ```

   The script will:

   - Open a Chrome window.
   - Navigate to the ChatGPT website.
   - Handle any login popups (if they appear).
   - Prompt you for input, send it to ChatGPT, and display the response.

4. **Exit the session**:

   Type `exit` when you're done interacting with ChatGPT to close the session.

## Code Explanation

### `ChatGPTAutomation` Class

The main class for interacting with ChatGPT, it manages the browser session and sends prompts.

- **`__init__`**: Initializes the Chrome browser using `undetected-chromedriver`, sets up the window size, and handles initial setup.
- **`_navigate_to_chatgpt`**: Opens ChatGPT in the browser and handles the login popup if it appears.
- **`handle_login_popup`**: Dismisses the login popup if present.
- **`send_prompt`**: Sends a user-provided prompt to ChatGPT and waits for the response.
- **`close`**: Closes the browser session cleanly.

### Random Time Delays

The `time_delay` function introduces random delays to simulate human-like behavior and avoid being flagged by anti-bot mechanisms.

### `run_chatgpt_session` Function

This function runs an interactive session. It continuously accepts user input, sends it to ChatGPT, and prints the response until the user types `exit`.

### SafeChrome Class

A subclass of `undetected_chromedriver.Chrome` to ensure safe browser termination and avoid errors when closing the browser.

## Logging

The script logs interactions, including browser initialization, login handling, prompt submission, and response retrieval, in a `chatgpt_automation.log` file.

## Troubleshooting

- **Issue with WebDriver**: Ensure you have the latest version of Chrome installed and that `undetected-chromedriver` is working with your version of Chrome.
- **Login Issues**: If the login popup doesn't dismiss correctly, ensure the website layout hasn't changed or the XPaths are updated.
