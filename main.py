from models import *
from applicant_methods import *
from interview_methods import *
from mentor_methods import *
from new_applicants import *
import os
from collections import OrderedDict
import time
import datetime

# Write here your console application


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def mentor_menu_loop():
    choice = None

    while choice != "q":
        print("\n--MENTOR MENU--\n")
        print("Enter 'q' to go back\n")
        for key, value in Mentor_menu.items():
            print("{}) {}".format(key, value))
        choice = input("Enter choice: ").lower().strip()

        if choice == "w":
            clear()
            mentor_methods.display_all_mentor()

        if choice == "a":
            clear()
            interview_methods.display_all_interview()

        elif choice == "d":
            clear()
            choice = input("Type mentor ID:").lower().strip()
            clear()
            interview_methods.filter_mentor(int(choice))

        elif choice == "s":
            clear()
            choice = input("Which schools's interviews do u want to see? Enter school location:").strip()
            clear()
            interview_methods.filter_school(choice)
        elif choice == 'f':
            clear()
            choice = input("Which date do you want to know. Format YYYY-MM-DD: ")
            interview_methods.filter_date(choice)


def applicant_menu_loop():
    choice = None

    while choice != "q":
        print("\n--APPLICANT MENU--\n")
        print("Enter 'q' to go back\n")
        for key, value in Applicant_menu.items():
            print("{}) {}".format(key, value))
        choice = input("Enter choice: ").lower().strip()

        if choice == "a":
            clear()
            applicant_methods.check_status()
        elif choice == "s":
            clear()
            applicant_methods.check_personal_data()


def admin_menu_loop():
    choice = None

    while choice != "q":
        print("\n--ADMINISTRATOR MENU--\n")
        print("Enter 'q' to go back\n")
        for key, value in Admin_menu.items():
            print("{}) {}".format(key, value))
        choice = input("Enter choice: ").lower().strip()

        if choice == "a":
            clear()
            applicant_methods.display_all_data()
        elif choice == "f":
            clear()
            applicant_methods.assign_id()
        elif choice == "g":
            clear()
            applicant_methods.assign_school()
        elif choice == "t":
            clear()
            interview_methods.assign_interviews()
        elif choice == "h":
            clear()
            string = input("Enter status (new/approved): ")
            applicant_methods.filter_by_status(string)
        elif choice == "j":
            clear()
            string = input("Enter location: ")
            applicant_methods.filter_by_location(string)
        elif choice == "k":
            clear()
            string = input("Enter school: ")
            applicant_methods.filter_by_school(string)
        elif choice == "l":
            clear()
            string = input("Enter name: ")
            applicant_methods.filter_by_name(string)
        elif choice == "m":
            clear()
            string = input("Enter date (YYYY-MM-DD): ")
            applicant_methods.filter_by_time(string)
        elif choice == "n":
            clear()
            string = input("Enter mentor's name: ")
            applicant_methods.filter_by_mentor(string)


def menu_loop():
    # show the menu
    choice = None

    while choice != "q":
        print("\n--MAIN MENU--\n")
        print("Enter 'q' to quit\n")
        for key, value in main_menu.items():
            print("{}) {}".format(key, value))
        choice = input("Enter choice: ").lower().strip()

        if choice == "a":
            clear()
            admin_menu_loop()
        elif choice == "s":
            clear()
            mentor_menu_loop()
        elif choice == "n":
            clear()
            new_applicants.generate_applicant()
        elif choice == "d":
            clear()
            applicant_menu_loop()

main_menu = OrderedDict([
    ("n", "Generate new Applicant"),
    ("a", "Administrator menu"),
    ("s", "Mentor menu"),
    ("d", "Applicant menu")

])


Admin_menu = OrderedDict([
    ("a", "Display all applicants"),
    ("f", "Assign ID to new applicants"),
    ("t", "Assign interview to new applicants"),
    ("g", "Assign SCHOOL to new applicants"),
    ("h", "Filter Applicants by status"),
    ("j", "Filter Applicants by location"),
    ("k", "Filter Applicants by school"),
    ("l", "Filter Applicants by name"),
    ("m", "Filter Applicants by time"),
    ("n", "Filter Applicants by mentor")
])

Applicant_menu = OrderedDict([
    ("a", "Check application status"),
    ("s", "View personal data")
])

Mentor_menu = OrderedDict([
    ("w", "View mentors"),
    ("a", "View scheduled interviews"),
    ("s", "Filter by school"),
    ("d", "Filter by mentor"),
    ("f", "Filter by date")
])


menu_loop()
