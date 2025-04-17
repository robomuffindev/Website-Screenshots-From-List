import os
import sys
import time
import re
import urllib.request
import zipfile
import platform
import subprocess
import json
import shutil
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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

def get_chrome_path():
    """Try to find Chrome or Chromium on the system."""
    if platform.system() == 'Windows':
        paths = [
            os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Google\\Chrome\\Application\\chrome.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'), 'Google\\Chrome\\Application\\chrome.exe'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google\\Chrome\\Application\\chrome.exe')
        ]
        for path in paths:
            if os.path.exists(path):
                return path
    elif platform.system() == 'Linux':
        try:
            chrome_path = subprocess.check_output(['which', 'google-chrome']).decode('utf-8').strip()
            return chrome_path
        except:
            try:
                chrome_path = subprocess.check_output(['which', 'chromium-browser']).decode('utf-8').strip()
                return chrome_path
            except:
                pass
    elif platform.system() == 'Darwin':  # MacOS
        paths = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium'
        ]
        for path in paths:
            if os.path.exists(path):
                return path
    
    return None

def get_chrome_version(chrome_path):
    """Get Chrome version."""
    try:
        if platform.system() == 'Windows':
            # Method 1: Try using wmic
            try:
                output = subprocess.check_output(
                    'wmic datafile where name="%s" get Version /value' % chrome_path.replace('\\', '\\\\'),
                    shell=True
                ).decode('utf-8').strip()
                version_match = re.search(r'Version=(.+)', output)
                if version_match:
                    return version_match.group(1)
            except Exception as e:
                print(f"WMIC method failed: {e}")
                
            # Method 2: Try using PowerShell
            try:
                command = f'powershell -command "(Get-Item \'{chrome_path}\').VersionInfo.ProductVersion"'
                output = subprocess.check_output(command, shell=True).decode('utf-8').strip()
                if output:
                    return output
            except Exception as e:
                print(f"PowerShell method failed: {e}")
                
            # Method 3: Try running Chrome with --version
            try:
                command = f'"{chrome_path}" --version'
                output = subprocess.check_output(command, shell=True).decode('utf-8').strip()
                version_match = re.search(r'Chrome\s+(\d+\.\d+\.\d+\.\d+)', output)
                if version_match:
                    return version_match.group(1)
            except Exception as e:
                print(f"Chrome --version method failed: {e}")
                
            # Method 4: Get major version from directory structure
            try:
                chrome_dir = os.path.dirname(chrome_path)
                version_file = os.path.join(chrome_dir, "chrome.dll")
                if os.path.exists(version_file):
                    # Get version using Windows file properties via PowerShell
                    command = f'powershell -command "(Get-Item \'{version_file}\').VersionInfo.ProductVersion"'
                    output = subprocess.check_output(command, shell=True).decode('utf-8').strip()
                    if output:
                        return output
            except Exception as e:
                print(f"File properties method failed: {e}")
                
            # Method 5: Hard-coded major version as fallback
            print("All automatic version detection methods failed. Using latest ChromeDriver.")
            return "135.0.0.0"  # Assuming Chrome 135 based on the error message
            
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            cmd = f'"{chrome_path}" --version'
            output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
            match = re.search(r'Chrome\s+(\d+\.\d+\.\d+\.\d+)', output)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Error getting Chrome version: {e}")
    
    return None

def get_latest_driver_version():
    """Get the latest version from Chrome for Testing JSON API."""
    try:
        # Get the latest version from the Chrome for Testing API
        url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        # Get the stable version
        latest_version = data.get('channels', {}).get('Stable', {}).get('version')
        if latest_version:
            print(f"Found latest stable Chrome version: {latest_version}")
            return latest_version
            
    except Exception as e:
        print(f"Error getting latest driver version: {e}")
        
    # Fallback version if we can't get the latest
    return "124.0.6367.0"  # Known working version

def get_chromedriver_url(chrome_version):
    """Get the appropriate ChromeDriver URL for the installed Chrome version."""
    try:
        # Get major version
        major_version = chrome_version.split('.')[0]
        print(f"Using Chrome major version: {major_version}")
        
        # Get the latest compatible version from the Chrome for Testing API
        latest_version = get_latest_driver_version()
        
        # Platform detection
        platform_name = None
        if platform.system() == 'Windows':
            platform_name = "win64"
        elif platform.system() == 'Linux':
            platform_name = "linux64"
        elif platform.system() == 'Darwin':
            if platform.machine() == 'arm64':  # M1/M2 Mac
                platform_name = "mac-arm64"
            else:
                platform_name = "mac-x64"
                
        # New URL format
        download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{latest_version}/{platform_name}/chromedriver-{platform_name}.zip"
        print(f"Using Chrome for Testing URL: {download_url}")
        return download_url
            
    except Exception as e:
        print(f"Error determining ChromeDriver URL: {e}")
        # Use a known working version as fallback
        if platform.system() == 'Windows':
            return "https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.0/win64/chromedriver-win64.zip"
        elif platform.system() == 'Linux':
            return "https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.0/linux64/chromedriver-linux64.zip"
        elif platform.system() == 'Darwin':
            if platform.machine() == 'arm64':  # M1/M2 Mac
                return "https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.0/mac-arm64/chromedriver-mac-arm64.zip"
            else:
                return "https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.0/mac-x64/chromedriver-mac-x64.zip"

def download_chromedriver(chrome_version):
    """Download and setup ChromeDriver based on Chrome version."""
    current_platform = platform.system().lower()
    
    # Create drivers directory if it doesn't exist
    driver_dir = os.path.join(os.getcwd(), 'drivers')
    os.makedirs(driver_dir, exist_ok=True)
    
    # Path to chromedriver
    chromedriver_path = os.path.join(driver_dir, 'chromedriver.exe' if current_platform == 'windows' else 'chromedriver')
    
    # Get ChromeDriver download URL
    download_url = get_chromedriver_url(chrome_version)
    if not download_url:
        print("Failed to determine ChromeDriver download URL")
        return None
    
    print(f"Using ChromeDriver download URL: {download_url}")
    
    try:
        # Download ChromeDriver
        print("Downloading ChromeDriver...")
        zip_path = os.path.join(driver_dir, 'chromedriver.zip')
        urllib.request.urlretrieve(download_url, zip_path)
        
        # Extract ChromeDriver
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Check if the zip contains a directory structure (newer Chrome versions)
            file_list = zip_ref.namelist()
            has_directory = any('/' in name for name in file_list)
            
            if has_directory:
                # Extract all files to temporary directory
                temp_dir = os.path.join(driver_dir, 'temp')
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                os.makedirs(temp_dir, exist_ok=True)
                zip_ref.extractall(temp_dir)
                
                # Find the chromedriver executable
                chromedriver_exe = None
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file == 'chromedriver.exe' or file == 'chromedriver':
                            chromedriver_exe = os.path.join(root, file)
                            break
                    if chromedriver_exe:
                        break
                
                if chromedriver_exe:
                    # Copy to final location
                    if os.path.exists(chromedriver_path):
                        os.remove(chromedriver_path)
                    shutil.copy(chromedriver_exe, chromedriver_path)
                    print(f"Copied ChromeDriver from {chromedriver_exe} to {chromedriver_path}")
                else:
                    print("Could not find chromedriver in the extracted files")
                    print("Files found:", os.listdir(temp_dir))
                    return None
                    
                # Clean up temp directory
                shutil.rmtree(temp_dir, ignore_errors=True)
            else:
                # Direct extraction for older versions
                if os.path.exists(chromedriver_path):
                    os.remove(chromedriver_path)
                zip_ref.extractall(driver_dir)
        
        # Make executable on Unix-like systems
        if current_platform != 'windows':
            os.chmod(chromedriver_path, 0o755)
        
        # Clean up
        os.remove(zip_path)
        
        print("ChromeDriver setup complete.")
        return chromedriver_path
    except Exception as e:
        print(f"Error setting up ChromeDriver: {e}")
        return None

def take_screenshot(url, output_dir, chromedriver_path, chrome_path=None):
    """Take two screenshots of the website and save them."""
    sanitized_url = sanitize_filename(url)
    full_url = ensure_protocol(url)
    initial_output_path = os.path.join(output_dir, f"{sanitized_url}_initial.png")
    final_output_path = os.path.join(output_dir, f"{sanitized_url}_final.png")
    success = False
    
    print(f"Processing: {url}")
    
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Updated for Chrome 115+
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1920")  # Square viewport at larger resolution
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL errors
    
    if chrome_path:
        chrome_options.binary_location = chrome_path
    
    try:
        # Initialize the Chrome driver
        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set page load timeout to 60 seconds for larger screenshots
        driver.set_page_load_timeout(60)
        
        try:
            # Navigate to the URL
            driver.get(full_url)
            
            # Take initial screenshot immediately
            driver.save_screenshot(initial_output_path)
            print(f"Initial screenshot saved to: {initial_output_path}")
            
            # Flag to track if we have at least the initial screenshot
            initial_success = True
            
            # Try for the final screenshot
            try:
                # Wait longer for the page to fully load (needed for higher resolution)
                time.sleep(10)
                
                # Scroll down and up to ensure all lazy-loaded elements are loaded
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(2)
                
                # Take final screenshot after everything is loaded
                driver.save_screenshot(final_output_path)
                print(f"Final screenshot saved to: {final_output_path}")
                
                # Both screenshots succeeded
                success = True
            except Exception as final_error:
                # If we at least got the initial screenshot, log the error but don't lose the initial success
                print(f"Error taking final screenshot: {final_error}")
                if initial_success:
                    # Consider it a partial success if we got at least the initial screenshot
                    success = True
        except Exception as nav_error:
            print(f"Error navigating to URL: {nav_error}")
            
    except TimeoutException:
        print(f"Timeout while loading {url}")
    except WebDriverException as e:
        print(f"Error accessing {url}: {e}")
    except Exception as e:
        print(f"Unexpected error with {url}: {e}")
        print(traceback.format_exc())
    finally:
        if 'driver' in locals():
            try:
                driver.quit()
            except:
                pass
    
    return success

def process_websites(input_file):
    """Process all websites from the input file."""
    # Create a timestamped folder for this run
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join(os.getcwd(), "screenshots", timestamp)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Screenshots will be saved to: {os.path.abspath(output_dir)}")
    
    # Get Chrome path
    chrome_path = get_chrome_path()
    if not chrome_path:
        print("Error: Chrome browser not found. Please install Google Chrome.")
        return
    
    print(f"Found Chrome at: {chrome_path}")
    
    # Get Chrome version
    chrome_version = get_chrome_version(chrome_path)
    if not chrome_version:
        print("Error: Could not determine Chrome version. Using Chrome 135.")
        chrome_version = "135.0.0.0"  # Fallback version
    
    print(f"Detected Chrome version: {chrome_version}")
    
    # Download matching ChromeDriver
    chromedriver_path = download_chromedriver(chrome_version)
    if not chromedriver_path:
        print("Error: Failed to download or locate ChromeDriver. Cannot continue.")
        return
    
    print(f"Using ChromeDriver at: {chromedriver_path}")
    
    try:
        # Read URLs from the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
        
        if not urls:
            print("No valid URLs found in the file.")
            return
        
        print(f"Found {len(urls)} URLs to process")
        
        # Process each URL
        successful = 0
        failed = 0
        
        for url in urls:
            if take_screenshot(url, output_dir, chromedriver_path, chrome_path):
                successful += 1
            else:
                failed += 1
            
        print("\nFinished processing all URLs")
        print(f"Results: {successful} successful, {failed} failed")
        print(f"Screenshots saved in: {os.path.abspath(output_dir)}")
        
        # Create a summary file
        summary_path = os.path.join(output_dir, "summary.txt")
        with open(summary_path, "w", encoding='utf-8') as summary_file:
            summary_file.write(f"Screenshot Run on {timestamp}\n")
            summary_file.write(f"Total URLs: {len(urls)}\n")
            summary_file.write(f"Successful: {successful}\n")
            summary_file.write(f"Failed: {failed}\n\n")
            summary_file.write("URLs processed:\n")
            for url in urls:
                summary_file.write(f"- {url}\n")
        
        print(f"Summary saved to: {summary_path}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"Error processing websites: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    # Check if input file is provided
    if len(sys.argv) < 2:
        print("Usage: python website_screenshot.py <input-file.txt>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    process_websites(input_file)
    
    # Keep console window open if run from batch file
    input("\nPress Enter to exit...")