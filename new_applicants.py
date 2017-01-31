# New applicants arrive into your project database by this script.
# You can run it anytime to generate new data!

from models import *
import random
from applicant_methods import *


class new_applicants:


    @classmethod
    def generate_applicant(cls):
        print("Please provide the following details!")
        first_name = input('FIRST NAME: ')
        last_name = input('LAST NAME: ')
        email = input('EMAIL: ')
        city = input('CITY: ')
        school = applicant_methods.assign_school()
        id = applicant_methods.generate_random()


        #random_city = random.choice(cls.cities)
        #cls.names.remove(random_name)

        Applicant.create(applicant_id=id, first_name =first_name, last_name=last_name, email=email, status='new', city=city, school = school)
        print("\nNew applicant --{} {}-- created\n".format(first_name,last_name))


