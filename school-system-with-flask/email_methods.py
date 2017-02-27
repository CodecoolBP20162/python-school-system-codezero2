from applicant_methods import *  ##
from models import *  ##
import smtplib
import traceback
from interview_methods import *  ##
import psycopg2
import peewee


try:
    from models import *
except Exception:
    from .models import *
try:
    from interview_methods import *
except Exception:
    from .interview_methods import *
try:
    from email_methods import *
except Exception:
    from .email_methods import *


class SendEmails:

    gmail_user = "codezerocc@gmail.com"
    gmail_pwd = "codecool"
    FROM = "codezerocc@gmail.com"

    @staticmethod
    def get_email_text(file_name):
        with open(file_name, "r") as file:
            text = file.read()
            return text

    @classmethod
    def send_email(cls, TO, message):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(cls.gmail_user, cls.gmail_pwd)
            server.sendmail(cls.FROM, TO, message.encode("utf8"))
            server.close()
        except Exception:
            print("failed to send mail")
            traceback.print_exc()

    """ APPLICANT REGISTRATION EMAIL """

    @classmethod
    def get_applicant_reg_info(cls, new_applicant_id):
        user = Applicant.select().where(Applicant.applicant_id == new_applicant_id).get()
        email = "codezerocc@gmail.com"  # user.email
        first_name = user.first_name
        last_name = user.last_name
        name = first_name + ' ' + last_name
        application_code = user.applicant_id
        school_name = user.school.name

        TO = email if type(email) is list else email
        SUBJECT = "Information about your application to Codecool"
        TEXT = cls.get_email_text("applicant_reg_email.txt").format(
            first_name,
            last_name,
            application_code,
            school_name)

        return TO, SUBJECT, TEXT, name

    @classmethod
    def prepare_applicant_reg_info(cls, new_applicant_id):
        TO, SUBJECT, TEXT, name = cls.get_applicant_reg_info(new_applicant_id)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (cls.FROM, ", ".join(TO), SUBJECT, TEXT)
        cls.reg_email_sent(new_applicant_id)
        return TO, message

    @classmethod
    def reg_email_sent(cls, new_applicant_id):
        recipient_email, subject, preview, recipient_name = cls.get_applicant_reg_info(new_applicant_id)
        Email.create(
            subject = subject,
            preview = preview[0:139],
            email_type = "Registration",
            recipient_name = recipient_name,
            recipient_email = recipient_email
        )

    """ APPLICANT INTERVIEW EMAIL """

    @classmethod
    def get_applicant_interview_info(cls, new_applicant_id):

        user = Applicant.select().where(Applicant.applicant_id == new_applicant_id).get()
        email = "codezerocc@gmail.com"  # user.email
        first_name = user.first_name
        last_name = user.last_name
        name = first_name + ' ' + last_name
        school_name = user.school.name
        interview_start_yr = user.interview[0].slot.start.year
        interview_start_mth = user.interview[0].slot.start.month
        interview_start_day = user.interview[0].slot.start.day
        interview_start_hr = user.interview[0].slot.start.hour
        mentor_first_name = user.interview[0].slot.assigned_mentor.first_name
        mentor_last_name = user.interview[0].slot.assigned_mentor.last_name

        interview_start = "{}-{}-{} {}:00".format(interview_start_yr,
                                                  interview_start_mth,
                                                  interview_start_day,
                                                  interview_start_hr)

        TO = email if type(email) is list else email
        SUBJECT = "Information about your personal interview at Codecool"
        TEXT = cls.get_email_text("applicant_interview_email.txt").format(
            first_name,
            last_name,
            school_name,
            interview_start,
            mentor_first_name,
            mentor_last_name)

        return TO, SUBJECT, TEXT, name

    @classmethod
    def prepare_applicant_interview_info(cls, new_applicant_id):
        TO, SUBJECT, TEXT, name = cls.get_applicant_interview_info(new_applicant_id)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (cls.FROM, ", ".join(TO), SUBJECT, TEXT)
        cls.app_interview_email_sent(new_applicant_id)
        return TO, message

    @classmethod
    def app_interview_email_sent(cls, new_applicant_id):
        recipient_email, subject, preview, recipient_name = cls.get_applicant_interview_info(new_applicant_id)
        Email.create(
            subject=subject,
            preview=preview[0:139],
            email_type="Applicant Interview",
            recipient_name=recipient_name,
            recipient_email=recipient_email
        )

    """ MENTOR EMAIL """

    @classmethod
    def get_mentor_interview_info(cls, new_applicant_id):
        user = Applicant.select().where(Applicant.applicant_id == new_applicant_id).get()
        assigned_mentor = user.interview[0].slot.assigned_mentor.id
        applicant_first_name = user.first_name
        applicant_last_name = user.last_name
        application_code = user.applicant_id
        school_name = user.school.name
        interview_start_yr = user.interview[0].slot.start.year
        interview_start_mth = user.interview[0].slot.start.month
        interview_start_day = user.interview[0].slot.start.day
        interview_start_hr = user.interview[0].slot.start.hour

        interview_start = "{}-{}-{} {}:00".format(interview_start_yr,
                                                  interview_start_mth,
                                                  interview_start_day,
                                                  interview_start_hr)

        mentor = Mentor.select().where(Mentor.id == assigned_mentor).get()
        mentor_first_name = mentor.first_name
        mentor_last_name = mentor.last_name
        mentor_name = mentor_first_name + ' ' + mentor_last_name
        email = "codezerocc@gmail.com"  # mentor.email

        TO = email if type(email) is list else email
        SUBJECT = "A new interview was assigned to you"
        TEXT = cls.get_email_text("mentor_email.txt").format(
            mentor_first_name,
            mentor_last_name,
            school_name,
            applicant_first_name,
            applicant_last_name,
            application_code,
            interview_start)

        return TO, SUBJECT, TEXT, mentor_name

    @classmethod
    def prepare_mentor_interview_info(cls, new_applicant_id):
        TO, SUBJECT, TEXT, mentor_name = cls.get_mentor_interview_info(new_applicant_id)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (cls.FROM, ", ".join(TO), SUBJECT, TEXT)
        cls.mentor_interview_email_sent(new_applicant_id)
        return TO, message

    @classmethod
    def mentor_interview_email_sent(cls, new_applicant_id):
        recipient_email, subject, preview, recipient_name = cls.get_mentor_interview_info(new_applicant_id)
        Email.create(
            subject=subject,
            preview=preview[0:139],

            email_type="Mentor Interview",
            recipient_name=recipient_name,
            recipient_email=recipient_email
        )

    @staticmethod
    def filter_redirect(choice, query):
        if choice == "type":
            return "filter_by_type"
        elif choice == "subject":
            return "filter_by_subject"
        elif choice == "recipient":
            return "filter_by_recipient"


    @staticmethod
    def send_emails(new_applicant_id):

        applicant_email, message = SendEmails.prepare_applicant_reg_info(new_applicant_id)
        SendEmails.send_email(applicant_email, message)

        applicant_email, message = SendEmails.prepare_applicant_interview_info(new_applicant_id)
        SendEmails.send_email(applicant_email, message)

        mentor_email, message = SendEmails.prepare_mentor_interview_info(new_applicant_id)
        SendEmails.send_email(mentor_email, message)
