from PIL import Image
import sys

def remove_bg_color(input_path, output_path, background_color):
    img = Image.open(input_path).convert("RGBA")
    image_data = img.getdata()

    new_image_data = []
    for color in image_data:
        if color[0:3] == background_color:
            new_image_data.append((0, 0, 0, 0))
        else:
            new_image_data.append(color)
    
    img.putdata(new_image_data)
    img.save(output_path)
    
    print(f"Saved the image with background removed to {output_path}")

args = sys.argv

if len(args) != 4:
    print("Usage: python script.py <path_to> <path_output_to> <(x, x, x) #color to remove>")
    sys.exit(1) 

input_image = args[1]
output_image = args[2]
background_color = args[3]

remove_bg_color(input_image, output_image, background_color)