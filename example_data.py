# This script can generate example data for "City" and "InterviewSlot" models.

from models import *
import build

School.create(name='Budapest')
School.create(name='Miskolc')
School.create(name='Krakow')


City.create(city_name='Szeged',location=1)
City.create(city_name='Székesfehérvár',location=1)
City.create(city_name='Debrecen',location=2)
City.create(city_name='Warsaw',location=3)


Mentor.create(name='Matyi',school=1)
Mentor.create(name='Laci',school=2)
Mentor.create(name='Basil',school=3)

Applicant.create(name='Panni',status='new',city='Szeged')
Applicant.create(name='Ancsika',status='new',city='Debrecen')
Applicant.create(name='Pancsika',status='new',city='Székesfehérvár')

InterviewSlot.create(start='2017-01-30 11:00',end='2017-01-30 12:00',reserved=False,assigned_mentor=1)
InterviewSlot.create(start='2017-01-31 11:00',end='2017-01-30 12:00',reserved=False,assigned_mentor=1)
InterviewSlot.create(start='2017-01-30 11:00',end='2017-01-30 12:00',reserved=True,assigned_mentor=3)

Interview.create(applicant=1,slot=1)
Interview.create(applicant=2,slot=2)
Interview.create(applicant=3,slot=3)

#query=Mentor.select(Mentor,InterviewSlot).join(InterviewSlot).where(InterviewSlot.reserved==True)
query=Mentor.select(Mentor.name.alias('mentor_name'),InterviewSlot.start,Applicant.name,InterviewSlot.reserved).join(InterviewSlot).join(Interview).join(Applicant).naive()


for item in query:
    print(item.mentor_name,item.name,item.start,item.reserved)






