from peewee import *

import datetime

# Configure your database connection here
# database name = should be your username on your laptop
# database user = should be your username on your laptop
db = PostgresqlDatabase('dbname', user='dbuser')


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db


class School(BaseModel):
    name = CharField()


class Applicant(BaseModel):
    applicant_id = CharField(unique=True, default=None)
    name = CharField()
    #application_date = DateTimeField(default=datetime.datetime.now)
    #interview_date = DateTimeField(default=None)
    city = CharField()
    status = CharField(default="applied")
    school = ForeignKeyField(School, related_name="applicants")


class City(BaseModel):
    name = CharField()
    location = ForeignKeyField(School, related_name="location")


class Mentor(BaseModel):
    name = CharField()
    school = ForeignKeyField(School, related_name="mentors")


class Interview(BaseModel):
    applicant = ForeignKeyField(Applicant, related_name="interview")


class InterviewSlot(BaseModel):
    start = CharField()
    end = CharField()
    reserved = BooleanField()
    assigned_mentor = ForeignKeyField(Mentor, related_name="interview_slot")
