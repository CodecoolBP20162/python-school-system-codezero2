from models import *
import smtplib

class send_emails:

    @staticmethod
    def email_applicant_with_reg_info(new_applicant_id):

        user = Applicant.select().where(Applicant.applicant_id == new_applicant_id).get()
        email = "codezerocc@gmail.com"  # user.email
        first_name = user.first_name
        last_name = user.last_name
        application_code = user.applicant_id
        school_name = user.school.name

        gmail_user = "codezerocc@gmail.com"
        gmail_pwd = "codecool"
        FROM = "codezerocc@gmail.com"
        TO = email if type(email) is list else [email]
        SUBJECT = "Information about your application to Codecool"
        TEXT = "Dear {} {},\n\n\
        We are emailing you because you have applied to our programming course at Codecool\n\
        Here are some details regarding your registration:\n\n\
        Your application code: {}\n\
        Your assigned school: {}\n\n\
        You will receive another email with details about your application process shortly.\n\n\
        Best Wishes\n\
        Codecool".format(
            first_name,
            last_name,
            application_code,
            school_name)

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            print('Thank you for applying!')
        except:
            print("failed to send mail")

    @staticmethod
    def email_applicant_with_interview_info(new_applicant_id):
        import smtplib

        user = Applicant.select().where(Applicant.applicant_id == new_applicant_id).get()
        email = "codezerocc@gmail.com"  # user.email
        first_name = user.first_name
        last_name = user.last_name
        application_code = user.applicant_id
        school_name = user.school.name
        interview_start = user.interview[0].slot.start,
        mentor_first_name = user.interview[0].slot.assigned_mentor.first_name,
        mentor_last_name = user.interview[0].slot.assigned_mentor.last_name

        gmail_user = "codezerocc@gmail.com"
        gmail_pwd = "codecool"
        FROM = "codezerocc@gmail.com"
        TO = email if type(email) is list else [email]
        SUBJECT = "Information about your personal interview at Codecool"
        TEXT = "Dear {} {},\n\n\
        We are inviting you for a personal interview here at Codecool\n\
        Here are some information regarding the details:\n\n\
        Location: {}\n\
        Your interview starts at: {}\n\n\
        You are assigned to our lovely mentor {} {}.\n\n\
        We are looking forward to meet you in person!\n\
        Codecool".format(
            first_name,
            last_name,
            school_name,
            interview_start,
            mentor_first_name,
            mentor_last_name)

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            #print('Thank you for applying!')
        except:
            print("failed to send mail")

    @staticmethod
    def email_mentor_with_interview_info(new_applicant_id):
        user = Applicant.select().where(Applicant.applicant_id == new_applicant_id).get()
        assigned_mentor = user.interview[0].slot.assigned_mentor.id
        applicant_first_name = user.first_name
        applicant_last_name = user.last_name
        application_code = user.applicant_id
        school_name = user.school.name
        interview_start = user.interview[0].slot.start,

        mentor = Mentor.select().where(Mentor.id == assigned_mentor).get()
        mentor_first_name = mentor.first_name
        mentor_last_name = mentor.last_name
        email = "codezerocc@gmail.com"  # mentor.email

        gmail_user = "codezerocc@gmail.com"
        gmail_pwd = "codecool"
        FROM = "codezerocc@gmail.com"
        TO = email if type(email) is list else [email]
        SUBJECT = "A new interview was assigned to you"
        TEXT = "Dear {} {},\n\n\
            This is an automated message letting you know that a new applicant was assigned to you for a personal interview.\n\
            Here are the details:\n\n\
            Location: {}\n\
            Applicant: {} {}\n\
            Application Code: {}\n\
            Interview starts at: {}\n\n\
            Best Wishes\n\
            Mr Robot".format(
            mentor_first_name,
            mentor_last_name,
            school_name,
            applicant_first_name,
            applicant_last_name,
            application_code,
            interview_start)

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            #print('Thank you for applying!')
        except:
            print("failed to send mail")