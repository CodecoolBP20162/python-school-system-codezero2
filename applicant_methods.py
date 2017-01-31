import random
import string

from models import *
import build


class applicant_methods:
    @classmethod
    def generate_random(cls):
        existing_ids = cls.get_all_applicant_id()
        generated = ''
        generated += random.choice(string.ascii_lowercase)
        generated += random.choice(string.ascii_lowercase)
        generated += random.choice(string.digits)
        generated += random.choice(string.ascii_uppercase)
        generated += random.choice(string.digits)
        if generated in existing_ids:
            cls.generate_random()
        return generated

    def get_all_applicant_id():
        id_list = []
        all_id = Applicant.select().where(Applicant.applicant_id.is_null(False))
        for item in all_id:
            id_list.append(item.applicant_id)
        return id_list

    def get_applicants_without_id():
        id_list = []
        without_id = Applicant.select().where(Applicant.applicant_id.is_null(True))
        for item in without_id:
            id_list.append(item.id)
        return id_list

    def show_applicants_without_id():
        applicant_list = get_applicants_without_id()
        for item in applicant_list:
            print(item)

    def show_applicants_with_id():
        applicant_list = []
        all_id = Applicant.select().where(Applicant.applicant_id.is_null(False))
        for item in all_id:
            applicant_list.append((item.applicant_id, item.first_name, item.last_name, item.city))
        for item in applicant_list:
            print(item)

    # MAIN FUNCTION ##### checks, generates and assignes new applicant_ids

    @classmethod
    def assign_id(cls):
        applicant_id = cls.get_applicants_without_id()
        # print(len(applicant_id))
        for i in range(len(applicant_id)):
            new_id = cls.generate_random()
            query = Applicant.update(applicant_id=new_id).where(Applicant.id == applicant_id[i])
            query.execute()
        print("done")

    def assign_school():
        query = Applicant. \
            select(Applicant.id.alias('applicant_id'), School.id.alias('school_id')) \
            .join(City, on=City.city_name == Applicant.city) \
            .join(School) \
            .naive()
        for item in query:
            # print(item.applicant_id,item.school_id)
            Applicant.update(school=item.school_id) \
                .where((Applicant.id == item.applicant_id) | (Applicant.school.is_null(True))) \
                .execute()


    def display_all_data():
        '''
        applicants = Applicant.select(Applicant.applicant_id, Applicant.name, Applicant.application_date, Applicant.city,
                                      Applicant.status, Applicant.school, School.name.alias("school_name"))\
            .join(School, join_type=JOIN.LEFT_OUTER)\
            .naive()

        for person in applicants:
            print("\nAPPLICANT ID: {}\nNAME: {}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
                  .format(person.applicant_id,
                          person.name,
                          person.application_date.year,
                          person.application_date.month,
                          person.application_date.day,
                          person.city,
                          person.status,
                          person.school_name))
        '''

        applicants = Applicant.select()

        for person in applicants:
            school_name = "None"
            if person.school is not None:
                school_name = person.school.name
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: {}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
                  .format(person.applicant_id,
                          person.first_name,
                          person.last_name,
                          person.email,
                          person.application_date.year,
                          person.application_date.month,
                          person.application_date.day,
                          person.city,
                          person.status,
                          school_name))

    def filter_by_status(string):
        applicants = Applicant.select().where(Applicant.status == string).naive()

        for person in applicants:
            school_name = "None"
            if person.school is not None:
                school_name = person.school.name
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: {}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
                  .format(person.applicant_id,
                          person.first_name,
                          person.last_name,
                          person.email,
                          person.application_date.year,
                          person.application_date.month,
                          person.application_date.day,
                          person.city,
                          person.status,
                          person.school_name))

    def filter_by_location(string):
        applicants = Applicant.select().where(Applicant.city == string)

        for person in applicants:
            school_name = "None"
            if person.school is not None:
                school_name = person.school.name
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: {}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
                  .format(person.applicant_id,
                          person.first_name,
                          person.last_name,
                          person.email,
                          person.application_date.year,
                          person.application_date.month,
                          person.application_date.day,
                          person.city,
                          person.status,
                          person.school_name))

    def filter_by_school(string):
        # applicants = Applicant.select().where(Applicant.school.name == string)

        applicants = Applicant.select(Applicant.applicant_id, Applicant.first_name, Applicant.last_name, Applicant.city,
                                      Applicant.status, Applicant.school, School.name.alias("school_name")). \
            join(School).where(School.name == string).naive()

        for person in applicants:
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: {}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
                  .format(person.applicant_id,
                          person.first_name,
                          person.last_name,
                          person.email,
                          person.application_date.year,
                          person.application_date.month,
                          person.application_date.day,
                          person.city,
                          person.status,
                          person.school_name))

    def filter_by_name(string1, string2):
        applicants = Applicant.select().where(Applicant.first_name == string1, Applicant.last_name == string2)

        for person in applicants:
            school_name = "None"
            if person.school is not None:
                school_name = person.school.name
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: {}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
                  .format(person.applicant_id,
                          person.first_name,
                          person.last_name,
                          person.email,
                          person.application_date.year,
                          person.application_date.month,
                          person.application_date.day,
                          person.city,
                          person.status,
                          person.school_name))

    def filter_by_time(string):
        applicants = Applicant.select().where(Applicant.application_date == string)

        try:
            for person in applicants:
                school_name = "None"
                if person.school is not None:
                    school_name = person.school.name
                print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: {}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
                      .format(person.applicant_id,
                          person.first_name,
                          person.last_name,
                          person.email,
                          person.application_date.year,
                          person.application_date.month,
                          person.application_date.day,
                          person.city,
                          person.status,
                          person.school_name))
        except DataError:
            print("Invalid format")

    def filter_by_mentor(string):
        applicants = Applicant.select(Applicant.applicant_id, Applicant.first_name, Applicant.last_name, Applicant.city,
                                      Applicant.status, Applicant.school, Mentor.school). \
            join(Mentor, on=(Applicant.school == Mentor.school),
                 join_type=JOIN.FULL).where(Mentor.name == string).naive()

        for person in applicants:
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: {}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
                  .format(person.applicant_id,
                          person.first_name,
                          person.last_name,
                          person.email,
                          person.application_date.year,
                          person.application_date.month,
                          person.application_date.day,
                          person.city,
                          person.status,
                          person.school_name))

    """ APPLICANT MENU VIEW - FUNCTIONS """

    def check_status():
        code = input("Please enter your application ID: ")
        applicants = Applicant.select().where(Applicant.applicant_id == code)

        for person in applicants:
            school_name = "None"
            if person.school is not None:
                school_name = person.school.name
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nSTATUS: {}\nSCHOOL:{}\n"
                  .format(person.applicant_id,
                          person.first_name,
                          person.last_name,
                          person.status,
                          person.school_name))

    def check_personal_data():
        code = input("Please enter your application ID: ")
        applicants = Applicant.select().where(Applicant.applicant_id == code)

        for person in applicants:
            school_name = "None"
            if person.school is not None:
                school_name = person.school.name
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: {}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
                  .format(person.applicant_id,
                          person.first_name,
                          person.last_name,
                          person.email,
                          person.application_date.year,
                          person.application_date.month,
                          person.application_date.day,
                          person.city,
                          person.status,
                          person.school_name))
