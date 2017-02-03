from models import *
import smtplib
import traceback


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
        application_code = user.applicant_id
        school_name = user.school.name

        TO = email if type(email) is list else [email]
        SUBJECT = "Information about your application to Codecool"
        TEXT = cls.get_email_text("applicant_reg_email.txt").format(
            first_name,
            last_name,
            application_code,
            school_name)

        return TO, SUBJECT, TEXT

    @classmethod
    def prepare_applicant_reg_info(cls, new_applicant_id):
        TO, SUBJECT, TEXT = cls.get_applicant_reg_info(new_applicant_id)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (cls.FROM, ", ".join(TO), SUBJECT, TEXT)

        return TO, message

    """ APPLICANT INTERVIEW EMAIL """

    @classmethod
    def get_applicant_interview_info(cls, new_applicant_id):

        user = Applicant.select().where(Applicant.applicant_id == new_applicant_id).get()
        email = "codezerocc@gmail.com"  # user.email
        first_name = user.first_name
        last_name = user.last_name
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

        TO = email if type(email) is list else [email]
        SUBJECT = "Information about your personal interview at Codecool"
        TEXT = cls.get_email_text("applicant_interview_email.txt").format(
            first_name,
            last_name,
            school_name,
            interview_start,
            mentor_first_name,
            mentor_last_name)

        return TO, SUBJECT, TEXT

    @classmethod
    def prepare_applicant_interview_info(cls, new_applicant_id):
        TO, SUBJECT, TEXT = cls.get_applicant_interview_info(new_applicant_id)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (cls.FROM, ", ".join(TO), SUBJECT, TEXT)

        return TO, message

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
        email = "codezerocc@gmail.com"  # mentor.email

        TO = email if type(email) is list else [email]
        SUBJECT = "A new interview was assigned to you"
        TEXT = cls.get_email_text("mentor_email.txt").format(
            mentor_first_name,
            mentor_last_name,
            school_name,
            applicant_first_name,
            applicant_last_name,
            application_code,
            interview_start)

        return TO, SUBJECT, TEXT

    @classmethod
    def prepare_mentor_interview_info(cls, new_applicant_id):
        TO, SUBJECT, TEXT = cls.get_mentor_interview_info(new_applicant_id)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (cls.FROM, ", ".join(TO), SUBJECT, TEXT)

        return TO, message