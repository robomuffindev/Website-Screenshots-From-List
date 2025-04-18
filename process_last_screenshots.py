import os
import glob
import sys
import time
from PIL import Image
import re

def find_latest_directory(base_dir):
    """Find the most recent timestamped directory."""
    if not os.path.exists(base_dir):
        print(f"Base directory {base_dir} does not exist.")
        return None
    
    dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    if not dirs:
        print(f"No subdirectories found in {base_dir}")
        return None
    
    # Filter directories that match the timestamp pattern YYYY-MM-DD_HH-MM-SS
    pattern = re.compile(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}')
    timestamp_dirs = [d for d in dirs if pattern.match(d)]
    
    if not timestamp_dirs:
        print(f"No timestamped directories found in {base_dir}")
        return None
    
    # Sort by name (which effectively sorts by timestamp)
    timestamp_dirs.sort(reverse=True)
    latest_dir = os.path.join(base_dir, timestamp_dirs[0])
    return latest_dir

def process_images(folder_path, resize=True, resize_width=800, save_webp=True):
    """Process images in the specified folder."""
    print(f"Processing images in folder: {folder_path}")
    print(f"- Resize: {resize} (width={resize_width})")
    print(f"- WebP conversion: {save_webp}")
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist.")
        return
    
    # Get all PNG images in the folder
    png_files = glob.glob(os.path.join(folder_path, "*.png"))
    print(f"Found {len(png_files)} PNG images in the folder.")
    
    if len(png_files) == 0:
        print("No images to process.")
        return
    
    # Process for resizing
    if resize:
        # Create resized directory
        resized_dir = os.path.join(folder_path, "resized")
        os.makedirs(resized_dir, exist_ok=True)
        print(f"Created/verified resized directory: {resized_dir}")
        
        # Process each image for resizing
        for img_path in png_files:
            img_filename = os.path.basename(img_path)
            resized_path = os.path.join(resized_dir, img_filename)
            
            try:
                # Open and resize the image
                img = Image.open(img_path)
                print(f"Opened image: {img_filename} ({img.size[0]}x{img.size[1]})")
                
                # Calculate new height to maintain aspect ratio
                width_percent = (resize_width / float(img.size[0]))
                target_height = int((float(img.size[1]) * float(width_percent)))
                
                # Resize with LANCZOS resampling for quality
                resized_img = img.resize((resize_width, target_height), Image.LANCZOS)
                resized_img.save(resized_path)
                
                print(f"Resized: {img_filename} to {resize_width}x{target_height} -> {resized_path}")
                img.close()
            except Exception as e:
                print(f"Error resizing {img_filename}: {e}")
    
    # Process for WebP conversion
    if save_webp:
        # Create WebP directory
        webp_dir = os.path.join(folder_path, "webp")
        os.makedirs(webp_dir, exist_ok=True)
        print(f"Created/verified WebP directory: {webp_dir}")
        
        # Determine source files (original or resized)
        source_files = []
        if resize:
            source_dir = os.path.join(folder_path, "resized")
            source_files = glob.glob(os.path.join(source_dir, "*.png"))
            print(f"Using {len(source_files)} resized images as source for WebP conversion")
        else:
            source_files = png_files
            print(f"Using {len(source_files)} original images as source for WebP conversion")
        
        # Convert each image to WebP
        for img_path in source_files:
            img_filename = os.path.basename(img_path)
            webp_filename = os.path.splitext(img_filename)[0] + ".webp"
            webp_path = os.path.join(webp_dir, webp_filename)
            
            try:
                # Open and convert the image
                img = Image.open(img_path)
                print(f"Converting to WebP: {img_filename}")
                
                # If resize is not already applied but is requested
                if not resize and resize_width > 0:
                    # Calculate new height to maintain aspect ratio
                    width_percent = (resize_width / float(img.size[0]))
                    target_height = int((float(img.size[1]) * float(width_percent)))
                    
                    # Resize with LANCZOS resampling for quality
                    img = img.resize((resize_width, target_height), Image.LANCZOS)
                    print(f"Resized during WebP conversion to {resize_width}x{target_height}")
                
                # Save as WebP with good quality
                img.save(webp_path, format="WEBP", quality=90)
                print(f"Saved WebP: {webp_path}")
                img.close()
            except Exception as e:
                print(f"Error converting {img_filename} to WebP: {e}")
    
    print("Image processing completed.")

def main():
    # First check if specific directory was provided
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        # Find the latest directory in screenshots or screenshots_full
        print("Looking for the most recent screenshot directory...")
        latest_regular = find_latest_directory("screenshots")
        latest_full = find_latest_directory("screenshots_full")
        
        if latest_regular and latest_full:
            # Compare timestamps to find the most recent one
            if os.path.getmtime(latest_regular) > os.path.getmtime(latest_full):
                folder_path = latest_regular
                print(f"Using most recent regular screenshots directory: {folder_path}")
            else:
                folder_path = latest_full
                print(f"Using most recent full-page screenshots directory: {folder_path}")
        elif latest_regular:
            folder_path = latest_regular
            print(f"Using most recent regular screenshots directory: {folder_path}")
        elif latest_full:
            folder_path = latest_full
            print(f"Using most recent full-page screenshots directory: {folder_path}")
        else:
            print("No screenshot directories found. Please specify directory as argument.")
            return
    
    # Get resize width if provided
    resize_width = 800  # Default
    if len(sys.argv) >= 3:
        try:
            resize_width = int(sys.argv[2])
        except ValueError:
            print(f"Invalid resize width: {sys.argv[2]}. Using default (800px).")
    
    # Ask user for options
    resize = input("Resize images? (Y/N, default=Y): ").strip().upper() != "N"
    
    if resize:
        width_input = input(f"Resize width (default={resize_width}): ").strip()
        if width_input:
            try:
                resize_width = int(width_input)
            except ValueError:
                print(f"Invalid width. Using {resize_width}px.")
    
    save_webp = input("Convert to WebP? (Y/N, default=Y): ").strip().upper() != "N"
    
    # Process images
    print("\nStarting image processing...")
    process_images(folder_path, resize=resize, resize_width=resize_width, save_webp=save_webp)

if __name__ == "__main__":
    main()
