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

### CSV to Excel Converter

* This project provides a simple Python script that converts a CSV file into an Excel file using the `pandas` library. This is part of a collection of mini code projects designed to demonstrate various Python functionalities.
* The provided code snippet reads data from a specified CSV file and writes it to an Excel file, making it easy to handle and share data in a widely-used format. 
* It converts ***CSV*** files to ***Excel*** format.
* It utilizes the `pandas` library for efficient data handling.
* It supports various data types typically found in CSV files.
* For better understanding read the ***readme.md*** given inside the folder.

### Image Resizer

* This project features a simple Python script that resizes images using the `PIL` (Pillow) library.
* It is part of a collection of mini code projects demonstrating various functionalities in Python.
* The provided code allows users to resize images to specified dimensions. This is useful for adjusting image sizes for different applications, such as web usage or personal projects.
* It resizes images to custom dimensions.
* It supports various image formats.
* For better understanding read the ***readme.md*** given inside the folder.

### Keep Screen Alive
* **Read** the ***Readme.md*** file inside. You just need to change the scripting rights in Powershell and then run the ***.bat*** file. It will keep pressing *scroll lock* and keep your PC awake even if the *power options* doesn't listen to you.

### Multiple File Rename

* **Read** the ***code comments*** and make ***changes*** which meets your requirements.
* The script uses ***os*** module which come by default in python now. If it is somehow not available then just do a **pip install** for it as well.
* The script is used to rename multiple files or folders inside a folder with a common name or a number appended to it.
* The script can also be used to remove a common name from all the files or folders inside a folder.

### Node Websocket For Realtime Tracking of File (Interview Question)

* The server has a ***log.txt file*** and when clients connect to the server they get the ***last 10 lines*** of the file.
* Whenever the file is updated, the updated line is also displayed to the connected clients in **realtime**.
* They gave two hours and open internet for the test but since I didn't use chatgpt to debug my code at the time, My server side code gave glitchy outputs.
* This is a working model which uses express and ws module of ***nodeJS***.
* Just do `npm init -y` and `npm install express ws` on the client and server folders seperately and run the clients and server using `node index.js`.
* They also asked to make the messages appear in a webpage. For this there is a ***index.html*** in the client folder which has html and the client JS code embedded inside it.

### Search and List Remaining Files

* I created this scripts to find the missing files from a site which I forgot to download due to lack of focus while scrolling.
* I created a list of files I have downloaded and a list of all the files there in the site after some pre-processing.
* Then it was a cake walk to check if the main list file's name was in the downloaded file's list.
* The files not present were printed as a list in the python console.

### Video Subtitle Generator (English)

* The required packages for the script are **openai-whisper** and **moviepy**. 
* The optional package for the script is **tqdm**, which is used to show the progress of the video processing. It can be disabled with keeping verbose false and commenting the tqdm import line and function call. ***Just install it if commentings parts of the code is not your thing***.
* Added an error handling code in case any of the video is not processed properly. The error is logged in a file named **SubtitleGenError.log** from where the script is called.
* I have added the **requirements.txt** file for the packages to be installed using pip. Just do a **pip install -r requirements.txt** to install all the required and optional packages.
* The **Video_Sub_Gen_Single.py** script is used to generate the subtitles for a single video in the current directory. Just add the video file in the current directory, add its name in the code's **filename** and run the script.
* The **Video_Sub_Gen_Multi.py** script is used to generate the subtitles for multiple videos in the current directory. Just add the video files in the current directory and run the script.
* The **Video_Sub_Gen_Tree.py** script is used to generate the subtitles for multiple videos in the current as well as the sub-directories. Just add the script in the root folder and run the script.
* The script can run on **CPU** as well as **GPU**. The ***GPU is recommended*** as it is ***faster***.
* The **Openai-Whisper** has 4 models (i.e, **base**, **small**, **medium** and **large**). The **base** and **small** models are of less size and produce results faster but you can always use the medium and large models for better results if you have large and faster GPU's.
* When you run the script for the first time it will download the required model from the openai server and store it in a folder named models.
* The ***base*** model has size ***138MB***, ***small*** model has size ***461MB***, ***medium*** model has size ***1.42GB*** and ***large*** model has size ***2.87GB***. The **base model** is already present in the **models** folder.
* In any case, I have added the **base** model in the **models** folder for you to use it directly without using gb's of your data for the bigger models.
* The **base** model is kept in parts *lesser than 25MB* so that it can be uploaded to github, you need to extract it using ***7zip*** or ***winrar*** to use it. Extract using the **extract here** option.
* The subtitle generation is done locally and the video is not uploaded to any server as per my understanding.
* **NOTE:** ***If you face any issues with the path of videos while running the tree script or the other two scripts then try moving the working folder closer to the root directory of the drive. It might solve the issue.***

### Simple Finance Tracker
* Read the Readme.md file inside the directory.
* The Simple Finance Tracker allows users to track daily expenses and incomes through an intuitive interface.
* It provides both a command-line interface (CLI) version and a graphical user interface (GUI) version.
* It can Add, edit, and delete expense/income records.
* One can View all expenses or incomes with a detailed breakdown.
* It generates summary reports (daily, weekly, monthly) and export them to an Excel file.
* Its data is stored in an SQLite database.

### Text TO Voice Converter
* This project allows users to convert text input into speech using the Web Speech API. 
* It provides an easy-to-use interface where users can type their text, select from a variety of voices available in the browser, and listen to the spoken output. 
* The project is built with HTML, CSS, and JavaScript, and leverages the browser's native speech synthesis capabilities. By utilizing the Web Speech API, it delivers real-time text-to-speech functionality without the need for external libraries. 
* This tool is useful for enhancing accessibility, especially for individuals with reading disabilities or those who prefer auditory content. Additionally, it demonstrates how native browser features can be harnessed to provide useful applications.
