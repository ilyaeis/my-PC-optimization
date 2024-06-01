import os
from PIL import Image
from datetime import datetime
import shutil

def copy_and_rename_os_safe(src_path, dest_path, new_name):
    """
    Copies a file from source to destination with a new name, handling potential permission issues gracefully.

    Args:
        src_path (str): Path to the source file.
        dest_path (str): Path to the destination directory.
        new_name (str): The new name for the copied file.

    Returns:
        bool: True if the copy operation was successful, False otherwise.
    """

    try:
        # Attempt to copy the file using os.copyfile
        shutil.copy(src_path, f"{dest_path}\\{new_name}")
        return True
    except PermissionError:
        print(f"Permission error while copying {src_path}. Trying with shutil.copy2...")
        try:
            # Fall back to shutil.copy2 for potentially better permission handling
            shutil.copy2(src_path, f"{dest_path}\\{new_name}")
            return True
        except Exception as e:  # Catch any other exceptions
            print(f"Failed to copy {src_path}: {e}")
            return False

def get_exif_key(img, key):
  exif_data = img._getexif()  # Get the EXIF data dictionary
  if exif_data:               # Check if the key is present
    return exif_data[key]  
  
def filter_images(source_dir, dest_dir):
    """
    Filters and copies images from source to destination directory based on EXIF data.

    Args:
        source_dir (str): Path to the source directory.
        dest_dir (str): Path to the destination directory.
    """

    for filename in os.listdir(source_dir):
        if not filename.lower().endswith(('.jpg', '.png')):
            continue

        src_path = os.path.join(source_dir, filename)
        if not os.path.isfile(src_path):  # Skip directories
            continue

        try:
            img = Image.open(src_path)
            key_to_check = 36867  # Example EXIF key (represents DateTimeOriginal)
            time = get_exif_key(img, key_to_check)

            if time:
                new_name = f"{convert_to_miseconds(time)}_{filename}"
                copy_success = copy_and_rename_os_safe(src_path, dest_dir, new_name)
                if not copy_success:
                    print(f"Failed to copy {src_path} to {dest_dir}/{new_name}")
        except (OSError, IOError) as e:
            print(f"Error processing {filename}: {e}")

def convert_to_miseconds(date_time_str):
    """
    Converts a date/time string (expected format) to milliseconds since epoch.

    Args:
        date_time_str (str): The date/time string to convert.

    Returns:
        int: The time in milliseconds since epoch, or None if parsing fails.
    """

    try:
        datetime_obj = datetime.strptime(date_time_str, "%Y:%m:%d %H:%M:%S")
        epoch = datetime.utcfromtimestamp(0)
        return int((datetime_obj - epoch).total_seconds() * 1000)
    except TypeError:
        print(f"Invalid date/time format: {date_time_str}")
        return None

if __name__ == "__main__":
    path = "C:\\Users\\Lenovo\\Pictures\\Gallery\\Camera"
    tpath = "C:\\Users\\Lenovo\\Pictures\\Gallery\\test"

    filter_images(path, tpath)
