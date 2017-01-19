from models import *
from applicant_methods import *
import os
from collections import OrderedDict
import time

# Write here your console application


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def applicant_menu_loop():
    choice = None

    while choice != "q":
        print("\n--APPLICANT MENU--\n")
        print("Enter 'q' to go back\n")
        for key, value in Admin_menu.items():
            print("{}) {}".format(key, value))
        choice = input("Enter choice: ").lower().strip()

        if choice == "a":
            clear()
            print("CHOICE A")
        elif choice == "s":
            clear()
            print("CHOICE S")


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
            display_all_data()
        elif choice == "s":
            clear()
            show_applicants_without_id()
        elif choice == "d":
            clear()
            show_applicants_with_id()
        elif choice == "f":
            clear()
            assign_id()
        elif choice == "g":
            clear()
            assign_school()
        elif choice == "h":
            clear()
            string = input("Enter status (new/approved): ")
            filter_by_status(string)


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
            print("CHOICE S")

main_menu = OrderedDict([
    ("a", "Administrator menu"),
    ("s", "Mentor menu"),
    ("d", "Applicant menu")
])


Admin_menu = OrderedDict([
    ("a", "Display all applicants"),
    ("s", "Show applicants w/o ID"),
    ("d", "Show applicants with ID"),
    ("f", "Assign ID to new applicants"),
    ("g", "Assign SCHOOL to new applicants"),
    ("h", "Filter Applicants by status")
])


menu_loop()
