from models import *
import example_data


class mentor_methods:
    def display_all_mentor():
        mentors = Mentor.select()

        for person in mentors:
            school_name = "None"
            if person.school is not None:
                school_name = person.school.name
            print("\nMENTOR ID: {}\nFIRST NAME: {}\nLAST NAME: {}\nEMAIL: {}\nSCHOOL: {}"
                  .format(person.id, person.first_name, person.last_name, person.email, school_name))
