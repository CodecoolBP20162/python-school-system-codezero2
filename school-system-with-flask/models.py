from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
import datetime

# Configure your database connection here
# database name = should be your username on your laptop

db = PostgresqlDatabase('schoolsystem', user='codezero', password='codezero', host='46.101.4.131')


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db


class School(BaseModel):
    name = CharField()


class User(BaseModel, UserMixin):
    login = CharField()
    password = CharField()
    role = CharField(default="applicant")

    @classmethod
    def create_user(cls, login, password):
        user = cls.create(login=login, password=generate_password_hash(password))
        return user



class Applicant(BaseModel):
    applicant_id = CharField(unique=True, null=True)
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    application_date = DateTimeField(default=datetime.datetime.now().date())
    city = CharField()
    status = CharField(default="applied")
    school = ForeignKeyField(School, related_name="applicants", null=True)
    user = ForeignKeyField(User, related_name='applicant', unique=True, null=False)

    class Meta:
        order_by = ('first_name', 'last_name', 'application_date')


class City(BaseModel):
    city_name = CharField()
    location = ForeignKeyField(School, related_name="location")


class Mentor(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    school = ForeignKeyField(School, related_name="mentors")
    user_id = ForeignKeyField(User, related_name='mentor', unique=True, null=False)


class InterviewSlot(BaseModel):
    start = DateTimeField()
    end = DateTimeField()
    reserved = BooleanField()
    week = IntegerField()
    assigned_mentor = ForeignKeyField(Mentor, related_name="slot")

    class Meta:
        indexes = (
            # create a unique one from/to/date
            (('start', 'end', 'assigned_mentor'), True),
        )


class Interview(BaseModel):
    applicant = ForeignKeyField(Applicant, related_name="interview")
    slot = ForeignKeyField(InterviewSlot, related_name='interview')


class Email(BaseModel):
    subject = CharField()
    preview = CharField()
    email_type = CharField(null=True)
    sent_date = DateTimeField(default=datetime.datetime.now().date())
    recipient_name = CharField()
    recipient_email = CharField(null=True)

class Week(BaseModel):
    id=IntegerField()
    monday=DateField()
    tuesday=DateField()
    wednesday=DateField()
    thursday=DateField()
    friday=DateField()

#db.create_table(Email)


'''
for i in range(1, 7):
    InterviewSlot.create(start='2017-03-0{} 11:00'.format(i), end='2017-03-0{} 12:00'.format(i), reserved=False, assigned_mentor=3)

for i in range(8, 10):
    InterviewSlot.create(start='2017-03-0{} 11:00'.format(i), end='2017-03-0{} 12:00'.format(i), reserved=False, assigned_mentor=3)


for i in range(10, 20):
    InterviewSlot.create(start='2017-03-{} 11:00'.format(i), end='2017-03-{} 12:00'.format(i), reserved=False, assigned_mentor=5)

for i in range(20, 30):
    InterviewSlot.create(start='2017-03-{} 11:00'.format(i), end='2017-03-{} 12:00'.format(i), reserved=False, assigned_mentor=6)

for i in range(1, 10):
    InterviewSlot.create(start='2017-04-0{} 11:00'.format(i), end='2017-04-0{} 12:00'.format(i), reserved=False, assigned_mentor=3)


for i in range(10, 20):
    InterviewSlot.create(start='2017-04-{} 11:00'.format(i), end='2017-04-{} 12:00'.format(i), reserved=False, assigned_mentor=5)

for i in range(20, 30):
    InterviewSlot.create(start='2017-04-{} 11:00'.format(i), end='2017-04-{} 12:00'.format(i), reserved=False, assigned_mentor=6)
'''
"""
Week.create(id=11,monday='2017-03-13',tuesday='2017-03-14',wednesday='2017-03-15',thursday='2017-03-16',friday='2017-03-17')
Week.create(id=12,monday='2017-03-20',tuesday='2017-03-21',wednesday='2017-03-22',thursday='2017-03-23',friday='2017-03-24')
"""
"""
mentors=Mentor.select()

for mentor in mentors:
    for hour in range(10,12):
        InterviewSlot.create(start='2017-03-03 {}:00'.format(hour),end='2017-03-03 {}:00'.format(hour + 1),reserved=False,assigned_mentor=mentor.id,week=9)
    for hour in range(13,15):
        InterviewSlot.create(start='2017-03-03 {}:00'.format(hour),end= '2017-03-03 {}:00'.format(hour + 1),reserved=False,assigned_mentor=mentor.id,week=9)
"""