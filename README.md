# DailyLife_Problem_Solvers
Python Scripts for solving daily life problems in windows (recommended)

# Instructions

### Add Extension to Files with No Extension

* **Read** the ***code comments*** and make ***changes*** which meets your requirements.
* You can choose between ***copy*** and ***rename*** function according to what you want to happen to your original file with no extension.

### Clean Files from Sub-Directories of a Folder

* **Read** the ***code comments*** and make ***changes*** which meets your requirements.
* The scripts uses ***os*** and ***shutil*** module which come by default in python now. If they are somehow not available then just do a **pip install** for them as well.
* The scripts are used to clean all the sub-directories inside a folder either by removing everything or by removing only the files in the sub-directories or by removing the files in the entire sub-tree of the folder.
* The **Clean_Subdirectories_Complete.py** script is used to remove everything inside the sub-directories.
* The **Clean_Subdirectories_Files.py** script is used to remove only the files inside the sub-directories.
* The **Clean_SubTree_Files.py** script is used to remove the files in the entire sub-tree of the folder.

### Colouring Book Sceapeops

* **Read** the ***readme.txt*** given inside the folder and try it out ! ***:-)***

### Convert Markdown to PDF Offline in Bulk

* **Pre-requisite** Device must have NPM (node) and **Installed** ***md-to-pdf***
* To install ***md-to-pdf*** using NPM use **npm i md-to-pdf**.
* The script is used to do multiple conversions using one click. For a single conversion you can always use console directly to do the task using ***"md-to-pdf <Filename>"***
* The script also uses modules named ***glob*** and ***subprocess*** which come by default in python now. If they are not available then just do a **pip install** for them as well.
* The script also adds mathjax support to the markdown file to help you convert your math equations written in latex inside the markdown file to be converted perfecty during the pdf conversion.

### Create Fake BigData

* **Read** the ***code comments*** and make ***changes*** which meets your requirements.
* The No Limit code runs all parellel csv generators together which can use the entire CPU.
* If You want to make a Single csv use the single csv. (PS: It uses single process so its going to take forever!)

### Multiple File Rename

* **Read** the ***code comments*** and make ***changes*** which meets your requirements.
* The script uses ***os*** module which come by default in python now. If it is somehow not available then just do a **pip install** for it as well.
* The script is used to rename multiple files or folders inside a folder with a common name or a number appended to it.
* The script can also be used to remove a common name from all the files or folders inside a folder.

### Search and List Remaining Files

* I created this scripts to find the missing files from a site which I forgot to download due to lack of focus while scrolling.
* I created a list of files I have downloaded and a list of all the files there in the site after some pre-processing.
* Then it was a cake walk to check if the main list file's name was in the downloaded file's list.
* The files not present were printed as a list in the python console.