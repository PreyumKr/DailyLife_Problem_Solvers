import os
import sys
import ctypes
from PIL import Image

def get_screen_resolution():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def resize_image(image_path, output_path, size):
    with Image.open(image_path) as img:
        img = img.resize(size, Image.LANCZOS)
        img.save(output_path)

args = sys.argv
path = args[1]

# Get screen resolution
screen_width, screen_height = get_screen_resolution()

# Resize the image
pwd = os.getcwd()
resized_image_path = "resized_wallpaper.jpg"
resize_image(path, resized_image_path, (screen_width, screen_height))

resized_image_path = os.path.join(pwd, resized_image_path)

# Set the resized image as wallpaper
ctypes.windll.user32.SystemParametersInfoW(20, 0, resized_image_path, 0)

# ctypes.windll.user32.SystemParametersInfoA(20, 0, resized_image_path, 0)