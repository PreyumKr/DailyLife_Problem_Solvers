import os

root = os.getcwd()

for file in os.listdir('.'):
   if not os.path.isfile(file):
    continue

   head, tail = os.path.splitext(file)
   
   # Specify the extension of files you trying to edit at once
   if tail == ".jpg":
    src = os.path.join(root, file)
    dst = os.path.join(root, head, "_TailingText" , tail)
    
    if not os.path.exists(dst): # check if the file doesn't exist
      os.rename(src, dst)