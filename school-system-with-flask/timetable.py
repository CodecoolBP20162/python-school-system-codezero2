from models import *

WEEKDAYS=['monday','tuesday','wednesday','thursday','friday']
HOURS=['10','11','13','14']

def get_this_week(week_number):
    this_week_ins = Week.get(id=week_number)
    this_week = this_week_ins._data
    return this_week

def init_dict():
    slots_dict={}
    for day in WEEKDAYS:
        slots_dict.update({day:{}})
        for hour in HOURS:
            slots_dict[day].update({hour:None})
    return slots_dict

def fill_dict(mentor_id,this_week,week_number):
    slots = InterviewSlot.select().join(Interview, JOIN.LEFT_OUTER).where(
        (InterviewSlot.assigned_mentor == mentor_id) & (InterviewSlot.week == week_number))
    slots_dict=init_dict()
    for slot in slots:
        start=slot.start
        for item in this_week:
            if this_week[item]==start.date():
                slots_dict[item][str(start.hour)]=slot
                break
    return slots_dict