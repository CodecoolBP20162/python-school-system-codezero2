from models import *
import example_data
import random


def random_slot(applicant):
    if applicant.school is not None:
        free_slots=InterviewSlot.select().join(Mentor).where((InterviewSlot.reserved==False)&(Mentor.school==applicant.school.id))
    else:
        print('Applicant has no school yet,please assign school first')
        return None
    try:
        free_slot=random.choice(free_slots)
    except IndexError:
        return None
    return free_slot

def assign_interview(applicant):
    slot=random_slot(applicant)
    if slot is None:
        print('There is no available interview slot for ',applicant.name)
        return False
    Interview.create(applicant=applicant.id,slot=slot.id)
    InterviewSlot.update(reserved=True).where(InterviewSlot.id==slot.id).execute()

def display_all_interview():
    sub = Mentor.select(Mentor.name, Applicant.name.alias('app_name'), InterviewSlot,Mentor.school) \
        .join(School) \
        .switch(Mentor) \
        .join(InterviewSlot) \
        .join(Interview) \
        .join(Applicant)\
        .naive()

    for inter in sub:
        print(inter.name, inter.app_name, inter.start,inter.school.name)

def filter_all_interview(filter):
    if type(filter)==Mentor:
        sub = Mentor.select(Mentor.name, Applicant.name.alias('app_name'), InterviewSlot,Mentor.school) \
            .join(InterviewSlot) \
            .join(Interview) \
            .join(Applicant) \
            .where(Mentor.id==filter.id)\
            .naive()
    elif type(filter)==Applicant:
        sub = Mentor.select(Mentor.name, Applicant.name.alias('app_name'), InterviewSlot,Mentor.school) \
            .join(InterviewSlot) \
            .join(Interview) \
            .join(Applicant) \
            .where(Applicant.id == filter.id) \
            .naive()

    elif type(filter)==School:
        sub = Mentor.select(Mentor.name, Applicant.name.alias('app_name'), InterviewSlot,Mentor.school) \
            .join(InterviewSlot) \
            .join(Interview) \
            .join(Applicant) \
            .where(Mentor.school == filter.id) \
            .naive()
    else:
        print('date')

    for inter in sub:
        print(inter.name, inter.app_name, inter.start,inter.school.name)