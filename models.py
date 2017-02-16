from peewee import *
import random
import datetime


# Configure your database connection here
# database name = should be your username on your laptop
# database user = should be your username on your laptop
db = PostgresqlDatabase('robertgaspar', user='robertgaspar')


# db = PostgresqlDatabase('schoolsystem', user='codezero',password='codezero',host='46.101.4.131')


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db


class School(BaseModel):
    name = CharField()


class Applicant(BaseModel):
    applicant_id = CharField(unique=True, null=True)
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    application_date = DateTimeField(default=datetime.datetime.now().date())
    city = CharField()
    status = CharField(default="applied")
    school = ForeignKeyField(School, related_name="applicants", null=True)


class City(BaseModel):
    city_name = CharField()
    location = ForeignKeyField(School, related_name="location")


class Mentor(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    school = ForeignKeyField(School, related_name="mentors")


class InterviewSlot(BaseModel):
    start = DateTimeField()
    end = DateTimeField()
    reserved = BooleanField()
    assigned_mentor = ForeignKeyField(Mentor, related_name="slot")

    class Meta:
        indexes = (
            (('start', 'end', 'assigned_mentor'), True),
        )


class Interview(BaseModel):
    applicant = ForeignKeyField(Applicant, related_name="interview")
    slot = ForeignKeyField(InterviewSlot, related_name='interview', null=False)
    slot_mentor2 = ForeignKeyField(InterviewSlot, related_name='interview2', null=True)

