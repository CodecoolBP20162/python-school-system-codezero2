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
City.create(city_name='Budapest',location=1)


Mentor.create(name='Matyi',school=1)
Mentor.create(name='Zozie',school=1)
Mentor.create(name='Laci',school=2)
Mentor.create(name='Basil',school=3)

Applicant.create(name='Panni',status='new',city='Szeged',school=1)
Applicant.create(name='Ancsika',status='new',city='Debrecen',school=2)
Applicant.create(name='Pancsika',status='new',city='Székesfehérvár')
Applicant.create(name='Robi',status='new',applicant_id='as3A5',city='Budapest')
Applicant.create(name='Pavel',status='approved',city='Warsaw')

InterviewSlot.create(start='2017-01-30 11:00',end='2017-01-30 12:00',reserved=False,assigned_mentor=1)
InterviewSlot.create(start='2017-01-17 11:00',end='2017-01-30 12:00',reserved=False,assigned_mentor=2)
InterviewSlot.create(start='2017-01-30 11:00',end='2017-01-30 12:00',reserved=False,assigned_mentor=3)
InterviewSlot.create(start='2017-01-31 11:00',end='2017-01-30 12:00',reserved=False,assigned_mentor=1)
InterviewSlot.create(start='2017-01-30 11:00',end='2017-01-30 12:00',reserved=True,assigned_mentor=4)

Interview.create(applicant=5,slot=5)
Interview.create(applicant=4,slot=1)
