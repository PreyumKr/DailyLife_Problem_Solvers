import os

root = os.getcwd()

for file in os.listdir('.'):

  if not os.path.isdir(file):
    continue

  src = os.path.join(root, file)
  dst = os.path.join(root, file.replace("_Trailingtext", ""))
  
  if not os.path.exists(dst): # check if the folder doesn't exist
    os.rename(src, dst)  