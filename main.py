from models import *
from applicant_methods import *
from interview_methods import *
from mentor_methods import *
import os
from collections import OrderedDict
import time
import datetime
import peewee
import psycopg2


# Write here your console application

class Menu:
    main_menu = OrderedDict([
        (" 0", "Register new Applicant"),
        (" 1", "Administrator menu"),
        (" 2", "Mentor menu"),
        (" 3", "Applicant menu")

    ])

    Admin_menu = OrderedDict([
        (" 1", "Display all applicants"),
        (" 2", "Assign ID to new applicants"),
        (" 3", "Assign SCHOOL to new applicants"),
        (" 4", "Assign interview to new applicants"),
        (" 5", "Assign second mentor to an interview"),
        (" 6", "Filter Applicants by status"),
        (" 7", "Filter Applicants by location"),
        (" 8", "Filter Applicants by school"),
        (" 9", "Filter Applicants by name"),
        (" 10", "Filter Applicants by time"),
        (" 11", "Filter Applicants by mentor")
    ])

    Applicant_menu = OrderedDict([
        (" 1", "Check application status"),
        (" 2", "View personal data"),
        (" 3", "View interview details")
    ])

    Mentor_menu = OrderedDict([
        (" 1", "View mentors"),
        (" 2", "View scheduled interviews"),
        (" 3", "Filter by school"),
        (" 4", "Filter by mentor"),
        (" 5", "Filter by date")
    ])

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    @classmethod
    def mentor_menu_loop(cls):
        choice = None

        while choice != "q":
            print("\n--MENTOR MENU--\n")
            print("Enter 'q' to go back\n")
            for key, value in cls.Mentor_menu.items():
                print("{}) {}".format(key, value))
            choice = input("Enter choice: ").lower().strip()

            if choice == "1":
                cls.clear()
                mentor_methods.display_all_mentor()

            if choice == "2":
                cls.clear()
                interview_methods.display_all_interview()

            elif choice == "4":
                cls.clear()
                choice = input("Type mentor ID:").lower().strip()
                cls.clear()
                try:
                    interview_methods.filter_mentor(int(choice))
                except ValueError:
                    print("Invalid keyword")

            elif choice == "3":
                cls.clear()
                choice = input("Which schools's interviews do u want to see? Enter school location:").strip()
                cls.clear()
                interview_methods.filter_school(choice)
            elif choice == '5':
                cls.clear()
                choice = input("Which date do you want to know. Format YYYY-MM-DD: ")
                try:
                    interview_methods.filter_date(choice)
                except (psycopg2.DataError, psycopg2.InternalError, peewee.DataError, peewee.InternalError):
                    print("Invalid format")

    @classmethod
    def applicant_menu_loop(cls):
        choice = None

        while choice != "q":
            print("\n--APPLICANT MENU--\n")
            print("Enter 'q' to go back\n")
            for key, value in cls.Applicant_menu.items():
                print("{}) {}".format(key, value))
            choice = input("Enter choice: ").lower().strip()

            if choice == "1":
                cls.clear()
                applicant_methods.check_status()
            elif choice == "2":
                cls.clear()
                applicant_methods.check_personal_data()
            elif choice == "3":
                cls.clear()
                applicant_methods.check_interview_details()

    @classmethod
    def admin_menu_loop(cls):
        choice = None

        while choice != "q":
            print("\n--ADMINISTRATOR MENU--\n")
            print("Enter 'q' to go back\n")
            for key, value in cls.Admin_menu.items():
                print("{}) {}".format(key, value))
            choice = input("Enter choice: ").lower().strip()

            if choice == "1":
                cls.clear()
                applicant_methods.display_all_data()
            elif choice == "2":
                cls.clear()
                applicant_methods.assign_id()
            elif choice == "3":
                cls.clear()
                applicant_methods.assign_school()
            elif choice == "4":
                cls.clear()
                interview_methods.assign_interviews()
            elif choice == "5":
                cls.clear()
                interview_methods.display_all_interview()
                try:
                    intview_id = int(input("Enter the id of the interview which u want to add a second mentor "))
                    interview = Interview.get(id=intview_id)
                    interview_methods.assign_second_mentor(interview)
                except ValueError:
                    print("Invalid input")

            elif choice == "6":
                cls.clear()
                string = input("Enter status (new/approved): ")
                applicant_methods.filter_by_status(string)
            elif choice == "7":
                cls.clear()
                string = input("Enter location: ")
                applicant_methods.filter_by_location(string)
            elif choice == "8":
                cls.clear()
                string = input("Enter school: ")
                applicant_methods.filter_by_school(string)
            elif choice == "9":
                cls.clear()
                string = input("Enter first name: ")
                string2 = input("Enger last name: ")
                applicant_methods.filter_by_name(string, string2)
            elif choice == "10":
                cls.clear()
                string = input("Enter date (YYYY-MM-DD): ")
                try:
                    applicant_methods.filter_by_time(string)
                except (psycopg2.DataError, psycopg2.InternalError, peewee.DataError, peewee.InternalError):
                    print("Invalid format")
            elif choice == "11":
                cls.clear()
                string = input("Enter mentor's first name: ")
                applicant_methods.filter_by_mentor(string)

    @classmethod
    def menu_loop(cls):
        # show the menu
        choice = None

        while choice != "q":
            print("\n--MAIN MENU--\n")
            print("Enter 'q' to quit\n")
            for key, value in cls.main_menu.items():
                print("{}) {}".format(key, value))
            choice = input("Enter choice: ").lower().strip()

            if choice == "1":
                cls.clear()
                cls.admin_menu_loop()
            elif choice == "2":
                cls.clear()
                cls.mentor_menu_loop()
            elif choice == "0":
                cls.clear()
                applicant_methods.register_applicant_process()
            elif choice == "3":
                cls.clear()
                cls.applicant_menu_loop()


Menu.menu_loop()
