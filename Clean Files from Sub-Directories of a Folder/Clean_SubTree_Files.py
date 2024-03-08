import os
import glob
import shutil

# Path to the directory
path = '.'

# List of the subdirectories inside the current directory
subdirectories = os.listdir(path)

# Walk through the sub-directories and remove the files
for subdirectory in subdirectories:
    for root, dirs, files in os.walk(subdirectory):
        for file in files:
            os.remove(os.path.join(root, file))

print('The Sub-Tree have been cleansed of Files!!!')