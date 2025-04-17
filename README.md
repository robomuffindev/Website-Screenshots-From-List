# Website Screenshot Tool

A comprehensive tool for capturing high-quality website screenshots from a list of URLs.

## Overview

This application takes a list of website URLs from a text file and captures screenshots with two different methods:
- **Regular Screenshots**: Fixed 1920×1920 square screenshots
- **Full-Page Screenshots**: Full-height screenshots with 1920px width

Both modes capture two shots per website:
- An initial screenshot taken immediately after page load
- A final screenshot taken after extended loading and scrolling

## Directory Structure

```
WebsiteScreenshotTool/
├── scripts/                       # Python scripts
│   ├── website_screenshot.py      # Regular screenshots script
│   ├── website_screenshot_full.py # Full-page screenshots script
│   └── website_screenshot_gui.py  # GUI interface script
├── batch/                         # Original batch files (backup)
│   ├── run.bat                    # Original runner script
│   ├── run-full.bat               # Original full-page runner
│   ├── run-gui.bat                # Original GUI runner
│   └── setup.bat                  # Original setup script
├── docs/                          # Documentation
│   ├── README.md                  # Regular screenshots documentation
│   ├── README-FULL.md             # Full-page screenshots documentation
│   └── README-GUI.md              # GUI interface documentation
├── drivers/                       # ChromeDriver files (auto-managed)
├── screenshots/                   # Regular screenshots output
│   └── YYYY-MM-DD_HH-MM-SS/       # Timestamped output folders
├── screenshots_full/              # Full-page screenshots output
│   └── YYYY-MM-DD_HH-MM-SS/       # Timestamped output folders
├── url-lists/                     # Additional URL lists
├── venv/                          # Python virtual environment
├── run.bat                        # Regular screenshots launcher
├── run-full.bat                   # Full-page screenshots launcher
├── run-gui.bat                    # GUI interface launcher
├── setup.bat                      # Environment setup script
├── cleanup.bat                    # Screenshot management utility
├── urls.txt                       # Default URL list
└── .gitignore                     # Git ignore file
```

## Setup

1. **Initial Setup**
   ```
   setup.bat
   ```
   This creates a Python virtual environment and installs necessary dependencies.

2. **URL List**
   Create a `urls.txt` file in the root directory with one URL per line:
   ```
   google.com
   github.com
   example.com
   ```

## Usage Options

### Command Line

1. **Regular Screenshots (1920×1920)**
   ```
   run.bat [url-file.txt]
   ```
   If no file is specified, `urls.txt` in the root directory is used.

2. **Full-Page Screenshots (1920×height)**
   ```
   run-full.bat [url-file.txt]
   ```
   Creates full-height screenshots with 1920px width.

### Graphical Interface

```
run-gui.bat
```

The GUI provides:
- URL file selection
- Choice between regular and full-page screenshots
- Real-time progress tracking
- Start/stop controls

## Output

Screenshots are organized in timestamped folders:

- **Regular Screenshots**:
  ```
  screenshots/2025-04-16_14-30-45/example_com_initial.png
  screenshots/2025-04-16_14-30-45/example_com_final.png
  ```

- **Full-Page Screenshots**:
  ```
  screenshots_full/2025-04-16_14-30-45/example_com_initial_full.png
  screenshots_full/2025-04-16_14-30-45/example_com_final_full.png
  ```

Each output folder contains a `summary.txt` with details about the capture session.

## Maintenance

Use `cleanup.bat` to manage screenshot directories:
- View all screenshot directories
- Clean up old or unneeded screenshots
- Remove unnecessary ChromeDriver files

## Technical Details

- Automatically detects Chrome version and downloads appropriate ChromeDriver
- Handles lazy-loaded content through scrolling
- Captures initial state before animations/sliders activate
- High-resolution 1920px width for all screenshots
- Extended timeouts for complex websites
- Designed for Windows with Chrome browser

## Requirements

- Windows OS
- Python 3.7 or newer
- Google Chrome browser
- Internet connection
