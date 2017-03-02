from flask import Flask, render_template, request, url_for, redirect, flash, abort
from peewee import *

from applicant_methods import *
from timetable import *
import mentor_methods
import interview_methods
from email_methods import *
import forms
import pushover
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_bcrypt import check_password_hash


try:
    from forms import *
except Exception:
    from .forms import *
try:
    from models import *
except Exception:
    from .models import *
try:
    from interview_methods import *
except Exception:
    from .interview_methods import *

try:
    from applicant_methods import *
except Exception:
    from .applicant_methods import *

try:
    from mentor_methods import *
except Exception:
    from .mentor_methods import *

try:
    from pushover import *
except Exception:
    from .pushover import *

try:
    from email_methods import *
except Exception:
    from .email_methods import *


def count_menu_items():
    num_of_applicants = int(len(Applicant.select()))
    num_of_interviews = int(len(Interview.select()))
    num_of_emails = int(len(Email.select()))
    num_of_mentors = int(len(Mentor.select()))
    return num_of_applicants, num_of_mentors, num_of_emails, num_of_interviews


app = Flask(__name__)
app.secret_key = 'aosjndajndjansdojnasd.asdadas.d.d.1'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(User.id == user_id)
    except DoesNotExist:
        return None


""" LOGIN - INDEX PAGE"""


@app.route('/assign_interview', methods=["GET", "POST"])
@login_required
def assgn():
    applicants = Applicant.select()
    for applicant in applicants:
        interview_methods.assign_interview(applicant)
    return redirect(url_for('homepage'))


@app.route('/', methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    form2 = forms.RegisterForm()

    if request.method == "POST" and form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class

        try:
            user = User.get(form.username.data == User.login)

        except DoesNotExist:
            flash('Invalid username or password.')
            return render_template('homepage.html', form=form, form2=form2)
        try:
            if user.password == form.password.data:
                login_user(user)
            elif check_password_hash(user.password, form.password.data):
                login_user(user)
        except Exception:
            flash('Invalid password.')
            return render_template('homepage.html', form=form, form2=form2)

        # next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        # if not is_safe_url(next):
        #    return Flask.abort(400)
        if current_user.role == 'admin':
            return redirect(url_for('homepage'))
        elif current_user.role == 'applicant':

            query = user.login
            return redirect(url_for('user_page', query=query))
        elif current_user.role == 'mentor':
            return redirect(url_for('mentor_page'))
        else:
            return redirect(url_for('homepage'))
    return render_template("homepage.html", form=form, form2=form2)


@app.route('/register', methods=["GET", "POST"])
def register():
    form2 = forms.RegisterForm()
    form = forms.LoginForm()
    if request.method == "POST" and form2.validate_on_submit():
        flash("You have successfully registered", "success")
        id = ApplicantMethods.create_new_user(form2)
        SendEmails.send_emails(id)
        return redirect(url_for("thanks"))
    return render_template("register3.html", form2=form2, form=form)


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

""" ADMIN HOMEPAGE """


@app.route('/admin', methods=["GET", "POST"])
@login_required
def homepage():
    if current_user.role != 'admin':
        return redirect(url_for('abort'))
    Applicants = Applicant.select()
    len_applicants, len_mentors, len_emails, len_interviews = count_menu_items()
    form = forms.FilterApplicantForm()
    if request.method == "GET":
        return render_template(
            "index2.html",
            form=form,
            Applicants=Applicants,
            len_applicants=len_applicants,
            len_interviews=len_interviews,
            len_emails=len_emails,
            len_mentors=len_mentors
        )
    elif request.method == "POST":
        if request.form.get('update_form'):
            app_id = request.form.get('update_form_applicant_id')
            new_email = request.form.get('update_email')
            new_school = request.form.get('update_school')
            new_status = request.form.get('update_status')
            applicant = Applicant.select().where(Applicant.applicant_id == app_id).get()
            applicant.email = new_email
            applicant.school.name = new_school
            applicant.status = new_status
            applicant.save()
            return redirect(url_for('homepage'))
        elif form.validate_on_submit():
            query = request.form.get('name')
            choice = request.form.get('options')
            url = ApplicantMethods.filter_redirect(choice, query)
            return redirect(url_for(url, query=query))


""" FILTER APPLICANTS BY FIRST NAME """


@app.route('/filter_by_first_name/<query>', methods=["GET", "POST"])
@login_required
def filter_by_first_name(query):
    if current_user.role != 'admin':
        abort(404)
    Applicants = Applicant.select().where(Applicant.first_name.contains(query))
    len_applicants, len_mentors, len_emails, len_interviews = count_menu_items()
    form = forms.FilterApplicantForm()
    update_form = forms.UpdateApplicantForm()
    if request.method == "GET":
        return render_template(
            "index2.html",
            Applicants=Applicants,
            len_applicants=len_applicants,
            len_interviews=len_interviews,
            len_emails=len_emails,
            len_mentors=len_mentors,
            form=form,
            update_form=update_form
        )

    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = ApplicantMethods.filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" FILTER APPLICANTS BY LAST NAME """


@app.route('/filter_by_last_name/<query>', methods=["GET", "POST"])
@login_required
def filter_by_last_name(query):
    if current_user.role != 'admin':
        abort(404)
    Applicants = Applicant.select().where(Applicant.last_name.contains(query))
    len_applicants, len_mentors, len_emails, len_interviews = count_menu_items()
    form = forms.FilterApplicantForm()
    update_form = forms.UpdateApplicantForm()
    if request.method == "GET":
        return render_template(
            "index2.html",
            Applicants=Applicants,
            len_applicants=len_applicants,
            len_interviews=len_interviews,
            len_emails=len_emails,
            len_mentors=len_mentors,
            form=form,
            update_form=update_form
        )

    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = ApplicantMethods.filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" FILTER APPLICANTS BY SCHOOL """


@app.route('/filter_by_school/<query>', methods=["GET", "POST"])
@login_required
def filter_by_school(query):
    if current_user.role != 'admin':
        abort(404)
    Applicants = Applicant.select().join(School).where(School.name.contains(query))
    len_applicants, len_mentors, len_emails, len_interviews = count_menu_items()
    form = forms.FilterApplicantForm()
    update_form = forms.UpdateApplicantForm()
    if request.method == "GET":
        return render_template(
            "index2.html",
            Applicants=Applicants,
            len_applicants=len_applicants,
            len_interviews=len_interviews,
            len_emails=len_emails,
            len_mentors=len_mentors,
            form=form,
            update_form=forms.UpdateApplicantForm()
        )

    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = ApplicantMethods.filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" FILTER APPLICANTS BY STATUS """


@app.route('/filter_by_status/<query>', methods=["GET", "POST"])
@login_required
def filter_by_status(query):
    if current_user.role != 'admin':
        abort(404)
    Applicants = Applicant.select().where(Applicant.status.contains(query))
    len_applicants, len_mentors, len_emails, len_interviews = count_menu_items()
    form = forms.FilterApplicantForm()
    update_form = forms.UpdateApplicantForm()
    if request.method == "GET":
        return render_template(
            "index2.html",
            Applicants=Applicants,
            len_applicants=len_applicants,
            len_interviews=len_interviews,
            len_emails=len_emails,
            len_mentors=len_mentors,
            form=form,
            update_form=update_form
        )

    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = applicant_methods.filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" DELETE APPLICANT """


@app.route('/delete_applicant/<app_id>', methods=["GET", "POST"])
@login_required
def delete_applicant(app_id):
    if current_user.role != 'admin':
        abort(404)
    user = Applicant.select().where(Applicant.applicant_id == app_id).get()
    if request.method == "GET":
        user.delete_instance(recursive=True)
        return redirect(url_for('homepage'))


"""LIST ALL EMAILS SENT"""


@app.route('/admin/emails', methods=["GET", "POST"])
def list_emails():
    if current_user.role != 'admin':
        abort(404)

    emails = Email.select()
    len_applicants, len_mentors, len_emails, len_interviews = count_menu_items()
    form = forms.FilterEmailForm()
    if request.method == "GET":
        return render_template('email.html',
                               form=form,
                               emails=emails,
                               len_applicants=len_applicants,
                               len_interviews=len_interviews,
                               len_emails=len_emails,
                               len_mentors=len_mentors)

    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = SendEmails.filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" FILTER EMAILS BY TYPE """


@app.route('/emails/filter_by_type/<query>', methods=["GET", "POST"])
@login_required
def filter_by_type(query):
    if current_user.role != 'admin':
        abort(404)
    emails = Email.select().where(Email.email_type.contains(query))
    len_applicants, len_mentors, len_emails, len_interviews = count_menu_items()
    form = forms.FilterEmailForm()
    if request.method == "GET":
        return render_template('email.html',
                               form=form,
                               emails=emails,
                               len_applicants=len_applicants,
                               len_interviews=len_interviews,
                               len_emails=len_emails,
                               len_mentors=len_mentors)

    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = SendEmails.filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" FILTER EMAILS BY SUBJECT """


@app.route('/emails/filter_by_subject/<query>', methods=["GET", "POST"])
@login_required
def filter_by_subject(query):
    if current_user.role != 'admin':
        abort(404)
    emails = Email.select().where(Email.subject.contains(query))
    len_applicants, len_mentors, len_emails, len_interviews = count_menu_items()
    form = forms.FilterEmailForm()
    if request.method == "GET":
        return render_template('email.html',
                               form=form,
                               emails=emails,
                               len_applicants=len_applicants,
                               len_interviews=len_interviews,
                               len_emails=len_emails,
                               len_mentors=len_mentors)

    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = SendEmails.filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" FILTER EMAILS BY RECIPIENT """


@app.route('/emails/filter_by_recipient/<query>', methods=["GET", "POST"])
@login_required
def filter_by_recipient(query):
    if current_user.role != 'admin':
        abort(404)
    emails = Email.select().where(Email.recipient_name.contains(query))
    len_applicants, len_mentors, len_emails, len_interviews = count_menu_items()
    form = forms.FilterEmailForm()
    if request.method == "GET":
        return render_template('email.html',
                               form=form,
                               emails=emails,
                               len_applicants=len_applicants,
                               len_interviews=len_interviews,
                               len_emails=len_emails,
                               len_mentors=len_mentors)

    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = SendEmails.filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


"""LIST ALL INTERVIEWS"""


@app.route('/admin/interviews', methods=["GET", "POST"])
def list_interviews():
    if current_user.role != 'admin':
        abort(404)
    interviews = Interview.select().join(InterviewSlot).switch().join(Applicant)
    form = forms.FilterInterviewForm()
    len_applicants, len_mentors, len_emails, len_interviews = count_menu_items()
    if request.method == "GET":
        return render_template('interview.html',
                               form=form,
                               interviews=interviews,
                               len_applicants=len_applicants,
                               len_interviews=len_interviews,
                               len_emails=len_emails,
                               len_mentors=len_mentors)

    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = interview_methods.filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" FILTER INTERVIEWS BY APPLICANT """


@app.route('/interview/filter_by_applicant/<query>', methods=["GET", "POST"])
@login_required
def filter_by_applicant(query):
    if current_user.role != 'admin':
        abort(404)
    interviews = Interview.select().join(InterviewSlot).switch().join(Applicant).where(
        Applicant.first_name.contains(query) | Applicant.last_name.contains(query))
    len_applicants, len_mentors, len_emails, len_interviews = count_menu_items()
    form = forms.FilterInterviewForm()
    if request.method == "GET":
        return render_template(
            "interview.html",
            form=form,
            interviews=interviews,
            len_applicants=len_applicants,
            len_interviews=len_interviews,
            len_emails=len_emails,
            len_mentors=len_mentors)

    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = interview_methods.filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" FILTER INTERVIEWS BY MENTOR """


@app.route('/interview/filter_by_mentor/<query>', methods=["GET", "POST"])
@login_required
def filter_by_mentor(query):
    if current_user.role != 'admin':
        abort(404)
    interviews = Interview.select().join(InterviewSlot).join(Mentor).switch().join(Applicant).where(
        Mentor.first_name.contains(query) | Mentor.last_name.contains(query))
    print(len(interviews))
    len_applicants, len_mentors, len_emails, len_interviews = count_menu_items()
    form = forms.FilterInterviewForm()
    if request.method == "GET":
        return render_template(
            "interview.html",
            form=form,
            interviews=interviews,
            len_applicants=len_applicants,
            len_interviews=len_interviews,
            len_emails=len_emails,
            len_mentors=len_mentors)

    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = interview_methods.filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" FILTER INTERVIEWS BY MENTOR """


@app.route('/interview/filter_by_location/<query>', methods=["GET", "POST"])
@login_required
def filter_by_location(query):
    if current_user.role != 'admin':
        abort(404)
    interviews = Interview.select().join(Applicant).join(School).where(School.name.contains(query))
    print(len(interviews))
    len_applicants, len_mentors, len_emails, len_interviews = count_menu_items()
    form = forms.FilterInterviewForm()
    if request.method == "GET":
        return render_template(
            "interview.html",
            form=form,
            interviews=interviews,
            len_applicants=len_applicants,
            len_interviews=len_interviews,
            len_emails=len_emails,
            len_mentors=len_mentors)

    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = interview_methods.filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "success")
    return redirect(url_for("login"))


""" APPLICANT HOMEPAGE """


@app.route('/applicant/profile/<query>', methods=["GET", "POST"])
@login_required
def user_page(query):
    # if current_user.role != 'applicant':
    # return redirect(url_for('abort'))
    applicant = Applicant.select().join(User).switch(Applicant).join(
        Interview).join(InterviewSlot).where(User.login == query).get()
    return render_template("profile.html", user=applicant, name=applicant.first_name + " " + applicant.last_name)


@app.route('/mentor', methods=["GET", "POST"])
@login_required
def mentor_page():
    if current_user.is_authenticated:
        if current_user.role != 'mentor':
            abort(404)
    else:
        abort(404)
    mentor = Mentor.get(user_id=current_user.id)
    WEEK_NUMBER = 9
    this_week = get_this_week(WEEK_NUMBER)
    slots_dict = fill_dict(mentor.id, this_week, WEEK_NUMBER)
    number_of_interviews = InterviewSlot.select().join(Interview).where(InterviewSlot.assigned_mentor == mentor.id)
    number_of_interviews = len(number_of_interviews)
    return render_template('mentor_site.html', mentor=mentor, this_week=this_week, weekdays=WEEKDAYS, slots=slots_dict, hours=HOURS, num_intviews=number_of_interviews)


@app.route('/mentors', methods=["GET", "POST"])
@login_required
def mentors():
    LISTA = mentor_methods.get_list()
    list_length = int(len(LISTA))
    if request.method == "GET":
        return render_template("mentors.html", LISTA=LISTA, list_length=list_length)


@app.route('/users', methods=["GET", "POST"])
@login_required
def users():
    LISTA = ApplicantMethods.user_list()
    list_length = int(len(LISTA))
    if request.method == "GET":
        return render_template("users.html", LISTA=LISTA, list_length=list_length)


@app.route('/interview', methods=["GET", "POST"])
@login_required
def interview():
    interviews = interview_methods.get_interviews()
    list_length = int(len(interviews))
    if request.method == "GET":
        return render_template("interviews.html", interviews=interviews, list_length=list_length)


@app.route('/abort', methods=["GET", "POST"])
def abort():
    if request.method == "GET":
        return render_template("abort.html")


if __name__ == "__main__":
    app.run(debug=True)
