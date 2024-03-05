import os
import glob

# Path to the directory
path = '.'

# List of the subdirectories inside the current directory
list = os.listdir(path)

# Loop to remove the files inside the subdirectories
for element in list:
    files = glob.glob(path + '/' + element + '/*')
    for file in files:
        if os.path.isfile(file):
            os.remove(file)

print('The Sub-Directories have been cleaned of Files!!!')