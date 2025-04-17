# Website Screenshot Tool

This tool takes a list of websites from a text file, captures high-resolution screenshots of each website, and saves them with the website URL as the filename (with special characters removed).

## Features

- Takes two screenshots of each website:
  - An initial screenshot immediately after page load
  - A final screenshot after extended loading and scrolling
- Uses high resolution 1920x1920 square screenshots
- Saves screenshots in timestamp-organized folders
- Creates a summary report for each run
- Automatically detects and uses the correct Chrome driver
- Sanitizes website URLs to create valid filenames
- Handles modern websites with lazy-loaded content

## Requirements

- Windows OS
- Python 3.7 or newer
- Google Chrome browser
- Internet connection

## Installation

1. Download all the files in this package to a folder on your computer
2. Double-click `setup.bat` to set up the environment (only needs to be done once)
3. Create a text file with your list of websites (one per line)

## Usage

1. Run the tool by double-clicking `run.bat` and dragging your URL text file onto it
   
   OR
   
   Open a command prompt and run:
   ```
   run.bat your-urls.txt
   ```
   
   OR 
   
   Simply double-click `run.bat` to use the default `urls.txt` file

2. The tool will process each website and save screenshots to a timestamped folder inside the `screenshots` directory

## Output Structure

```
screenshots/
├── 2025-04-16_14-30-45/
│   ├── example_com_initial.png
│   ├── example_com_final.png
│   ├── another_website_com_initial.png
│   ├── another_website_com_final.png
│   └── summary.txt
└── 2025-04-16_15-45-12/
    ├── new_site_org_initial.png
    ├── new_site_org_final.png
    ├── my_website_com_initial.png
    ├── my_website_com_final.png
    └── summary.txt
```

Each run creates a new folder with:
- Screenshots named after sanitized website URLs
- A summary.txt file with details about the run

## Example

If your text file contains:
```
google.com
github.com
wikipedia.org
```

The tool will create timestamped folders with:
- google_com_initial.png
- google_com_final.png
- github_com_initial.png
- github_com_final.png
- wikipedia_org_initial.png
- wikipedia_org_final.png
- summary.txt

## Troubleshooting

- If you get an error about Chrome not being found, make sure Google Chrome browser is installed
- If websites appear incomplete, the script may need more time to load content. Try adjusting the wait times in the script.
- For large websites, the tool might time out. You can increase the timeout in the script if needed.
- If you see Chrome version incompatibility errors, the script should automatically resolve these, but you may need to run setup.bat again.

## How It Works

The tool uses:
1. Selenium WebDriver to control Chrome browser in headless mode
2. Chrome browser to render websites properly
3. Chrome's internal screenshot capabilities to capture high-quality images
4. Automatic version detection to ensure compatibility between Chrome and ChromeDriver
5. Dual screenshot approach:
   - Initial screenshot taken immediately after navigation
   - Final screenshot taken after extended loading and scrolling
6. Page scrolling to ensure lazy-loaded content is captured

## Technical Details

- Takes 1920x1920 pixel screenshots
- Waits up to 90 seconds for pages to load
- Scrolls down and up to trigger lazy-loaded content
- Automatically detects Chrome version and downloads appropriate ChromeDriver

## License

This tool is provided as-is for personal use.