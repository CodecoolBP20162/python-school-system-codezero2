def sum_title(array):
    sumof = 0
    for item in array:
        sumof += item
    return sumof

def print_interview_table(table):
    title_list=['MENTOR NAME','APPLICANT NAME','DATE OF THE INTERVIEW','SCHOOL LOCATION']
    title_list_len = []
    for item in range(len(title_list)):
        title_list_len.append(len(title_list[item]))
    print('/' + '-' * (sum_title(title_list_len) + len(title_list) * 7 - 2) + '\\')
    for title in range(len(title_list)):
        print('|' + title_list[title].center(title_list_len[title] + 5) + "|", end="")
    print('\n', end="")
    print('-' * (sum_title(title_list_len) + len(title_list) * 7))
    for line in table:
        print('|' + line.name.center(title_list_len[0] + 5) + "|", end="")
        print('|' + line.app_name.center(title_list_len[1] + 5) + "|", end="")
        print('|' + str(line.start).center(title_list_len[2] + 5) + "|", end="")
        print('|' + line.school.name.center(title_list_len[3] + 5) + "|", end="")
        print('\n', end="")
        if line !=table[-1]:
            print('-' * (sum_title(title_list_len) + len(title_list) * 7))
    print('\\' + '-' * (sum_title(title_list_len) + len(title_list) * 7 - 2) + '/')