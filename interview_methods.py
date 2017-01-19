from models import *
import example_data
import random


def random_slot(applicant):
    if applicant.school is not None:
        free_slots = InterviewSlot.select().join(Mentor).where((InterviewSlot.reserved == False) & (Mentor.school == applicant.school.id))
    else:
        print('Applicant has no school yet,please assign school first')
        return None
    try:
        free_slot = random.choice(free_slots)
    except IndexError:
        return None
    return free_slot


def assign_interviews():
    sub=select_applicant_wo_interview()
    for applicant in sub:
        slot = random_slot(applicant)
        if slot is None:
            print('There is no available interview slot for ', applicant.name)
            return False
        Interview.create(applicant=applicant.id, slot=slot.id)
        InterviewSlot.update(reserved=True).where(InterviewSlot.id == slot.id).execute()


def display_all_interview():
    sub = Mentor.select(Mentor.name, Applicant.name.alias('app_name'), InterviewSlot, Mentor.school) \
        .join(School) \
        .switch(Mentor) \
        .join(InterviewSlot) \
        .join(Interview) \
        .join(Applicant)\
        .naive()

    for inter in sub:
        print(inter.name, inter.app_name, inter.start, inter.school.name)


def filter_all_interview(filter):
    if type(filter) == Mentor:
        sub = Mentor.select(Mentor.name, Applicant.name.alias('app_name'), InterviewSlot, Mentor.school) \
            .join(InterviewSlot) \
            .join(Interview) \
            .join(Applicant) \
            .where(Mentor.id == filter.id)\
            .naive()

    elif type(filter) == Applicant:
        sub = Mentor.select(Mentor.name, Applicant.name.alias('app_name'), InterviewSlot, Mentor.school) \
            .join(InterviewSlot) \
            .join(Interview) \
            .join(Applicant) \
            .where(Applicant.id == filter.id) \
            .naive()

    elif type(filter) == School:
        sub = Mentor.select(Mentor.name, Applicant.name.alias('app_name'), InterviewSlot, Mentor.school) \
            .join(InterviewSlot) \
            .join(Interview) \
            .join(Applicant) \
            .where(Mentor.school == filter.id) \
            .naive()
    else:
        sub = Mentor.select(Mentor.name, Applicant.name.alias('app_name'), InterviewSlot, Mentor.school) \
            .join(InterviewSlot) \
            .join(Interview) \
            .join(Applicant) \
            .where(InterviewSlot.start < filter) \
            .naive()


    if len(sub)==0:
        print('there are no scheduled iws')
    else:
        for inter in sub:
            print(inter.name, inter.app_name, inter.start, inter.school.name)

def filter_mentor(number):
    mentor=Mentor.get(Mentor.id==number)
    filter_all_interview(mentor)

def filter_school(text):
    school=School.select().where(School.name==text)
    if len(school)==0:
        print('type again')
    else:
        school = school[0]
        filter_all_interview(school)

def filter_date(date):
    filter_all_interview(date)

def select_applicant_wo_interview():
    sub=Applicant.select().join(Interview,join_type=JOIN_LEFT_OUTER).where(Interview.applicant==None)
    return sub
