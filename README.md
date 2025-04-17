# Website Screenshot Tool

A robust tool for capturing high-quality screenshots of websites from a text list of URLs.

## Features

- **Two screenshot modes**:
  - **Regular mode**: Fixed 1920×1920 square screenshots
  - **Full-page mode**: Full-height screenshots with 1920px width
- **Dual capture for each website**:
  - Initial screenshot (immediate capture after page load)
  - Final screenshot (after extended loading and scrolling)
- **User-friendly GUI interface**
- **Progress tracking**
- **Automatic ChromeDriver detection**
- **Virtual environment isolation**
- **Error recovery and robustness**

## Installation

### Prerequisites

- Windows OS
- Python 3.7+ installed and added to PATH
- Google Chrome browser

### Setup

1. Clone or download this repository
2. Run the launcher:
   ```
   launch-gui.bat
   ```
   
   The launcher will automatically:
   - Create a virtual environment
   - Install required dependencies
   - Create necessary directories
   - Launch the GUI

## Usage

### Preparing URL List

Create a text file with one URL per line:

```
google.com
github.com
example.com
wikipedia.org
```

The default `urls.txt` file in the root directory is used if no other file is selected.

### Taking Screenshots

#### Using the GUI

1. Launch the GUI using `launch-gui.bat`
2. Select your URL file (or use the default)
3. Choose screenshot type:
   - Regular (1920×1920)
   - Full-page (1920×height)
4. Click "Start Screenshot Process"
5. Monitor progress in the GUI

#### Using Command Line

For regular screenshots:
```
run.bat [url-file.txt]
```

For full-page screenshots:
```
run-full.bat [url-file.txt]
```

### Output

Screenshots are organized in timestamped folders:

```
screenshots/
└── 2025-04-16_14-30-45/
    ├── google_com_initial.png
    ├── google_com_final.png
    └── summary.txt

screenshots_full/
└── 2025-04-16_14-35-12/
    ├── google_com_initial_full.png
    ├── google_com_final_full.png
    └── summary.txt
```

Each folder contains:
- Initial and final screenshots for each URL
- A summary file with details about the capture session

## Error Handling

The tool has robust error handling to manage problematic websites:

- **SSL Certificate Errors**: Automatically bypassed
- **Timeouts**: Configurable page load timeouts (default: 60-90 seconds)
- **JavaScript Errors**: Fallback mechanisms when page scripts fail
- **Character Encoding**: UTF-8 encoding for all file operations
- **Partial Success**: Records initial screenshots even if final ones fail
- **Detailed Logging**: Captures and reports detailed error information

## How It Works

The tool uses:
1. **Selenium** with Chrome in headless mode
2. **ChromeDriver** for browser control (auto-downloaded)
3. **Tkinter** for the GUI interface
4. **Virtual environment** for dependency isolation

The screenshot process:
1. Loads each URL in a headless Chrome browser
2. Takes an immediate screenshot
3. Waits 10 seconds for full page loading
4. Scrolls to trigger lazy-loaded content (3 seconds at bottom)
5. Scrolls back to top (2 seconds to stabilize)
6. Takes a final screenshot
7. Moves to the next URL

## Project Structure

```
WebsiteScreenshotTool/
├── website_screenshot.py       # Regular screenshots script
├── website_screenshot_full.py  # Full-page screenshots script
├── simple_gui.py               # GUI interface script
├── launch-gui.bat              # GUI launcher script
├── run.bat                     # Regular screenshots launcher
├── run-full.bat                # Full-page screenshots launcher
├── venv/                       # Virtual environment
├── drivers/                    # ChromeDriver files
├── screenshots/                # Regular screenshots output
├── screenshots_full/           # Full-page screenshots output
└── urls.txt                    # Default URL list
```

## Customization

### Sleep Times

The scripts use these default waiting periods:
- 10 seconds after initial page load
- 3 seconds after scrolling to bottom
- 2 seconds after scrolling back to top

To adjust these for slower websites, modify the `time.sleep()` values in the scripts.

### Screenshot Dimensions

- Regular mode: Fixed 1920×1920 pixels
- Full-page mode: 1920px width with dynamic height (minimum 1080px)

To change these dimensions, modify the `width` and `height` values in the scripts.

## Troubleshooting

- **ChromeDriver issues**: The tool automatically downloads the correct ChromeDriver version for your Chrome browser. If you update Chrome, run the tool again to get a matching driver.

- **Screenshot quality**: For complex websites, you might need to adjust the wait times in the script files to ensure all elements load properly.

- **RAM usage**: For very long webpages in full-page mode, you might experience high memory usage. Consider processing fewer URLs at once.

- **Character encoding errors**: The script handles UTF-8 encoding for all file operations. If you encounter encoding errors, ensure your console supports UTF-8.

## License

MIT License - feel free to use and modify for your own projects.
