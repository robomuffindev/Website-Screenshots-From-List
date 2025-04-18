# Website Screenshot Tool

A versatile tool for capturing high-quality screenshots of websites from a text list of URLs, with integrated image processing capabilities.

## Features

- **Two screenshot modes**:
  - **Regular mode**: Fixed 1920×1920 square screenshots
  - **Full-page mode**: Full-height screenshots with 1920px width
- **Dual capture for each website**:
  - Initial screenshot (immediate capture after page load)
  - Final screenshot (after extended loading and scrolling)
- **Image processing options**:
  - Resize images to custom width (maintaining aspect ratio)
  - Convert images to WebP format for optimization
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

1. Download or clone this repository
2. Run the setup script:
   ```
   setup.bat
   ```
   
   The setup will automatically:
   - Create a virtual environment
   - Install required dependencies (Selenium and Pillow)
   - Create necessary directories
   - Create a default URLs file if none exists

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
4. Set image processing options if desired:
   - Check/uncheck "Resize Images After Process"
   - Set width for resized images
   - Check/uncheck "Save as WebP Format"
5. Click "Start Screenshot Process"
6. After screenshots complete, click "Process Latest Images" to process them using your settings
7. Monitor progress in the GUI log window

#### Using Command Line

For regular screenshots:
```
run.bat [url-file.txt]
```

For full-page screenshots:
```
run-full.bat [url-file.txt]
```

### Alternative Image Processing

If you prefer using the command line for image processing, you can use:

```
process_images.bat
```

This will:
1. Automatically find your most recent screenshot directory
2. Prompt you for image processing options
3. Process the images accordingly

You can also specify a directory and width:
```
process_images.bat "path\to\screenshot\folder" 1200
```

### Output

Screenshots are organized in timestamped folders:

```
screenshots/
└── 2025-04-16_14-30-45/
    ├── google_com_initial.png
    ├── google_com_final.png
    ├── summary.txt
    ├── resized/               # Created by image processor
    │   ├── google_com_initial.png
    │   └── google_com_final.png
    └── webp/                  # Created by image processor
        ├── google_com_initial.webp
        └── google_com_final.webp

screenshots_full/
└── 2025-04-16_14-35-12/
    ├── google_com_initial_full.png
    ├── google_com_final_full.png
    ├── summary.txt
    ├── resized/               # Created by image processor
    │   ├── google_com_initial_full.png
    │   └── google_com_final_full.png
    └── webp/                  # Created by image processor
        ├── google_com_initial_full.webp
        └── google_com_initial_full.webp
```

## Workflow Examples

### Basic GUI Workflow

1. Run `setup.bat` (first time only)
2. Edit `urls.txt` with your websites
3. Run `launch-gui.bat`
4. Choose screenshot type
5. Set image processing options
6. Click "Start Screenshot Process"
7. Wait for completion
8. Click "Process Latest Images" button
9. View results in the log window

### Command Line Workflow

1. Prepare URL list in a text file
2. Run `run.bat` or `run-full.bat` with your URL file
3. After completion, run `process_images.bat`
4. Specify processing options when prompted

## Technical Details

### Screenshot Process

The tool uses:
1. **Selenium** with Chrome in headless mode
2. **ChromeDriver** for browser control (auto-downloaded)
3. **Extended wait times** to handle complex websites:
   - 10 seconds after initial page load
   - 3 seconds after scrolling to bottom 
   - 2 seconds after scrolling back to top

### Image Processing

The image processor uses:
1. **PIL/Pillow** for image manipulation
2. **LANCZOS resampling** for high-quality resizing
3. **90% quality WebP** for good compression-to-quality ratio

## Project Files

```
WebsiteScreenshotTool/
├── website_screenshot.py       # Regular screenshots script
├── website_screenshot_full.py  # Full-page screenshots script
├── simple_gui.py               # GUI interface with image processing button
├── process_last_screenshots.py # Standalone image processor script
├── launch-gui.bat              # GUI launcher
├── run.bat                     # Regular screenshots launcher
├── run-full.bat                # Full-page screenshots launcher
├── process_images.bat          # Command-line image processor launcher
├── setup.bat                   # Environment setup
├── README.md                   # This file
└── urls.txt                    # Default URL list
```

## GUI Interface Guide

### Main Controls

- **URL File**: Select the text file containing your list of websites
- **Screenshot Type**: Choose between regular (square) or full-page screenshots
- **Image Processing Options**: Set options for post-processing images
  - Resize Images: Reduces the width to the specified value
  - WebP Conversion: Creates optimized WebP copies of images
- **Buttons**:
  - Start Screenshot Process: Begin taking screenshots
  - Stop: Cancel the current process
  - Process Latest Images: Apply image processing to the most recent screenshot directory

### Workflow

1. Configure settings (URL file, screenshot type, processing options)
2. Click "Start Screenshot Process"
3. Monitor progress in the log window
4. When screenshots are complete, click "Process Latest Images"
5. View the results in the log window

## Troubleshooting

- **ChromeDriver issues**: The tool automatically downloads the correct ChromeDriver version for your Chrome browser. If you update Chrome, run the tool again to get a matching driver.

- **Image processing errors**: If you encounter issues with the "Process Latest Images" button, try using the separate `process_images.bat` script.

- **Screenshot quality**: For complex websites, you might need to adjust the wait times in the script files to ensure all elements load properly.

- **RAM usage**: For very long webpages in full-page mode, you might experience high memory usage. Consider processing fewer URLs at once.

- **Character encoding errors**: The script handles UTF-8 encoding for all file operations. If you encounter encoding errors, ensure your console supports UTF-8.

## License

This tool is provided as-is for personal use.