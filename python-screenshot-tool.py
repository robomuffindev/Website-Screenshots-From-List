import os
import sys
import time
from urllib.parse import urlparse
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException

def sanitize_filename(url):
    """Convert URL to a valid filename by removing special characters."""
    # Remove protocol (http://, https://)
    filename = re.sub(r'^(https?:\/\/)', '', url)
    
    # Replace special characters with underscores
    filename = re.sub(r'[^a-zA-Z0-9.]', '_', filename)
    
    return filename

def ensure_protocol(url):
    """Ensure URL has a protocol."""
    if not url.startswith('http://') and not url.startswith('https://'):
        return 'https://' + url
    return url

def take_screenshot(url, output_dir):
    """Take a screenshot of the website and save it."""
    sanitized_url = sanitize_filename(url)
    full_url = ensure_protocol(url)
    output_path = os.path.join(output_dir, f"{sanitized_url}.png")
    
    print(f"Processing: {url}")
    
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1024,1024")  # Square viewport
    
    try:
        # Initialize the Chrome driver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Set page load timeout
        driver.set_page_load_timeout(30)
        
        # Navigate to the URL
        driver.get(full_url)
        
        # Wait for the page to load
        time.sleep(3)
        
        # Take screenshot
        driver.save_screenshot(output_path)
        print(f"✓ Screenshot saved to: {output_path}")
        
    except TimeoutException:
        print(f"✗ Timeout while loading {url}")
    except WebDriverException as e:
        print(f"✗ Error accessing {url}: {e}")
    except Exception as e:
        print(f"✗ Unexpected error with {url}: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

def process_websites(input_file):
    """Process all websites from the input file."""
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Read URLs from the input file
        with open(input_file, 'r') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
        
        if not urls:
            print("No valid URLs found in the file.")
            return
        
        print(f"Found {len(urls)} URLs to process")
        
        # Process each URL
        for url in urls:
            take_screenshot(url, output_dir)
            
        print("\nFinished processing all URLs")
        print(f"Screenshots saved in: {os.path.abspath(output_dir)}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"Error processing websites: {e}")

if __name__ == "__main__":
    # Check if input file is provided
    if len(sys.argv) < 2:
        print("Usage: python website_screenshot.py <input-file.txt>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    process_websites(input_file)
    
    # Keep console window open if run from batch file
    input("\nPress Enter to exit...")
