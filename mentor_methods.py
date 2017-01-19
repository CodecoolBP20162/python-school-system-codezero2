from models import *
import example_data


def display_all_mentor():
    mentors = Mentor.select(Mentor.id, Mentor.name, School.name.alias("school_name"))\
        .join(School)\
        .naive()

    for person in mentors:
        print("\nMentor ID: {}\nNAME: {}\nSchool: {}"
              .format(person.id, person.name, person.school_name))


