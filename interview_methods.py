from models import *
import random
from print_table import *


class interview_methods:
    @staticmethod
    def random_slot(applicant):
        if applicant.school is not None:
            free_slots = InterviewSlot.select().join(Mentor).where(
                (InterviewSlot.reserved == False) & (Mentor.school == applicant.school.id))
        else:
            print('Applicant has no school yet,please assign school first')
            return None
        try:
            free_slot = random.choice(free_slots)
        except IndexError:
            return None
        return free_slot

    @classmethod
    def assign_interviews(cls):
        sub = interview_methods.select_applicant_wo_interview()
        for applicant in sub:
            slot = cls.random_slot(applicant)
            if slot is None:
                print('There is no available interview slot for ', applicant.first_name, applicant.last_name)
                return False
            Interview.create(applicant=applicant.id, slot=slot.id)
            InterviewSlot.update(reserved=True).where(InterviewSlot.id == slot.id).execute()

    @classmethod
    def assign_second_mentor(cls, interview):
        sub = InterviewSlot.select().join(Interview, join_type=JOIN_LEFT_OUTER).switch(InterviewSlot).join(
            Mentor).where((InterviewSlot.start == interview.slot.start) & (InterviewSlot.reserved == False) &
                          (Mentor.school == interview.applicant.school))
        if len(sub) == 0:
            print('Impossibru')
        else:
            slot = random.choice(sub)
            Interview.update(slot_mentor2=slot.id).where(Interview.id == interview.id).execute()
            InterviewSlot.update(reserved=True).where(InterviewSlot.id == slot.id).execute()

    @classmethod
    def assign_interview(cls, applicant):
        slot = cls.random_slot(applicant)
        if slot is None:
            print('There is no available interview slot for ', applicant.first_name, applicant.last_name)
            return False
        Interview.create(applicant=applicant.id, slot=slot.id)
        InterviewSlot.update(reserved=True).where(InterviewSlot.id == slot.id).execute()

    @staticmethod
    def display_all_interview():
        sub = Interview.select()
        print_interview_table(sub)

    @staticmethod
    def filter_all_interview(filter):
        if type(filter) == Mentor:
            sub = Mentor.select(Mentor.first_name, Mentor.last_name, Applicant.first_name.alias('app_name'),
                                InterviewSlot, Mentor.school) \
                .join(InterviewSlot) \
                .join(Interview) \
                .join(Applicant) \
                .where(Mentor.id == filter.id) \
                .naive()

        elif type(filter) == Applicant:
            sub = Mentor.select(Mentor.first_name, Mentor.last_name, Applicant.first_name.alias('app_name'),
                                InterviewSlot, Mentor.school) \
                .join(InterviewSlot) \
                .join(Interview) \
                .join(Applicant) \
                .where(Applicant.id == filter.id) \
                .naive()

        elif type(filter) == School:
            sub = Mentor.select(Mentor.first_name, Mentor.last_name, Applicant.first_name.alias('app_name'),
                                InterviewSlot, Mentor.school) \
                .join(InterviewSlot) \
                .join(Interview) \
                .join(Applicant) \
                .where(Mentor.school == filter.id) \
                .naive()
        else:
            sub = Mentor.select(Mentor.first_name, Mentor.last_name, Applicant.first_name.alias('app_name'),
                                InterviewSlot, Mentor.school) \
                .join(InterviewSlot) \
                .join(Interview) \
                .join(Applicant) \
                .where(InterviewSlot.start < filter) \
                .naive()

        if len(sub) == 0:
            print('there are no scheduled iws')
        else:
            print_interview_table(sub)

    @classmethod
    def filter_mentor(cls, number):
        mentor = Mentor.get(Mentor.id == number)
        cls.filter_all_interview(mentor)

    @classmethod
    def filter_school(cls, text):
        school = School.select().where(School.name == text)
        if len(school) == 0:
            print('type again')
        else:
            school = school[0]
            cls.filter_all_interview(school)

    @classmethod
    def filter_date(cls, date):
        cls.filter_all_interview(date)

    @staticmethod
    def select_applicant_wo_interview():
        sub = Applicant.select().join(Interview, join_type=JOIN_LEFT_OUTER).where(Interview.applicant == None)
        return sub