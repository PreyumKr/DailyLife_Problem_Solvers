from dateutil import parser

# validator function to identify multiple formats of dates 
# It can go wrong and ommit few numbers which are not actually date aas well and 
# Also leave numbers like 0 or / in some cases
def is_valid_date(date_str):
    try:
        parser.parse(date_str)
        return True
    except:
        return False


list_badges = open("list.txt", 'r')
str_list = ''
for line in list_badges:
    str_list += line

# My list were containing below mentioned garbage value which I cleaned using replace
str_list = str_list.replace('0', "")
str_list = str_list.replace('/', "")
str_list = str_list.replace('BADGE', "")
str_list = str_list.replace('Completed on', "")

# Both lines created a clean list of file names which i needed
clean_list = [' '.join([word for word in line.split(" ") if not is_valid_date(word)]) for line in str_list]
clean_list = ''.join(clean_list)

# To remove unnecessary new lines
clean_list = [line for line in clean_list.split('\n') if line.strip()]

list_badges_clean = open("list_clean.txt", 'w+')

# To create a file that can show the list items in new lines 
for line in clean_list:
    list_badges_clean.write(line + "\n")

list_badges.close()
list_badges_clean.close()