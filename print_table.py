def sum_title(array):
    sumof = 0
    for item in array:
        sumof += item
    return sumof

def print_interview_table(table):
    title_list=['ID OF INTVIEW','MENTOR NAME','APPLICANT NAME','DATE OF THE INTERVIEW','SCHOOL LOCATION','SECOND MENTOR']
    title_list_len = []
    for item in range(len(title_list)):
        title_list_len.append(len(title_list[item]))
    print('/' + '-' * (sum_title(title_list_len) + len(title_list) * 7 - 2) + '\\')
    for title in range(len(title_list)):
        print('|' + title_list[title].center(title_list_len[title] + 5) + "|", end="")
    print('\n', end="")
    print('-' * (sum_title(title_list_len) + len(title_list) * 7))
    for interview in table:
        print('|' + str(interview.id).center(title_list_len[0] + 5) + "|", end="")
        print('|' + interview.slot.assigned_mentor.first_name.center(title_list_len[1] + 5) + "|", end="")
        print('|' + interview.applicant.first_name.center(title_list_len[2] + 5) + "|", end="")
        print('|' + str(interview.slot.start).center(title_list_len[3] + 5) + "|", end="")
        print('|' + interview.applicant.school.name.center(title_list_len[4] + 5) + "|", end="")
        if interview.slot_mentor2 is not None:
            print('|' + interview.slot_mentor2.assigned_mentor.first_name.center(title_list_len[5] + 5) + "|", end="")
        else:
            print('|' + "".center(title_list_len[5] + 5) + "|", end="")
        print('\n', end="")
        if interview !=table[-1]:
            print('-' * (sum_title(title_list_len) + len(title_list) * 7))
    print('\\' + '-' * (sum_title(title_list_len) + len(title_list) * 7 - 2) + '/')

def print_applicant_table(table):
    title_list = ['ID','FIRST NAME', 'LAST NAME', '  EMAIL ADDRESS  ', '   CITY   ', 'APPLICATION DATE', 'STATUS',' SCHOOL ']
    title_list_len = []
    for item in range(len(title_list)):
        title_list_len.append(len(title_list[item]))
    print('/' + '-' * (sum_title(title_list_len) + len(title_list) * 7 - 2) + '\\')
    for title in range(len(title_list)):
        print('|' + title_list[title].center(title_list_len[title] + 5) + "|", end="")
    print('\n', end="")
    print('-' * (sum_title(title_list_len) + len(title_list) * 7))
    for applicant in table:
        print('|' + str(applicant.id).center(title_list_len[0] + 5) + "|", end="")
        print('|' + applicant.first_name.center(title_list_len[1] + 5) + "|", end="")
        print('|' + applicant.last_name.center(title_list_len[2] + 5) + "|", end="")
        print('|' + applicant.email.center(title_list_len[3] + 5) + "|", end="")
        print('|' + applicant.city.center(title_list_len[4] + 5) + "|", end="")
        print('|' + "{}-{}-{}".format(applicant.application_date.year,applicant.application_date.month, applicant.application_date.day).center(title_list_len[5] + 5) + "|", end="")
        print('|' + str(applicant.status).center(title_list_len[6] + 5) + "|", end="")
        if applicant.school is not None:
            print('|' + applicant.school.name.center(title_list_len[7] + 5) + "|", end="")
        else:
            print('|' + "".center(title_list_len[7] + 5) + "|", end="")
        print()
    print('\\' + '-' * (sum_title(title_list_len) + len(title_list) * 7 - 2) + '/')