# This script can generate example data for "City" and "InterviewSlot" models.

from models import *
import build


School.create(name='Budapest')
School.create(name='Miskolc')
School.create(name='Krakow')


"""City.create(city_name='Szeged',location=1)
City.create(city_name='Székesfehérvár',location=1)
City.create(city_name='Debrecen',location=2)
City.create(city_name='Warsaw',location=3)
City.create(city_name='Budapest',location=1)"""

f = open('telepules_csv.csv', 'r')

for i in f:
    line1 = i.split("\n")
    line2 = line1[0].split(',')
    #print(line2[0],line2[1])
    City.create(city_name=line2[0],location=line2[1])


Mentor.create(first_name='Matyi',last_name="Forián",email= '3242fsd@email.com',school=1)
Mentor.create(first_name='Zozie',last_name="Sallai",email= '3435hf@email.com',school=1)
Mentor.create(first_name='Laci',last_name='Szabó',email= '353dfh@email.com',school=2)
Mentor.create(first_name='Basil',last_name='Basil',email= '32443vd@email.com',school=3)

Applicant.create(first_name='Anna',last_name='Szabó',email = '34543tfsd@gmail.com',status='new',city='Szeged')
Applicant.create(first_name='Annabella',last_name='Varga',email = '34sdfs33@gmail.com',status='new',city='Debrecen')
Applicant.create(first_name='Pancsika',last_name='Tóth',email = '3496ghvd@gmail.com',status='new',city='Székesfehérvár')
Applicant.create(first_name='Robi',last_name='Gáspár',email = '3967sdgdgg@gmail.com',status='new',city='Budapest')
Applicant.create(first_name='Pavel',last_name='Nowak',email = '329634vv@gmail.com',status='approved',city='Warsaw')

InterviewSlot.create(start='2017-01-30 11:00',end='2017-01-30 12:00',reserved=True,assigned_mentor=1)
InterviewSlot.create(start='2017-01-17 13:00',end='2017-01-17 12:00',reserved=False,assigned_mentor=2)
InterviewSlot.create(start='2017-01-30 09:00',end='2017-01-30 12:00',reserved=False,assigned_mentor=3)
InterviewSlot.create(start='2017-01-31 07:00',end='2017-01-30 12:00',reserved=False,assigned_mentor=1)
InterviewSlot.create(start='2017-01-30 12:00',end='2017-01-30 12:00',reserved=True,assigned_mentor=4)
InterviewSlot.create(start='2017-01-31 15:00',end='2017-01-30 12:00',reserved=False,assigned_mentor=3)
InterviewSlot.create(start='2017-01-31 08:00',end='2017-01-30 12:00',reserved=False,assigned_mentor=2)


Interview.create(applicant=5,slot=5)
Interview.create(applicant=4,slot=1)

