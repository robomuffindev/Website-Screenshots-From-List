import os
import sys
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
import threading
import subprocess
import time
import queue
import glob

class WebsiteScreenshotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Website Screenshot Tool")
        self.root.geometry("800x700")
        self.root.minsize(800, 700)
        
        # Set up queue for threaded output
        self.queue = queue.Queue()
        self.update_interval = 100  # milliseconds
        
        # Initialize variables
        self.url_file_path = tk.StringVar(value=os.path.join(os.getcwd(), "urls.txt"))
        self.progress_var = tk.DoubleVar(value=0.0)
        self.status_var = tk.StringVar(value="Ready")
        self.total_urls = 0
        self.processed_urls = 0
        self.last_output_dir = None  # Track the last output directory
        self.processing_active = False  # Flag to track if processing is currently active
        
        # Image processing options
        self.resize_images = tk.BooleanVar(value=True)
        self.resize_width = tk.IntVar(value=800)
        self.save_webp = tk.BooleanVar(value=True)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create and place widgets
        self.create_widgets(main_frame)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)  # Increased for the new option
        
        # Start queue processing
        self.process_queue()
        
        # Start status monitor
        self.monitor_process_status()
        
    def create_widgets(self, parent):
        # URL File Selection
        file_frame = ttk.LabelFrame(parent, text="URL File", padding="10")
        file_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        url_entry = ttk.Entry(file_frame, textvariable=self.url_file_path, width=50)
        url_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        file_frame.columnconfigure(0, weight=1)
        
        browse_button = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_button.grid(row=0, column=1, sticky="e", padx=5, pady=5)
        
        # Screenshot Type Selection
        type_frame = ttk.LabelFrame(parent, text="Screenshot Type", padding="10")
        type_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        self.screenshot_type = tk.StringVar(value="regular")
        
        regular_radio = ttk.Radiobutton(
            type_frame, 
            text="Regular Screenshots (1920x1920)", 
            variable=self.screenshot_type, 
            value="regular"
        )
        regular_radio.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        widescreen_radio = ttk.Radiobutton(
            type_frame, 
            text="Widescreen Screenshots (1920x1080)", 
            variable=self.screenshot_type, 
            value="widescreen"
        )
        widescreen_radio.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        fourbythree_radio = ttk.Radiobutton(
            type_frame, 
            text="4:3 Aspect Ratio (1920x1440)", 
            variable=self.screenshot_type, 
            value="fourbythree"
        )
        fourbythree_radio.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        
        full_radio = ttk.Radiobutton(
            type_frame, 
            text="Full-Page Screenshots (1920xHeight)", 
            variable=self.screenshot_type, 
            value="full"
        )
        full_radio.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        
        # Image Processing Options
        process_frame = ttk.LabelFrame(parent, text="Image Processing Options", padding="10")
        process_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        process_frame.columnconfigure(1, weight=1)
        
        # Resize Images Option
        resize_check = ttk.Checkbutton(
            process_frame, 
            text="Resize Images After Process", 
            variable=self.resize_images
        )
        resize_check.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Width Entry
        ttk.Label(process_frame, text="Width:").grid(row=0, column=1, sticky="e", padx=5, pady=5)
        width_entry = ttk.Entry(process_frame, textvariable=self.resize_width, width=5)
        width_entry.grid(row=0, column=2, sticky="e", padx=5, pady=5)
        
        # WebP Option
        webp_check = ttk.Checkbutton(
            process_frame, 
            text="Save as WebP Format", 
            variable=self.save_webp
        )
        webp_check.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        # Control Buttons
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        
        start_button = ttk.Button(
            button_frame, 
            text="Start Screenshot Process", 
            command=self.start_process
        )
        start_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        stop_button = ttk.Button(
            button_frame, 
            text="Stop", 
            command=self.stop_process
        )
        stop_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Add Process Images Button
        process_button = ttk.Button(
            button_frame,
            text="Process Latest Images",
            command=self.process_latest_images
        )
        process_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Status and Progress
        status_frame = ttk.LabelFrame(parent, text="Progress", padding="10")
        status_frame.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        
        # Progress bar (the status bar indicator has been removed)
        self.progress_bar = ttk.Progressbar(
            status_frame, 
            variable=self.progress_var, 
            maximum=100.0
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Log Display
        log_frame = ttk.LabelFrame(status_frame, text="Output Log", padding="10")
        log_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure weight for expanding widgets
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(1, weight=1)
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select URL File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.url_file_path.set(file_path)
    
    def start_process(self):
        # Check if file exists
        if not os.path.exists(self.url_file_path.get()):
            self.log_text.insert(tk.END, f"Error: File {self.url_file_path.get()} not found.\n")
            return
        
        # Reset progress
        self.progress_var.set(0.0)
        self.log_text.delete(1.0, tk.END)
        self.processing_active = True
        
        # Count total URLs for progress tracking
        try:
            with open(self.url_file_path.get(), 'r') as f:
                urls = [line.strip() for line in f.readlines() if line.strip()]
            self.total_urls = len(urls)
            self.processed_urls = 0
            self.log_text.insert(tk.END, f"Found {self.total_urls} URLs to process.\n")
        except Exception as e:
            self.log_text.insert(tk.END, f"Error reading URL file: {e}\n")
            self.processing_active = False
            return
        
        # Determine which script to run
        if self.screenshot_type.get() == "regular":
            script_name = "website_screenshot.py"
            output_dir_base = "screenshots"
        elif self.screenshot_type.get() == "widescreen":
            script_name = "website_screenshot_widescreen.py"
            output_dir_base = "screenshots_widescreen"
        elif self.screenshot_type.get() == "fourbythree":
            script_name = "website_screenshot_fourbythree.py"
            output_dir_base = "screenshots_fourbythree"
        else:  # "full"
            script_name = "website_screenshot_full.py"
            output_dir_base = "screenshots_full"
        
        # For widescreen mode, we need to create the script if it doesn't exist
        if self.screenshot_type.get() == "widescreen" and not os.path.exists(script_name):
            self.create_widescreen_script()
            
        # For 4:3 mode, we need to create the script if it doesn't exist
        if self.screenshot_type.get() == "fourbythree" and not os.path.exists(script_name):
            self.create_fourbythree_script()
        
        # Check if the script exists
        if not os.path.exists(script_name):
            self.log_text.insert(tk.END, f"Error: Script {script_name} not found.\n")
            self.log_text.insert(tk.END, "Please make sure the script is in the same directory.\n")
            self.processing_active = False
            return
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir_base):
            os.makedirs(output_dir_base)
        
        # Create and start thread
        self.process_thread = threading.Thread(
            target=self.run_process,
            args=(script_name, self.url_file_path.get(), output_dir_base),
            daemon=True
        )
        self.process_thread.start()
    
    def create_widescreen_script(self):
        """Create the widescreen screenshot script based on the regular one"""
        try:
            # Check if the regular script exists
            if not os.path.exists("website_screenshot.py"):
                self.log_text.insert(tk.END, "Error: Cannot create widescreen script, website_screenshot.py not found.\n")
                return False
            
            # Read the regular script
            with open("website_screenshot.py", 'r') as f:
                script_content = f.read()
            
            # Modify for widescreen (1920x1080)
            script_content = script_content.replace(
                'chrome_options.add_argument("--window-size=1920,1920")',
                'chrome_options.add_argument("--window-size=1920,1080")'
            )
            
            # Replace output directory
            script_content = script_content.replace(
                'output_dir = os.path.join(os.getcwd(), "screenshots", timestamp)',
                'output_dir = os.path.join(os.getcwd(), "screenshots_widescreen", timestamp)'
            )
            
            # Write to new file
            with open("website_screenshot_widescreen.py", 'w') as f:
                f.write(script_content)
            
            self.log_text.insert(tk.END, "Created widescreen screenshot script.\n")
            return True
        except Exception as e:
            self.log_text.insert(tk.END, f"Error creating widescreen script: {e}\n")
            return False
            
    def create_fourbythree_script(self):
        """Create the 4:3 aspect ratio screenshot script based on the regular one"""
        try:
            # Check if the regular script exists
            if not os.path.exists("website_screenshot.py"):
                self.log_text.insert(tk.END, "Error: Cannot create 4:3 script, website_screenshot.py not found.\n")
                return False
            
            # Read the regular script
            with open("website_screenshot.py", 'r') as f:
                script_content = f.read()
            
            # Modify for 4:3 aspect ratio (1920x1440)
            script_content = script_content.replace(
                'chrome_options.add_argument("--window-size=1920,1920")',
                'chrome_options.add_argument("--window-size=1920,1440")'
            )
            
            # Replace output directory
            script_content = script_content.replace(
                'output_dir = os.path.join(os.getcwd(), "screenshots", timestamp)',
                'output_dir = os.path.join(os.getcwd(), "screenshots_fourbythree", timestamp)'
            )
            
            # Write to new file
            with open("website_screenshot_fourbythree.py", 'w') as f:
                f.write(script_content)
            
            self.log_text.insert(tk.END, "Created 4:3 aspect ratio screenshot script.\n")
            return True
        except Exception as e:
            self.log_text.insert(tk.END, f"Error creating 4:3 aspect ratio script: {e}\n")
            return False
    
    def run_process(self, script_name, url_file, output_dir_base):
        try:
            # Start process
            cmd = f'python "{script_name}" "{url_file}"'
            
            self.process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Variables to track output directory
            self.last_output_dir = None
            screenshot_run_completed = False
            
            # Monitor output
            for line in iter(self.process.stdout.readline, ''):
                # Add line to queue for display in the UI
                self.queue.put(line)
                
                # Update progress based on output
                if "Processing:" in line:
                    self.processed_urls += 1
                    progress = (self.processed_urls / self.total_urls) * 100
                    self.progress_var.set(progress)
                
                # Extract output directory from log
                if "Screenshots will be saved to:" in line:
                    self.last_output_dir = line.split("Screenshots will be saved to:")[1].strip()
                    self.queue.put(f"Detected output directory: {self.last_output_dir}\n")
                
                # Check if process was stopped
                if not hasattr(self, 'process'):
                    break
                
                # Check if processing is completed
                if "Finished processing all URLs" in line:
                    screenshot_run_completed = True
                
            # Process has exited - set progress to 100%
            self.queue.put("\nProcess completed.\n")
            self.progress_var.set(100.0)
            self.processing_active = False
            # Force UI to update
            self.root.update_idletasks()
            
            # Prompt for image processing
            if (self.resize_images.get() or self.save_webp.get()) and screenshot_run_completed and self.last_output_dir:
                self.queue.put("\nWould you like to process images now? Use the 'Process Latest Images' button.\n")
            
        except Exception as e:
            self.queue.put(f"Error: {e}\n")
            self.processing_active = False
    
    def monitor_process_status(self):
        """Monitor process status and force update if needed"""
        # Check if process is running but shouldn't be
        if hasattr(self, 'process'):
            if self.process.poll() is not None:  # Process has terminated
                # Process has ended but progress not updated
                self.progress_var.set(100.0)
                self.processing_active = False
                self.root.update_idletasks()
        
        # Schedule next check
        self.root.after(1000, self.monitor_process_status)
    
    def process_latest_images(self):
        """Run the process_last_screenshots.py script with parameters from UI"""
        
        # Reset progress
        self.progress_var.set(0.0)
        self.processing_active = True
        self.queue.put("\n--- Starting Image Processing ---\n")
        
        # Check if we have a known output directory from the last run
        directory_to_process = None
        
        if self.last_output_dir and os.path.exists(self.last_output_dir):
            directory_to_process = self.last_output_dir
            self.queue.put(f"\nUsing last screenshot directory: {directory_to_process}\n")
        else:
            # Find the latest directory ourselves
            self.queue.put("\nLooking for the most recent screenshot directory...\n")
            
            # Define a function to find latest directory in a base dir
            def find_latest_dir(base_dir):
                if not os.path.exists(base_dir):
                    return None
                
                dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
                if not dirs:
                    return None
                
                # Filter directories that match the timestamp pattern
                timestamp_dirs = [d for d in dirs if len(d.split("_")) >= 2 and len(d.split("_")[0].split("-")) >= 3]
                
                if not timestamp_dirs:
                    return None
                
                # Sort by name (which effectively sorts by timestamp)
                timestamp_dirs.sort(reverse=True)
                return os.path.join(base_dir, timestamp_dirs[0])
            
            # Check all screenshot directories
            latest_dirs = {}
            latest_times = {}
            
            for dir_base in ["screenshots", "screenshots_full", "screenshots_widescreen", "screenshots_fourbythree"]:
                latest_dir = find_latest_dir(dir_base)
                if latest_dir:
                    latest_dirs[dir_base] = latest_dir
                    latest_times[dir_base] = os.path.getmtime(latest_dir)
            
            if latest_times:
                # Find the most recent directory
                most_recent_base = max(latest_times.items(), key=lambda x: x[1])[0]
                directory_to_process = latest_dirs[most_recent_base]
                self.queue.put(f"Found most recent directory in {most_recent_base}: {directory_to_process}\n")
            else:
                self.queue.put("No screenshot directories found. Please run the screenshot process first.\n")
                self.progress_var.set(0.0)
                self.processing_active = False
                return
        
        # Now that we have a directory to process, create and run the process
        self.queue.put(f"\nStarting image processing with the following options:\n")
        self.queue.put(f"- Resize: {self.resize_images.get()}\n")
        self.queue.put(f"- Width: {self.resize_width.get()}\n")
        self.queue.put(f"- WebP: {self.save_webp.get()}\n\n")
        
        # Create a temporary script file for processing
        script_content = """
import os
import glob
import sys
from PIL import Image

def process_images(folder_path, resize=True, resize_width=800, save_webp=True):
    print(f"Processing images in folder: {folder_path}")
    print(f"- Resize: {resize} (width={resize_width})")
    print(f"- WebP conversion: {save_webp}")
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist.")
        return
    
    # Get all PNG images in the folder
    png_files = glob.glob(os.path.join(folder_path, "*.png"))
    print(f"Found {len(png_files)} PNG images to process.")
    
    if len(png_files) == 0:
        print("No images to process.")
        return
    
    # Process for resizing
    if resize:
        # Create resized directory
        resized_dir = os.path.join(folder_path, "resized")
        os.makedirs(resized_dir, exist_ok=True)
        print(f"Created resized directory: {resized_dir}")
        
        # Process each image for resizing
        for img_path in png_files:
            img_filename = os.path.basename(img_path)
            resized_path = os.path.join(resized_dir, img_filename)
            
            try:
                # Open and resize the image
                img = Image.open(img_path)
                
                # Calculate new height to maintain aspect ratio
                width_percent = (resize_width / float(img.size[0]))
                target_height = int((float(img.size[1]) * float(width_percent)))
                
                # Resize with LANCZOS resampling for quality
                resized_img = img.resize((resize_width, target_height), Image.LANCZOS)
                resized_img.save(resized_path)
                
                print(f"Resized: {img_filename} to {resize_width}x{target_height}")
                img.close()
            except Exception as e:
                print(f"Error resizing {img_filename}: {e}")
    
    # Process for WebP conversion
    if save_webp:
        # Create WebP directory
        webp_dir = os.path.join(folder_path, "webp")
        os.makedirs(webp_dir, exist_ok=True)
        print(f"Created WebP directory: {webp_dir}")
        
        # Determine source files (original or resized)
        source_files = []
        if resize:
            source_dir = os.path.join(folder_path, "resized")
            source_files = glob.glob(os.path.join(source_dir, "*.png"))
        else:
            source_files = png_files
        
        # Convert each image to WebP
        for img_path in source_files:
            img_filename = os.path.basename(img_path)
            webp_filename = os.path.splitext(img_filename)[0] + ".webp"
            webp_path = os.path.join(webp_dir, webp_filename)
            
            try:
                # Open and convert the image
                img = Image.open(img_path)
                
                # If resize is not already applied but is requested
                if not resize and resize_width > 0:
                    # Calculate new height to maintain aspect ratio
                    width_percent = (resize_width / float(img.size[0]))
                    target_height = int((float(img.size[1]) * float(width_percent)))
                    
                    # Resize with LANCZOS resampling for quality
                    img = img.resize((resize_width, target_height), Image.LANCZOS)
                
                # Save as WebP with good quality
                img.save(webp_path, format="WEBP", quality=90)
                
                print(f"Converted to WebP: {webp_filename}")
                img.close()
            except Exception as e:
                print(f"Error converting {img_filename} to WebP: {e}")
    
    print("Image processing completed.")
    print("\\n==== COMPLETED ====\\n")  # Special marker for completion

if __name__ == "__main__":
    resize = sys.argv[2].lower() == "true"
    resize_width = int(sys.argv[3])
    save_webp = sys.argv[4].lower() == "true"
    
    process_images(sys.argv[1], resize, resize_width, save_webp)
"""
        
        # Create a temporary script file
        temp_script_path = os.path.join(os.getcwd(), "temp_image_processor.py")
        with open(temp_script_path, "w") as f:
            f.write(script_content)
        
        # Run the script in a separate process with parameters from the UI
        cmd = [
            sys.executable, 
            temp_script_path, 
            directory_to_process, 
            str(self.resize_images.get()).lower(), 
            str(self.resize_width.get()), 
            str(self.save_webp.get()).lower()
        ]
        
        # Run in a separate thread
        threading.Thread(
            target=self.run_image_processor,
            args=(cmd, temp_script_path),
            daemon=True
        ).start()
    
    def run_image_processor(self, cmd, temp_script_path):
        """Run the image processor in a separate process"""
        try:
            # Run image processing
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor output
            for line in iter(process.stdout.readline, ''):
                self.queue.put(line)
                
                # Check for completion marker
                if "==== COMPLETED ====" in line:
                    # Update progress to 100%
                    self.progress_var.set(100.0)
                    self.root.update_idletasks()
            
            # Wait for process to complete
            process.wait()
            
            # Clean up
            try:
                os.remove(temp_script_path)
            except:
                pass
                
            # Set progress to 100%
            self.queue.put("\nImage processing completed.\n")
            self.progress_var.set(100.0)
            self.processing_active = False
            self.root.update_idletasks()
            
        except Exception as e:
            self.queue.put(f"Error during image processing: {e}\n")
            import traceback
            self.queue.put(traceback.format_exc())
            self.processing_active = False
    
    def stop_process(self):
        if hasattr(self, 'process'):
            if os.name == 'nt':  # Windows
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])
            else:
                self.process.terminate()
            delattr(self, 'process')
            self.progress_var.set(0.0)
            self.processing_active = False
            self.queue.put("\nProcess stopped by user.\n")
    
    def process_queue(self):
        """Process messages in the queue and update the log widget"""
        try:
            while True:
                # Get a message from the queue without blocking
                message = self.queue.get_nowait()
                # Update the log widget
                self.log_text.insert(tk.END, message)
                self.log_text.see(tk.END)  # Scroll to the end
                self.queue.task_done()
        except queue.Empty:
            # No more messages in the queue
            pass
        finally:
            # Schedule the next queue check - FIXED LINE
            self.root.after(100, self.process_queue)

def main():
    root = tk.Tk()
    app = WebsiteScreenshotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()