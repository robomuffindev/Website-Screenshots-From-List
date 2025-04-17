import os 
import sys 
ECHO is off.
# Add scripts directory to path 
script_dir = os.path.dirname(os.path.abspath(__file__)) 
root_dir = os.path.dirname(script_dir) 
sys.path.insert(0, root_dir) 
ECHO is off.
import os
import sys
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
import threading
import subprocess
import time
import queue

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
sys.path.insert(0, root_dir)

class RedirectText:
    def __init__(self, text_widget, queue):
        self.output = text_widget
        self.queue = queue

    def write(self, string):
        self.queue.put(string)

    def flush(self):
        pass

class WebsiteScreenshotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Website Screenshot Tool")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # Set up queue for threaded output
        self.queue = queue.Queue()
        self.update_interval = 100  # milliseconds
        
        # Initialize variables
        self.url_file_path = tk.StringVar(value=os.path.join(root_dir, "urls.txt"))
        self.progress_var = tk.DoubleVar(value=0.0)
        self.status_var = tk.StringVar(value="Ready")
        self.total_urls = 0
        self.processed_urls = 0
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create and place widgets
        self.create_widgets(main_frame)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Start queue processing
        self.process_queue()
        
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
        
        full_radio = ttk.Radiobutton(
            type_frame, 
            text="Full-Page Screenshots (1920xHeight)", 
            variable=self.screenshot_type, 
            value="full"
        )
        full_radio.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        # Control Buttons
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
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
        
        # Status and Progress
        status_frame = ttk.LabelFrame(parent, text="Status", padding="10")
        status_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.progress_bar = ttk.Progressbar(
            status_frame, 
            variable=self.progress_var, 
            maximum=100.0
        )
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        # Log Display
        log_frame = ttk.LabelFrame(status_frame, text="Output Log", padding="10")
        log_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure weight for expanding widgets
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(2, weight=1)
        
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
        self.status_var.set("Running...")
        
        # Count total URLs for progress tracking
        try:
            with open(self.url_file_path.get(), 'r') as f:
                urls = [line.strip() for line in f.readlines() if line.strip()]
            self.total_urls = len(urls)
            self.processed_urls = 0
            self.log_text.insert(tk.END, f"Found {self.total_urls} URLs to process.\n")
        except Exception as e:
            self.log_text.insert(tk.END, f"Error reading URL file: {e}\n")
            self.status_var.set("Error")
            return
        
        # Determine which script to run
        if self.screenshot_type.get() == "regular":
            script_name = os.path.join(script_dir, "website_screenshot.py")
        else:  # "full"
            script_name = os.path.join(script_dir, "website_screenshot_full.py")
        
        # Create and start thread
        self.process_thread = threading.Thread(
            target=self.run_process,
            args=(script_name, self.url_file_path.get()),
            daemon=True
        )
        self.process_thread.start()
    
    def run_process(self, script_name, url_file):
        try:
            # Set up virtual environment activation
            if os.name == 'nt':  # Windows
                activate_cmd = os.path.join(root_dir, "venv", "Scripts", "activate")
                cmd = f'"{sys.executable}" "{script_name}" "{url_file}"'
            else:  # Unix-like
                activate_cmd = os.path.join(root_dir, "venv", "bin", "activate")
                cmd = f'"{sys.executable}" "{script_name}" "{url_file}"'
            
            # Start process
            self.process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor output
            for line in iter(self.process.stdout.readline, ''):
                self.queue.put(line)
                
                # Update progress based on output
                if "Processing:" in line:
                    self.processed_urls += 1
                    progress = (self.processed_urls / self.total_urls) * 100
                    self.progress_var.set(progress)
                
                # Check if process was stopped
                if not hasattr(self, 'process'):
                    break
            
            # Process completed
            self.status_var.set("Completed")
            self.progress_var.set(100.0)
            self.queue.put("\nProcess completed.\n")
        
        except Exception as e:
            self.queue.put(f"Error: {e}\n")
            self.status_var.set("Error")
    
    def stop_process(self):
        if hasattr(self, 'process'):
            if os.name == 'nt':  # Windows
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])
            else:
                self.process.terminate()
            delattr(self, 'process')
            self.status_var.set("Stopped")
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
            # Schedule the next queue check
            self.root.after(self.update_interval, self.process_queue)

def main():
    root = tk.Tk()
    app = WebsiteScreenshotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()