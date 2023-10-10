import os
# import shutil


# getting the current directory you are in
root = os.getcwd()

# checking all the files inside the directory
for file in os.listdir('.'):
   
   # if no files in directory just skip
   if not os.path.isfile(file):
       continue
   
   # spliting the name and extension of the files
   head, tail = os.path.splitext(file)
   
   # when no extension is found it will add it
   if not tail:
       src = os.path.join(root, file)

       # you may choose your required extension instead of .jpg
       dst = os.path.join(root, file + '.jpg')
       
       # rewriting the files back in the directory and
       # check if the file doesn't already exist
       if not os.path.exists(dst): 
           
           # the rename function will rename the file without extension so
           # incase you need those files without extension use the shutil command
           # and comment the rename command
           os.rename(src, dst)

        #    shutil.copyfile(src, dst)