import random
import string

from interview_methods import * ##
from pushover import * ##

try:
    from pushover import *
except Exception:
    from .pushover import *
try:
    from interview_methods import *
except Exception:
    from .interview_methods import *

try:
    from .models import *
except Exception:
    from models import *


class ApplicantMethods:

    @staticmethod
    def generate_random():
        existing_ids = ApplicantMethods.get_all_applicant_id()
        generated = ''
        generated += random.choice(string.ascii_lowercase)
        generated += random.choice(string.ascii_lowercase)
        generated += random.choice(string.digits)
        generated += random.choice(string.ascii_uppercase)
        generated += random.choice(string.digits)
        if generated in existing_ids:
            ApplicantMethods.generate_random()
        return generated

    @classmethod
    def get_all_applicant_id(cls):
        id_list = []
        all_id = Applicant.select().where(Applicant.applicant_id.is_null(False))
        for item in all_id:
            id_list.append(item.applicant_id)
        return id_list

    @classmethod
    def get_applicants_without_id(cls):
        id_list = []
        without_id = Applicant.select().where(Applicant.applicant_id.is_null(True))
        for item in without_id:
            id_list.append(item.id)
        return id_list

    # MAIN FUNCTION ##### checks, generates and assignes new applicant_ids
    @classmethod
    def assign_id_to_applicant(cls, applicant):
        new_id = cls.generate_random()
        applicant.applicant_id = new_id
        applicant.save()
        return new_id

    @classmethod
    def assign_school_to_applicant(cls, applicant):
        city = City.get(City.city_name == applicant.city)
        applicant.school = city.location
        applicant.save()

    @classmethod
    def get_list(cls):
        table = Applicant.select()
        lista = [("APPLICANT ID", "NAME", "CITY", "STATUS")]
        for item in table:
            if len(item.interview)==0:
                lista.append(
                    (item.applicant_id, item.first_name, item.last_name, item.email, item.city, item.status,
                     item.school.name,'False'))
            else:
                lista.append(
                    (item.applicant_id, item.first_name, item.last_name, item.email, item.city, item.status,
                     item.school.name, 'True'))
        return lista

    @staticmethod
    def filter_redirect(choice, query):
        if choice == "last_name":
            return "filter_by_last_name"
        elif choice == "first_name":
            return "filter_by_first_name"
        elif choice == "school":
            return "filter_by_school"
        elif choice == "status":
            return "filter_by_status"

    @staticmethod
    def create_new_user(form):
        user = User.create_user(login=form.login.data, password=form.password.data)
        applicant = Applicant.create(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                                     city=str(form.city.data).lower(), user=user.id)

        new_applicant_id = ApplicantMethods.assign_id_to_applicant(applicant)
        ApplicantMethods.assign_school_to_applicant(applicant)
        interview_methods.assign_interview(applicant)

        msg = "{} {} just registered as an applicant! - codezero".format(applicant.first_name, applicant.last_name)
        pushover.send_pushover(msg)
        return new_applicant_id


    @staticmethod
    def user_list():
        array = []
        array.append(('Username', 'Password', 'Applicant name'))
        for item in User.select():
            if len(item.applicant) != 0:
                array.append((item.login, item.password, item.applicant[0].first_name))
            else:
                array.append((item.login, item.password))

        return array


