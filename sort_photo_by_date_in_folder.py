import os
from PIL import Image
from datetime import datetime
import shutil

def copy_and_rename_os_safe(src_path, dest_path, new_name):
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
                new_name = f"{convert_to_seconds(time)}_{filename}"
                copy_success = copy_and_rename_os_safe(src_path, dest_dir, new_name)
                if not copy_success:
                    print(f"Failed to copy {src_path} to {dest_dir}/{new_name}")
        except (OSError, IOError) as e:
            print(f"Error processing {filename}: {e}")

def convert_to_seconds(date_time_str):
    try:
        datetime_obj = datetime.strptime(date_time_str, "%Y:%m:%d %H:%M:%S")
        epoch = datetime.utcfromtimestamp(0)
        return int((datetime_obj - epoch).total_seconds())
    except TypeError:
        print(f"Invalid date/time format: {date_time_str}")
        return None

if __name__ == "__main__":
    path = "...\\Pictures\\Gallery\\Camera"
    tpath = "...\\Pictures\\Gallery\\CompletePhotocolection"

    filter_images(path, tpath)
