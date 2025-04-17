# Website Screenshot Tool

This tool takes a list of websites from a text file, captures screenshots of each website, and saves them with the website URL as the filename (with special characters removed).

## Requirements

- Windows OS
- Python 3.7 or newer
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

2. The tool will process each website and save screenshots to a `screenshots` folder

## Example

If your text file contains:
```
google.com
github.com
wikipedia.org
```

The tool will create:
- screenshots/google_com.png
- screenshots/github_com.png  
- screenshots/wikipedia_org.png

## Troubleshooting

- If you get an error about Chrome not being found, install Google Chrome browser
- If you get security errors, try running the batch files as administrator
- For large websites, the tool might time out. You can increase the timeout in the script if needed

## How It Works

The tool uses Selenium and ChromeDriver to:
1. Open a headless (invisible) Chrome browser
2. Navigate to each website
3. Wait for the page to load
4. Take a square screenshot (1024×1024 pixels)
5. Save it with a sanitized filename

## License

This tool is provided as-is for personal use.