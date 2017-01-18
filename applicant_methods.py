import random
import string

from models import *
import build
import example_data


def generate_random():
    existing_ids = get_all_applicant_id()
    generated = ''
    generated += random.choice(string.ascii_lowercase)
    generated += random.choice(string.ascii_lowercase)
    generated += random.choice(string.digits)
    generated += random.choice(string.ascii_uppercase)
    generated += random.choice(string.digits)
    if generated in existing_ids:
        generate_random()
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


# MAIN FUNCTION ##### checks, generates and assignes new applicant_ids


def assign_id():
    applicant_id = get_applicants_without_id()
    # print(len(applicant_id))
    for i in range(len(applicant_id)):
        new_id = generate_random()
        query = Applicant.update(applicant_id=new_id).where(Applicant.id == applicant_id[i])
        query.execute()
    print("done")


def assign_school():
    query = Applicant.\
        select(Applicant.id.alias('applicant_id'), School.id.alias('school_id')).\
        join(City, on=City.city_name == Applicant.city).join(School).naive()
    for item in query:
        # print(item.applicant_id,item.school_id)
        Applicant.update(school=item.school_id).where((Applicant.id == item.applicant_id) & (Applicant.school.is_null(True))).execute()

assign_id()
assign_school()
