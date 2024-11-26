print("Test")

import os
from app.services.cloudinary_service import CloudinaryService

cloudinary_service = CloudinaryService()

# Define a pattern to match all image files (with any extension)
image_extensions = ['*.jpg', '*.jpeg', '*.png']
# image_patterns = [os.path.join('./events', ext) for ext in image_extensions]


# Read all folders and files in the specified directory
# def read_files_in_directory(directory):
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             print(os.path.join(root, file))
            
# read_files_in_directory('./seed/seeders/images/events')

# Directory containing event images
# image_root_dir = './seed/seeders/images/events'
# folder_list = os.listdir(image_root_dir)

# for folder in range(20):
#     folder_name = folder_list[folder % len(folder_list)]
#     print(folder_name)
    
import random


# Directory containing user images
image_root_dir = './seed/seeders/images/event_organizers'

# Read all image in user images directory
image_list = os.listdir(image_root_dir)

# Ensure there are images available to use
if not image_list:
    print("No images found in the specified directory.")

# Randomly select an image from the list
image_name = random.choice(image_list)

print(image_name)
    