from dateutil import parser

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

str_list = str_list.replace('0', "")
str_list = str_list.replace('/', "")
str_list = str_list.replace('BADGE', "")
str_list = str_list.replace('Completed on', "")
clean_list = [' '.join([word for word in line.split(" ") if not is_valid_date(word)]) for line in str_list]
clean_list = ''.join(clean_list)

clean_list = [line for line in clean_list.split('\n') if line.strip()]

list_badges_clean = open("list_clean.txt", 'w+')

for line in clean_list:
    list_badges_clean.write(line + "\n")

list_badges.close()
list_badges_clean.close()