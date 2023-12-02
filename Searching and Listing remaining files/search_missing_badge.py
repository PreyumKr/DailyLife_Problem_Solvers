import os

root = os.getcwd()

list_downloaded_badges = []

for file in os.listdir('.'):
   if not os.path.isfile(file):
    continue

   head, tail = os.path.splitext(file)
   
   # Specify the extension of files you trying to edit at once
   if tail == ".pdf":
     list_downloaded_badges.append(head)

list_all_badges = open("list_clean.txt", 'r')

remaining_badges = []
str_list_all_badges = ''

for line in list_all_badges:
    str_list_all_badges += line

str_list_all_badges = str_list_all_badges.split('\n')
# print(str_list_all_badges)

for line in str_list_all_badges:
  if line not in list_downloaded_badges:
    remaining_badges.append(line)

print(remaining_badges)

list_all_badges.close()