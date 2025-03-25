import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import random
import logging
import pyautogui
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='chatgpt_automation.log'
)

def time_delay(time_start=1, time_end=3):
    """Random delay for simulating human-like interaction."""
    return random.uniform(time_start, time_end)

# Subclass Chrome to suppress the OSError in __del__
class SafeChrome(uc.Chrome):
    def __del__(self):
        try:
            super().__del__()
        except OSError:
            print("Session is clossed!")

class ChatGPTAutomation:
    def __init__(self):
        print("Initializing the Chrome browser once.")
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument(f"user-agent={UserAgent().random}")
            self.driver = SafeChrome(options=chrome_options)  # Use SafeChrome instead
            self.driver.set_page_load_timeout(20)

            screen_width, screen_height = pyautogui.size()
            window_width = screen_width // 2.3
            window_height = screen_height
      
            self.driver.set_window_size(window_width, window_height)
            self.driver.set_window_position(0, 0)

            print(f"Browser initialized with size {window_width}x{window_height}.")
            logging.info(f"Browser initialized with size {window_width}x{window_height}.")
        except Exception as e:
            logging.error(f"Failed to initialize browser: {str(e)}")
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
            raise

    def __enter__(self):
        self._navigate_to_chatgpt()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _navigate_to_chatgpt(self):
        """Navigate to ChatGPT."""
        self.driver.get("https://chatgpt.com")
        WebDriverWait(self.driver, time_delay(2, 4))
        self.handle_login_popup()

    def handle_login_popup(self):
        """Handle login popup by clicking 'Stay logged out'."""
        try:
            stay_logged_out = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='dismiss-welcome' and contains(text(), 'Stay logged out')]"))
            )
            stay_logged_out.click()
            logging.info("Login popup handled: clicked 'Stay logged out'.")
            WebDriverWait(self.driver, time_delay())
        except Exception as e:
            logging.error(f"Login popup handling failed: {str(e)}")
            logging.info("Assuming no login popup or already handled.")

    def send_prompt(self, prompt):
        """Send a prompt to ChatGPT and return the response."""
        try:
            
            # Ensure the window is focused before sendini g input
            # self.driver.switch_to.window(self.driver.current_window_handle)
            # self.driver.execute_script("window.focus();")

            input_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "prompt-textarea"))
            )
            self.driver.execute_script("arguments[0].innerText = ''", input_field)
            input_field.send_keys(prompt)
            logging.info(f"Prompt sent: {prompt}")
            WebDriverWait(self.driver, time_delay(1, 2))

            input_field.send_keys(Keys.ENTER)
            logging.info("Prompt submitted via ENTER key.")

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(self.driver, time_delay(2, 3))

            # Wait for the response to start rendering
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "(//div[contains(@class, 'markdown prose w-full')])[last()]"))
            )

           # Wait for response to finish streaming
            WebDriverWait(self.driver, 60).until(
                EC.invisibility_of_element_located((By.XPATH, "//button[@data-testid='stop-button']"))
            )
            WebDriverWait(self.driver, time_delay(1, 2))

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(self.driver, time_delay(1, 2))

            response_container = self.driver.find_element(By.XPATH, "(//div[contains(@class, 'markdown prose w-full')])[last()]")
            response_text = response_container.text.strip()

            if response_text:
                logging.info(f"Response retrieved: {response_text[:50]}...")
                return response_text
            else:
                logging.error("Response text is empty after streaming completed.")
                return None

        except Exception as e:
            logging.error(f"Error during prompt execution: {str(e)}")
            return None
        
    def close(self):
        """Close the browser cleanly."""
        try:
            if hasattr(self, 'driver') and self.driver:
                time.sleep(0.5)  # Small delay to stabilize resources
                self.driver.quit()
                logging.info("Browser closed successfully.")
        except Exception as e:
            logging.error(f"Error closing browser: {str(e)}")

def run_chatgpt_session():
    """Run an interactive session for multiple prompts."""
    try:
        with ChatGPTAutomation() as automation:
            print("ChatGPT session started. Enter prompts (type 'exit' to quit):")
            while True:
                prompt = input("Prompt: ").strip()
                if prompt.lower() == 'exit':
                    print("Closing session.")
                    break

                response = automation.send_prompt(prompt)
                if response:
                    print(f"Response: {response}")
                else:
                    print("Failed to get a response.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    run_chatgpt_session()