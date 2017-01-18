from models import *
import example_data
import random


def random_slot():
    free_slots=InterviewSlot.select().where(InterviewSlot.reserved==False)
    try:
        free_slot=random.choice(free_slots)
    except IndexError:
        return None
    return free_slot

def assign_interview(applicant):
    slot=random_slot()
    if slot is None:
        print('There is no available interview slot for ',applicant.name)
        return False
    Interview.create(applicant=applicant.id,slot=slot.id)
    InterviewSlot.update(reserved=True).where(InterviewSlot.id==slot.id).execute()

def display_all_interview():
    sub = Mentor.select(Mentor.name, Applicant.name.alias('app_name'), InterviewSlot) \
        .join(InterviewSlot) \
        .join(Interview) \
        .join(Applicant) \
        .naive()

    for inter in sub:
        print(inter.name, inter.app_name, inter.start,inter.end)



app=Applicant.get(Applicant.id==1)

app2=Applicant.get(Applicant.id==2)

assign_interview(app)
assign_interview(app2)
assign_interview(app2)
assign_interview(app2)


display_all_interview()



