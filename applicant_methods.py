import string
from send_emails import *
from interview_methods import *
from print_table import *
import psycopg2
import peewee


class applicant_methods:
    @classmethod
    def generate_random_code(cls):
        existing_ids = cls.get_all_applicant_id()
        generated = ''
        generated += random.choice(string.ascii_lowercase)
        generated += random.choice(string.ascii_lowercase)
        generated += random.choice(string.digits)
        generated += random.choice(string.ascii_uppercase)
        generated += random.choice(string.digits)
        if generated in existing_ids:
            cls.generate_random_code()
        return generated

    @staticmethod
    def get_all_applicant_id():
        id_list = []
        all_id = Applicant.select().where(Applicant.applicant_id.is_null(False))
        for item in all_id:
            id_list.append(item.applicant_id)
        return id_list

    @staticmethod
    def get_applicants_without_id():
        id_list = []
        without_id = Applicant.select().where(Applicant.applicant_id.is_null(True))
        for item in without_id:
            id_list.append(item.id)
        return id_list

    @staticmethod
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
            new_id = cls.generate_random_code()
            query = Applicant.update(applicant_id=new_id).where(Applicant.id == applicant_id[i])
            query.execute()
        print("done")

    # REG__1__
    @staticmethod
    def register_data_inputs():
        print("Please provide the following details!")
        first_name = input('FIRST NAME: ')
        last_name = input('LAST NAME: ')
        email = input('EMAIL: ')
        city_name = input('CITY: ')

        return first_name, last_name, email, city_name

    # REG__3__
    @staticmethod
    def assign_school_shorter(city_name):
        get_location_id = City.select().where(City.city_name == city_name.lower())
        return get_location_id[0].location_id

    # REG__4__
    @staticmethod
    def create_new_applicant(first_name, last_name, email, city_name, new_applicant_id, school_id):
        Applicant.create(
            applicant_id=new_applicant_id,
            first_name=first_name,
            last_name=last_name,
            email=email, status='new',
            city=city_name,
            school=school_id
        )

    # REG__5__
    @staticmethod
    def assign_interview(new_applicant_id):
        applicant = Applicant.select().join(Interview, join_type=JOIN_LEFT_OUTER).where(
            Applicant.applicant_id == new_applicant_id).get()
        slot = interview_methods.random_slot(applicant)
        if slot is None:
            print('There is no available interview slot for ', applicant.first_name, applicant.last_name)
            return False
        Interview.create(applicant=applicant.id, slot=slot.id)
        InterviewSlot.update(reserved=True).where(InterviewSlot.id == slot.id).execute()

    @staticmethod
    def assign_school():
        query = Applicant. \
            select(Applicant.id.alias('applicant_id'), School.id.alias('school_id')) \
            .join(City, on=City.city_name == Applicant.city) \
            .join(School) \
            .naive()
        for item in query:
            # print(item.applicant_id,item.school_id)
            Applicant.update(school=item.school_id) \
                .where((Applicant.id == item.applicant_id) & (Applicant.school.is_null(True))) \
                .execute()

    """ MAIN REGISTRATION PROCESS """

    @classmethod
    def register_applicant_process(cls):
        first_name, last_name, email, city_name = cls.register_data_inputs()
        new_applicant_id = cls.generate_random_code()
        try:
            school_id = cls.assign_school_shorter(city_name)
        except IndexError:
            print("City does not exist! try again.")
            return False
        cls.create_new_applicant(first_name, last_name, email, city_name, new_applicant_id, school_id)
        cls.assign_interview(new_applicant_id)

        # Send registration info to applicant:
        applicant_email, message = SendEmails.prepare_applicant_reg_info(new_applicant_id)
        SendEmails.send_email(applicant_email, message)

        # Send interview info to applicant:
        applicant_email, message = SendEmails.prepare_applicant_interview_info(new_applicant_id)
        SendEmails.send_email(applicant_email, message)

        # Send info to Mentor:
        mentor_email, message = SendEmails.prepare_mentor_interview_info(new_applicant_id)
        SendEmails.send_email(mentor_email, message)

    @staticmethod
    def assign_school_bulk():
        query = Applicant. \
            select(Applicant.id.alias('applicant_id'), School.id.alias('school_id')) \
            .join(City, on=City.city_name == Applicant.city) \
            .join(School) \
            .naive()
        for item in query:
            print(item.applicant_id)
            Applicant.update(school=item.school_id) \
                .where((Applicant.applicant_id == item.applicant_id) & (Applicant.school.is_null(True))) \
                .execute()


    @staticmethod
    def display_all_data():
        applicants = Applicant.select()
        print_applicant_table(applicants)

    @staticmethod
    def filter_by_status(string):
        applicants = Applicant.select().where(Applicant.status == string).naive()

        for person in applicants:
            school_name = "None"
            if person.school is not None:
                school_name = person.school.name
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: "
                  "{}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
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

    @staticmethod
    def filter_by_location(string):
        applicants = Applicant.select().where(Applicant.city == string)

        for person in applicants:
            school_name = "None"
            if person.school is not None:
                school_name = person.school.name
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: "
                  "{}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
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

    @staticmethod
    def filter_by_school(string):
        # applicants = Applicant.select().where(Applicant.school.name == string)

        applicants = Applicant.select(Applicant.applicant_id, Applicant.first_name, Applicant.last_name, Applicant.city,
                                      Applicant.status, Applicant.school, School.name.alias("school_name")). \
            join(School).where(School.name == string).naive()

        for person in applicants:
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: "
                  "{}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
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

    @staticmethod
    def filter_by_name(string1, string2):
        applicants = Applicant.select().where(Applicant.first_name == string1, Applicant.last_name == string2)

        for person in applicants:
            school_name = "None"
            if person.school is not None:
                school_name = person.school.name
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: "
                  "{}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
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

    @staticmethod
    def filter_by_time(string):
        applicants = Applicant.select().where(Applicant.application_date == string)

        try:
            for person in applicants:
                school_name = "None"
                if person.school is not None:
                    school_name = person.school.name
                print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: "
                      "{}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
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
        except (psycopg2.DataError, psycopg2.InternalError, peewee.DataError, peewee.InternalError):
            print("Invalid format")

    @staticmethod
    def filter_by_mentor(string):
        applicants = Applicant.select(Applicant.applicant_id, Applicant.first_name, Applicant.last_name, Applicant.city,
                                      Applicant.status, Applicant.school, Mentor.school). \
            join(Mentor, on=(Applicant.school == Mentor.school),
                 join_type=JOIN.FULL).where(Mentor.first_name == string).naive()

        for person in applicants:
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: "
                  "{}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
                  .format(person.applicant_id,
                          person.first_name,
                          person.last_name,
                          person.email,
                          person.application_date.year,
                          person.application_date.month,
                          person.application_date.day,
                          person.city,
                          person.status,
                          person.school.name))

    """ APPLICANT MENU VIEW - FUNCTIONS """

    @staticmethod
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
                          school_name))

    @staticmethod
    def check_personal_data():
        code = input("Please enter your application ID: ")
        applicants = Applicant.select().where(Applicant.applicant_id == code)

        for person in applicants:
            school_name = "None"
            if person.school is not None:
                school_name = person.school.name
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: "
                  "{}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
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

    @staticmethod
    def check_interview_details():
        code = input("Please enter your application ID: ")
        applicants = Applicant.select().where(Applicant.applicant_id == code)

        for person in applicants:
            print("\nAPPLICANT ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nSCHOOL: {}\nINTERVIEW: {}\nMENTOR: {} {}"
                  .format(person.applicant_id,
                          person.first_name,
                          person.last_name,
                          person.school.name,
                          person.interview[0].slot.start,
                          person.interview[0].slot.assigned_mentor.first_name,
                          person.interview[0].slot.assigned_mentor.last_name))
