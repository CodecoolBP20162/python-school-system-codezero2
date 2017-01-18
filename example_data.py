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
Mentor.create(name='Laci',school=2)
Mentor.create(name='Basil',school=3)

Applicant.create(name='Panni',status='new',city='Szeged')
Applicant.create(name='Ancsika',status='new',city='Debrecen')
Applicant.create(name='Pancsika',status='new',city='Székesfehérvár')
Applicant.create(name='Robi',status='new',applicant_id='as3A5',city='Budapest')

InterviewSlot.create(start='2017-01-30 11:00',end='2017-01-30 12:00',reserved=False,assigned_mentor=1)
InterviewSlot.create(start='2017-01-31 11:00',end='2017-01-30 12:00',reserved=False,assigned_mentor=1)
InterviewSlot.create(start='2017-01-30 11:00',end='2017-01-30 12:00',reserved=True,assigned_mentor=3)

Interview.create(applicant=1,slot=1)
Interview.create(applicant=2,slot=2)
Interview.create(applicant=3,slot=3)

#query=Mentor.select(Mentor,InterviewSlot).join(InterviewSlot).where(InterviewSlot.reserved==True)

"""
query=Mentor.select(Mentor.name.alias('mentor_name'),InterviewSlot.start,Applicant.name,InterviewSlot.reserved).join(InterviewSlot).join(Interview).join(Applicant).naive()


for item in query:
    print(item.mentor_name,item.name,item.start,item.reserved)
"""

query=Applicant.select(Applicant.name,Applicant.city,School.name.alias('school_name')).join(City,on=City.city_name==Applicant.city).join(School).naive()

for applicant in query:
    print(applicant.name,applicant.city,applicant.school_name)

"""
subquery = Tweet.select(fn.COUNT(Tweet.id)).where(Tweet.user == User.id)
update = User.update(num_tweets=subquery)
update.execute()

"""

subq=City.select(City.location).where(City.location==School.id)

for item in subq:
    print(City.city_name)

#update=Applicant.update(school=subq)
#update.execute()






